#!/bin/bash

#(sudo apt-get update  -y && \
# sudo apt-get install -y bc) &> /dev/null || true

WORK_DIR="$PWD"

# get ROSE tutorial(s)
TARBALL_URL="\
https://github.com/radical-cybertools/ROSE/tarball/feature/tutorial"
mkdir -p "$WORK_DIR/ROSE"; cd "$WORK_DIR/ROSE" || true
curl -sL $TARBALL_URL | \
  tar --transform='s/.*\///' \
      --wildcards -xz \
      '*/examples/tutorials/**.ipynb'

cd "$WORK_DIR" || true

