# Docker container with RADICAL-Cybertools (RCT) tutorial notebooks

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/radical-cybertools/tutorials/main)

> [!IMPORTANT]
> [Binder](https://mybinder.readthedocs.io) lets you run and test our RCT
> notebooks. You should **not** expect Binder to match the performance
> achievable by RCT on local or high performance computing (HPC) platforms.
> If performance is a consideration, please consider executing our RCT Docker
> container locally or in a suitable HPC environment.

## How to run

The RCT Tutorials container is based on
[jupyter/minimal-notebook](https://github.com/jupyter/docker-stacks) image.
We prepared a container image with all the latest tutorials in this
repository, and uploaded this image to
[DockerHub](https://hub.docker.com/u/radicalcybertools)
(`radicalcybertools/tutorials:seavea-hackathon-2025`). The following command
pulls and runs the RCT Tutorials container locally (**NOTE**: `docker` is
required to be installed locally):

```shell
docker run --rm -it -p 8888:8888 radicalcybertools/tutorials:seavea-hackathon-2025
```

## Documentation

* RADICAL-EnTK:  https://radicalentk.readthedocs.io/
* RADICAL-Pilot: https://radicalpilot.readthedocs.io/

