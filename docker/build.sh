#!/bin/bash

RCT_BASE_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]:-$0}"; )/../" &> /dev/null && pwd 2> /dev/null; )"

while getopts ":n:t:" option; do
   case $option in
      n) # tutorial name
         NAME=$OPTARG;;
      t) # tutorial tag
         TAG=$OPTARG;;
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

echo "Build docker container $TAG (name: ${NAME:-n/a})"
docker build \
    -t "$TAG" \
    --build-arg TUTORIAL_NAME="$NAME"\
    -f "$RCT_BASE_DIR/docker/Dockerfile" \
    "$RCT_BASE_DIR/tutorials/"
