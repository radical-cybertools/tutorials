#!/bin/bash

RCT_BASE_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]:-$0}"; )/../" &> /dev/null && pwd 2> /dev/null; )"

while getopts ":n:t:p:" option; do
   case $option in
      n) # tutorial name
         NAME=$OPTARG;;
      t) # tutorial tag
         TAG=$OPTARG;;
      p) # build platform
         PLATFORM=$OPTARG;;
     \?) # unknown option
         echo "Unknown option $OPTARG";;
   esac
done

if [[ -z $NAME ]]; then
    NAME="${RCT_TUTORIAL_NAME}"
fi

if [[ -z $TAG ]]; then
    TAG="${RCT_TUTORIAL_TAG:-latest}"
fi
TAG="radicalcybertools/tutorials:$TAG"

if [[ -z $PLATFORM ]]; then
    PLATFORM="linux/amd64"
fi

echo "Build docker container $TAG (name: ${NAME:-n/a})"
docker build \
    -t "$TAG" \
    --build-arg TUTORIAL_NAME="$NAME" \
    --build-arg BUILDPLATFORM="$PLATFORM" \
    -f "$RCT_BASE_DIR/docker/Dockerfile" \
    "$RCT_BASE_DIR/src/"

