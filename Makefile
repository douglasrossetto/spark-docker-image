# Variáveis
IMAGE_NAME = docker-spark-aws
CONTAINER_NAME = spark-aws-container
CONFIG_DIR = $(PWD)/config
APP_DIR = $(PWD)/app
AWS_PROFILE ?= 
TOKEN_SCRIPT = $(CONFIG_DIR)/generate_token.py

# Construir a imagem Docker
build:
	docker build -t $(IMAGE_NAME) .

# Gerar o token do AWS SSO
generate-token:
	@if [ -f $(TOKEN_SCRIPT) ]; then \
		echo "Gerando token AWS SSO..."; \
		python3 $(TOKEN_SCRIPT) --profile $(AWS_PROFILE); \
	else \
		echo "Script $(TOKEN_SCRIPT) não encontrado!"; \
		exit 1; \
	fi

# Executar o contêiner para testes
run: generate-token
	docker run --rm --name spark-container \
		-v $(PWD)/app:/workspace \
		-v $(PWD)/config/aws_credentials.env:/root/.aws/credentials \
		$(IMAGE_NAME)

# Subir o contêiner em modo interativo para depuração
debug: generate-token
	docker run --rm --name $(CONTAINER_NAME) -it \
		-v $(CONFIG_DIR):/config \
		-v $(APP_DIR):/app \
		-e AWS_PROFILE=$(AWS_PROFILE) \
		$(IMAGE_NAME) bash

# Preparar o ambiente copiando o arquivo de modelo
prepare-environment:
	@if [ ! -f $(CONFIG_DIR)/aws_credentials.env ]; then \
		cp $(CONFIG_DIR)/aws_credentials.env_template $(CONFIG_DIR)/aws_credentials.env; \
		echo "Arquivo 'aws_credentials.env' criado. Atualize com suas credenciais."; \
	else \
		echo "Arquivo 'aws_credentials.env' já existe. Nada a fazer."; \
	fi

# Limpar contêineres e imagens antigos
clean:
	docker rmi -f $(IMAGE_NAME)

# Usar o contêiner como ambiente de desenvolvimento no VSCode
vscode: generate-token
	docker run --rm --name $(CONTAINER_NAME) -it \
		-v $(CONFIG_DIR):/config \
		-v $(APP_DIR):/app \
		-v $(PWD):/workspace \
		-w /workspace \
		-p 4040:4040 \
		$(IMAGE_NAME) bash
