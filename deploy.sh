#!/bin/bash
git pull origin main

# construire l'image
if [[ "$(docker images -q api-rawls 2> /dev/null)" != "" ]]; then
    docker rmi -f api-rawls
fi

docker build --no-cache -t api-rawls  .

# Lancer le container
if [[ "$(docker ps -q rawls_api_instance 2> /dev/null)" != "" ]]; then
    docker stop rawls_api_instance
    docker rm rawls_api_instance
fi
docker run --name rawls_api_instance -p 5001:5001 api-rawls