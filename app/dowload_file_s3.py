import boto3

# Inicialize o cliente S3
s3 = boto3.client('s3')

# Defina o bucket e o nome do arquivo no S3
bucket_name = ''
s3_file_key = ''

# Caminho local onde o arquivo será salvo
local_file_path = ''

# Baixar o arquivo
s3.download_file(bucket_name, s3_file_key, local_file_path)

print(f'Arquivo {s3_file_key} baixado para {local_file_path}')
