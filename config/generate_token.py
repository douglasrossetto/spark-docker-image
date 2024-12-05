import os
import json
import subprocess
import argparse
from datetime import datetime, timezone

CONFIG_PATH = os.getenv("HOME") + "/.aws/config"
CREDENTIAL_FILE = os.getenv("HOME") + "/.aws/sso/cache/"
ENV_FILE = os.getcwd() + "/config/aws_credentials.env"
ENV_LIST = [
    "AWS_ACCESS_KEY_ID",
    "AWS_SECRET_ACCESS_KEY",
    "AWS_SESSION_TOKEN",
]

PAYLOAD = """
{
    "aws_access_key_id": "$clientId",
    "aws_secret_access_key": "$clientSecret",
    "aws_session_token": "$accessToken",
    "region": "sregion"
}
"""

def check_sso_login(profile):
    """
    Check if the SSO token is valid, and log in if necessary.
    """
    try:
        # Get the SSO cache directory
        files = os.listdir(CREDENTIAL_FILE)
        for file in files:
            credentials_path = os.path.join(CREDENTIAL_FILE, file)
            with open(credentials_path) as cred_file:
                credentials = json.load(cred_file)
                expiration = credentials.get("expiresAt")
                if expiration:
                    expiration_time = datetime.fromisoformat(expiration.replace("Z", "+00:00"))
                    if expiration_time > datetime.now().replace(tzinfo=timezone.utc):
                        print("SSO token is valid.")
                        return
        print("SSO token has expired or is not present.")
    except Exception as e:
        print(f"Error checking SSO login: {e}")

    # Prompt user to log in
    print(f"Logging into AWS SSO for profile '{profile}'...")
    subprocess.run(f"aws sso login --profile {profile}", shell=True, check=True)
    print("Login completed.")


def process_aws_file(credentials_file):
    credentials = {}
    files = os.listdir(credentials_file)
    for credentals_file in files:
        credentials.update(json.load(open(CREDENTIAL_FILE + credentals_file)))
    credentials = (
        PAYLOAD.replace("$clientId", credentials["clientId"])
        .replace("$clientSecret", credentials["clientSecret"])
        .replace("$accessToken", credentials["accessToken"])
        .replace("$region", credentials["region"])
    )

    return credentials

def process_aws_config(profile, credentials):
    account_id = subprocess.check_output(
        f"aws configure get sso_account_id --profile {profile}",
        shell=True,
        encoding="utf-8",
    ).rstrip()
    role_name = subprocess.check_output(
        f"aws configure get sso_role_name --profile {profile}",
        shell=True,
        encoding="utf-8",
    ).rstrip()
    region = subprocess.check_output(
        f"aws configure get sso_region --profile {profile}",
        shell=True,
        encoding="utf-8",
    ).rstrip()

    output = subprocess.check_output(
        f"aws sso get-role-credentials --account-id {account_id} --role-name {role_name} "
        f"--access-token {json.loads(credentials)['aws_session_token']} --region {region} "
        f"--profile {profile}",
        shell=True,
    )

    output_credentials = json.loads(output)["roleCredentials"]
    return output_credentials


def write_env(env_file, credentials, env_data):
    for line in env_data:
        if "AWS_ACCESS_KEY_ID" in line:
            line = f"AWS_ACCESS_KEY_ID={credentials['accessKeyId']}\n"
        elif "AWS_SECRET_ACCESS_KEY" in line:
            line = f"AWS_SECRET_ACCESS_KEY={credentials['secretAccessKey']}\n"
        elif "AWS_SESSION_TOKEN" in line:
            line = f"AWS_SESSION_TOKEN={credentials['sessionToken']}\n"
        env_file.write(line)


def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description="Process AWS credentials and update environment file."
    )
    parser.add_argument("--profile", required=True, help="AWS SSO profile name")
    args = parser.parse_args()

    profile = args.profile
    
    # Check SSO login status
    check_sso_login(profile)

    # Process the credentials and environment
    credentials = process_aws_file(CREDENTIAL_FILE)
    aws_credentials = process_aws_config(profile, credentials)

    with open(ENV_FILE, "r") as env_file:
        env_data = env_file.readlines()

    with open(ENV_FILE, "w") as env_file:
        write_env(env_file, aws_credentials, env_data)

if __name__ == "__main__":
    main()
