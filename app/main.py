from pyspark.sql import SparkSession
import boto3

# Configurar a SparkSession
spark = SparkSession.builder \
    .appName("Spark AWS Test") \
    .config("spark.hadoop.fs.s3a.access.key", "AWS_ACCESS_KEY_ID") \
    .config("spark.hadoop.fs.s3a.secret.key", "AWS_SECRET_ACCESS_KEY") \
    .config("spark.hadoop.fs.s3a.endpoint", "s3.amazonaws.com") \
    .getOrCreate()

# Ler da camada raw
raw_path = "s3a://bucket-raw/path-to-data/"
data = spark.read.json(raw_path)

# Processar e gravar no sandbox
sandbox_path = "s3a://bucket-sandbox/path-to-data/"
data.write.mode("overwrite").parquet(sandbox_path)

print("Processamento concluído!")
