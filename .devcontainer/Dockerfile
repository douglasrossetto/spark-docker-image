FROM openjdk:11-slim

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y python3 python3-pip curl procps

# Instalar Spark
ENV SPARK_VERSION=3.4.4
RUN curl -L https://dlcdn.apache.org/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop3.tgz \
    | tar -xz -C /opt && mv /opt/spark-${SPARK_VERSION}-bin-hadoop3 /opt/spark

# Adicionar Spark ao PATH
ENV PATH="/opt/spark/bin:/opt/spark/sbin:$PATH"
ENV SPARK_DIST_CLASSPATH="$(/opt/spark/bin/spark-classpath)"

ENV HADOOP_HOME=/opt/hadoop
ENV SPARK_HOME=/opt/spark
ENV SPARK_NO_DAEMONIZE=1


# Configurar variáveis de ambiente para a AWS
ENV AWS_SHARED_CREDENTIALS_FILE=/root/.aws/credentials
ENV AWS_DEFAULT_REGION=us-east-1

# Configurar Hadoop para suporte ao S3
RUN curl -o /opt/spark/jars/hadoop-aws-3.3.6.jar \
    https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.4.1/hadoop-aws-3.3.6.jar && \
    curl -o /opt/spark/jars/aws-java-sdk-bundle-1.12.550.jar \
    https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.12.99/aws-java-sdk-bundle-1.12.550.jar

# Instalar bibliotecas Python necessárias
COPY requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt

# Definir diretório de trabalho
WORKDIR /workspace

# Comando padrão
CMD ["bash"]

ENTRYPOINT ["/opt/spark/bin/spark-submit"]