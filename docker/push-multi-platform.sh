#!/bin/bash

RCT_BASE_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]:-$0}"; )/../" &> /dev/null && pwd 2> /dev/null; )"

# push to the DockerHub registry
docker buildx create --use --name rct_builder
docker buildx build \
    --output=type=registry \
    --platform linux/amd64,linux/arm64 \
    -t radicalcybertools/tutorials \
    -f "$RCT_BASE_DIR/docker/Dockerfile" \
    "$RCT_BASE_DIR/tutorials/"
