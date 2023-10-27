# RADICAL-Cybertools (RCT) with MongoDB

The latest RCT packages with MongoDB requirement:

```shell
radical.analytics : 1.34.0
radical.entk      : 1.37.0
radical.pilot     : 1.37.0
radical.saga      : 1.36.0
radical.utils     : 1.33.0
```

The RCT Tutorials container is based on 
[jupyter/minimal-notebook](https://github.com/jupyter/docker-stacks) image.
We prepared a container image with all tutorials available before the `1.40`
release (when we dropped the MongoDB requirement), and uploaded this image to 
[DockerHub](https://hub.docker.com/u/radicalcybertools)
(`radicalcybertools/tutorials:latest-mongo`). The following commands pull and 
run the RCT Tutorials container locally (**NOTE**: `docker` and/or 
`docker-compose` are required to be installed locally).

## 1. Run containers with `docker-compose`

```shell
wget https://raw.githubusercontent.com/radical-cybertools/tutorials/main/docker/mongo/docker-compose.yaml
export RCT_TUTORIAL_TAG=latest-mongo
docker compose up -d
docker compose logs -f rct-tutorials
# stop and remove containers
#    docker compose down
```

## 2. Run containers manually

These steps do the same as `docker-compose`, but all necessary commands are
executed manually.

Docker network to communicate with service(s):

```shell
docker network create rct-network
```

Launch MongoDB service:

```shell
docker run -d --hostname mongodb --name rct-mongodb -p 27017:27017 \
           -e MONGO_INITDB_ROOT_USERNAME=root_user \
           -e MONGO_INITDB_ROOT_PASSWORD=root_pass \
           -e MONGO_INITDB_USERNAME=guest \
           -e MONGO_INITDB_PASSWORD=guest \
           -e MONGO_INITDB_DATABASE=default \
           --network rct-network mongo:4.4
```
```shell
docker exec rct-mongodb bash -c \
  "mongo --authenticationDatabase admin -u root_user -p root_pass default \
   --eval \"db.createUser({user: 'guest', pwd: 'guest', \
                           roles: [{role: 'readWrite', db: 'default'}]});\""
```

Run container with network:

```shell
docker run --rm -it -p 8888:8888 --network rct-network \
           radicalcybertools/tutorials:latest-mongo
```

Stop services after work is done:

```shell
# stop container
docker stop rct-mongodb
# remove container and network
#    docker rm -f rct-mongodb
#    docker network remove rct-network
```

