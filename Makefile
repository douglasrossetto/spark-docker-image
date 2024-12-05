# Variáveis
IMAGE_NAME = docker-spark-aws
CONTAINER_NAME = spark-aws-container
CONFIG_DIR = $(PWD)/config
APP_DIR = $(PWD)/app

# Construir a imagem Docker
build:
	docker build -t $(IMAGE_NAME) .

# Executar o contêiner para testes
run:
	docker run --rm --name $(CONTAINER_NAME) -v $(CONFIG_DIR):/config -v $(APP_DIR):/app $(IMAGE_NAME)

# Subir o contêiner em modo interativo para depuração
debug:
	docker run --rm --name $(CONTAINER_NAME) -it -v $(CONFIG_DIR):/config -v $(APP_DIR):/app $(IMAGE_NAME) bash

# Limpar contêineres e imagens antigos
clean:
	docker rmi -f $(IMAGE_NAME)

# Usar o contêiner como ambiente de desenvolvimento no VSCode
vscode:
	docker run --rm --name $(CONTAINER_NAME) -it \
		-v $(CONFIG_DIR):/config \
		-v $(APP_DIR):/app \
		-v $(PWD):/workspace \
		-w /workspace \
		-p 4040:4040 \
		$(IMAGE_NAME) bash
