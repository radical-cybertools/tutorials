# Docker container with RADICAL-Cybertools (RCT) tutorial notebooks

## 1. Get container image

(*) RCT Tutorials container is based on 
[jupyter/minimal-notebook](https://github.com/jupyter/docker-stacks) image.

**To have RCT Tutorials container image locally it should be either BUILT or 
PULLED from DockerHub.**

### 1.A. Build container

**Tutorial name** is a subdirectory within `/src` with the target notebook(s).

```shell
# provide a tutorial name and a corresponding tag either as arguments OR 
# with the env variables (will be considered only if arguments are skipped):
#    export RCT_TUTORIAL_NAME=radical-entk
#    export RCT_TUTORIAL_TAG=entk-intro
./docker/build.sh [-n tutorial_name] [-t tag]
```

### 1.B. Pull container

```shell
# use a specific tag to pull a corresponding container ("latest" is default)
docker pull radicalcybertools/tutorials:latest
```

## 2. Run container image

### 2.A. Run `docker-compose`

It starts `rct-tutorials` container with the auxiliary service MongoDB,
which is used by the RCT components as part of a communication layer.

```shell
cd docker
# use a specific tag to pull a corresponding container by setting env variable:
#    export RCT_TUTORIAL_TAG=entk-intro
# if container with defined tag doesn't exist (neither locally nor online),
# then it will be built, thus provide the name for a tutorial:
#    export RCT_TUTORIAL_NAME=radical-entk

docker compose up -d
docker compose logs -f rct-tutorials
# stop containers
#    docker compose stop
# remove containers
#    docker compose rm -f
```

### 2.B. Run container image with MongoDB service manually

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
# set a tag with which container was built or if it is not available locally, 
# then it will be pulled:
#    export RCT_TUTORIAL_TAG=entk-intro
docker run --rm -it -p 8888:8888 --network rct-network \
           radicalcybertools/tutorials:${RCT_TUTORIAL_TAG:-latest}
```

Stop services after work is done:

```shell
# stop container(s)
docker stop rct-mongodb
# stop and remove container(s)
#    docker rm -f rct-mongodb
```

## 3. For tutorial developers

This subsection outlines steps necessary to take for setting up a corresponding 
environment for a tutorial development.

1. Build a basic container for development:

       ./docker/build.sh -n default -t dev

2. Start auxiliary services if needed, as described in 
   [Section 2B](#2b-run-container-image-with-mongodb-service-manually), 
   without running tutorials container image itself;
3. Run the basic container with the **mounted** tutorials source directory:

       docker run --rm -it -p 8888:8888 --network rct-network \
                  --mount type=bind,source="$(pwd)/src",target=/tutorials \
                  radicalcybertools/tutorials:dev

4. Access Jupyter server with the provided URL 
   (e.g., `http://127.0.0.1:8888/lab?token=<token>`);
5. Create a corresponding directory (i.e., _tutorial name_) within the working 
   directory and create files `setup.sh` and `environment.yml` if needed by 
   following templates located in `/default`;
6. Start creating Jupyter notebooks.

**Created tutorial (with the corresponding notebooks) will be preserved locally 
after container being shut down.**

