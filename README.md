# Docker container with RADICAL-Cybertools (RCT) tutorial notebooks

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/radical-cybertools/tutorials/fix/mybinder)

> [!IMPORTANT]
> [Binder](https://mybinder.readthedocs.io) lets you run and test our RCT 
> notebooks. You should **not** expect Binder to match the performance 
> achievable by RCT on local or high performance computing (HPC) platforms. 
> If performance is a consideration, please consider executing our RCT Docker 
> container locally or in a suitable HPC environment.

* [Quickstart](#1-quickstart)
* [Build container locally](#2-build-container-locally)
* [For tutorial developers](#3-for-tutorial-developers)

## 1. Quickstart

The RCT Tutorials container is based on 
[jupyter/minimal-notebook](https://github.com/jupyter/docker-stacks) image.
We prepared a container image with all the latest tutorials in this 
repository, and uploaded this image to
[DockerHub](https://hub.docker.com/u/radicalcybertools)
(`radicalcybertools/tutorials:latest`). The following command pulls and runs
the RCT Tutorials container locally (**NOTE**: `docker` is required to be 
installed locally):

```shell
docker run --rm -it -p 8888:8888 radicalcybertools/tutorials:latest
```

## 2. Build container locally

**Tutorial name** is a subdirectory within `/src` with the target notebook(s).

```shell
# provide a tutorial name and a corresponding tag either as arguments OR 
# with the env variables (will be considered only if arguments are skipped):
#    export RCT_TUTORIAL_NAME=radical-entk
#    export RCT_TUTORIAL_TAG=latest-entk
./docker/build.sh [-n tutorial_name] [-t tag]
```
```shell
# set a tag with which container was built or if it is not available locally, 
# then it will be pulled:
#    export RCT_TUTORIAL_TAG=latest-entk
docker run --rm -it -p 8888:8888 \
           radicalcybertools/tutorials:${RCT_TUTORIAL_TAG:-latest}
```

## 3. For tutorial developers

This subsection outlines steps necessary to take for setting up a corresponding 
environment for a tutorial development.

1. Build a basic container for development (`devel`-branches of the RADICAL
   stack):

       ./docker/build.sh -n devel -t devel

2. Run the basic container with the **mounted** tutorials source directory:

       docker run --rm -it -p 8888:8888 \
                  --mount type=bind,source="$(pwd)/src",target=/tutorials \
                  radicalcybertools/tutorials:devel

3. Access Jupyter server with the provided URL 
   (e.g., `http://127.0.0.1:8888/lab?token=<token>`);
4. Create a corresponding directory (i.e., _tutorial name_) within the working 
   directory and create files `setup.sh` and `environment.yml` if needed by 
   following templates located in `/default`;
5. Start creating Jupyter notebooks.

Created tutorial (with the corresponding notebooks) will be preserved locally 
after container being shut down.

