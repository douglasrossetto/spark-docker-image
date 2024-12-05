FROM openjdk:8-jdk-slim

# Instalações básicas
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    wget \
    curl \
    && apt-get clean

# Instalar Spark
ENV SPARK_VERSION=3.3.1
ENV HADOOP_VERSION=3
ENV SPARK_HOME=/opt/spark
RUN wget https://downloads.apache.org/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz \
    && tar -xvf spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz \
    && mv spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION} $SPARK_HOME \
    && rm spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz

ENV PATH="$SPARK_HOME/bin:$PATH"

# Instalar bibliotecas Python
COPY requirements.txt /
RUN pip3 install -r /requirements.txt

# Copiar arquivos necessários
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Configurar diretório da aplicação
WORKDIR /app
COPY app /app
COPY config /config

ENTRYPOINT ["/entrypoint.sh"]
