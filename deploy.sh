#!/bin/bash

# construire l'image
docker rmi -f api-rawls
docker build --no-cache -t api-rawls  .

# Lancer le container
docker stop rawls_api_instance
docker rm rawls_api_instance
docker run --name rawls_api_instance -p 5001:5001 api-rawls