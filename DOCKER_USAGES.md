# Utilisation de Docker

## Quelques commandes

Voir les instances dockers qui tournent :
```
docker ps
```

Voir toutes les instances docker même celles qui ne tournent pas : 
```
docker ps -a
```

Stopper une instance Docker :
```
docker stop <container-id>
```

Supprimer une instance Docker :
```
docker rm <container-id>
```

Liste des images docker :
```
docker images
```

Supprimer une image docker :
```
docker rmi <image-tag>
```


## Générer notre image et notre instance

Fichier `Dockerfile` utilisé pour représenter l'image API rawls (ci-besoin, voir ce [lien](https://docs.docker.com/language/python/build-images/)).

Création de l'image docker pour l'API rawls
```
docker build -t api-rawls  .
```

```
docker run --name rawls_api_instance -p 5001:5001 api-rawls
```