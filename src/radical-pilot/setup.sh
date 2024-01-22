#!/bin/bash

# ensure that necessary package is installed
sudo apt-get update  -y && \
sudo apt-get install -y curl

RADICAL_PILOT_TARBALL_URL="\
https://api.github.com/repos/radical-cybertools/radical.pilot/tarball/master"

curl -sL $RADICAL_PILOT_TARBALL_URL | \
  tar --transform='s/.*\///' --wildcards -xz '*/docs/source/**.ipynb'

