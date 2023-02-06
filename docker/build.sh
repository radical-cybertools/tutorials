#!/bin/bash

RCT_BASE_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]:-$0}"; )/../" &> /dev/null && pwd 2> /dev/null; )"

docker build \
    -t rct-tutorials \
    -f "$RCT_BASE_DIR/docker/Dockerfile" \
    "$RCT_BASE_DIR/tutorials/"
