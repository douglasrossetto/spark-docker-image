from pyspark.sql import SparkSession
import boto3

# Configurar a SparkSession
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("S3 Access") \
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .config("spark.hadoop.fs.s3a.aws.credentials.provider", 
            "com.amazonaws.auth.DefaultAWSCredentialsProviderChain") \
    .getOrCreate()
    
# Ler da camada raw
raw_path = "s3a://pacman-data-analytics-stream-prod/success/source=plataforma-cobranca-distribuicao/year=2024/month=12/day=05/*/"
data = spark.read.parquet(raw_path)

# Processar e gravar no sandbox
sandbox_path = "s3a://bucket-sandbox/path-to-data/"
data.write.mode("overwrite").parquet(sandbox_path)

print("Processamento concluído!")



import boto3
s3 = boto3.client('s3')
response = s3.list_objects_v2(Bucket='pacman-data-analytics-stream-prod')
print(response)