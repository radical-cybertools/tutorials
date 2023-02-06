# Docker container with RADICAL-Cybertools (RCT) tutorial notebooks

## Get container image

RCT Tutorials container is based on 
[jupyter/minimal-notebook](https://github.com/jupyter/docker-stacks) image.

```shell
# BUILD
./docker/build.sh

# OR PULL
docker pull radicalcybertools/tutorials:latest
```

## A. Run `docker-compose`

It starts `rct-tutorials` container with auxiliary service(s), such as MongoDB,
which is used by the RCT components.

```shell
cd docker

docker compose up -d
docker compose logs -f rct-tutorials
# stop containers
#   docker compose stop
# remove containers
#   docker compose rm -f
```

## B. Run container image with MongoDB service manually

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

docker exec rct-mongodb bash -c \
  "mongo --authenticationDatabase admin -u root_user -p root_pass default \
   --eval \"db.createUser({user: 'guest', pwd: 'guest', \
                           roles: [{role: 'readWrite', db: 'default'}]});\""
```

Run container with network:

```shell
docker run --rm -it -p 8888:8888 --network rct-network radicalcybertools/tutorials
```

NOTE: if it is required to work with tutorials located outside the container,
      then a corresponding directory can be mounted - use the following option
      within the command above:

`--mount type=bind,source="$(pwd)/../tutorials",target=/tutorials`

Stop services after work is done:

```shell
# stop container(s)
docker stop rct-mongodb
# stop and remove container(s)
#   docker rm -f rct-mongodb
```
