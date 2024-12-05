import boto3

# Inicialize o cliente S3
s3 = boto3.client('s3')

# Defina o bucket e o nome do arquivo no S3
bucket_name = 'pacman-data-analytics-stream-prod'
s3_file_key = 'success/source=plataforma-cobranca-distribuicao/year=2024/month=12/day=05/hour=05/pacman-firehose-to-s3-with-parquet-9-2024-12-05-05-54-27-64b49ed0-6946-383a-9db9-51c7e0e975ca.parquet'

# Caminho local onde o arquivo será salvo
local_file_path = '/root/tmp/files/parquet_teste_divida.parquet'

# Baixar o arquivo
s3.download_file(bucket_name, s3_file_key, local_file_path)

print(f'Arquivo {s3_file_key} baixado para {local_file_path}')
