#!/bin/bash

# Carregar as credenciais da AWS
if [ -f /config/aws_credentials.env ]; then
    export $(cat /config/aws_credentials.env | xargs)
fi

# Executar o script principal
#python3 main.py
