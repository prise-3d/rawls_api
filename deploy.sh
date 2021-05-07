#!/bin/bash
git pull origin main

# construire l'image
if [[ "$(docker images -q api-rawls 2> /dev/null)" != "" ]]; then
    docker rmi -f api-rawls
fi

docker build --no-cache -t api-rawls  .

# Lancer le container
if [[ "$(docker ps | grep rawls_api_instance 2> /dev/null)" != "" ]]; then
    docker stop rawls_api_instance
    docker rm rawls_api_instance
fi

if [[ "$(docker ps -a | grep rawls_api_instance 2> /dev/null)" != "" ]]; then
    docker rm rawls_api_instance
fi

docker run -d --name rawls_api_instance --volume /mnt/rawls/p3d_output:/app/rawls -p 5001:5001 api-rawls