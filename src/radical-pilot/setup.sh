#!/bin/bash

sudo apt-get update  -y && \
sudo apt-get install -y subversion

TUTORIALS_BASE_URL="\
https://github.com/radical-cybertools/radical.pilot/\
branches/master/docs/source"

echo "Export tutorials from $TUTORIALS_BASE_URL"
svn export --quiet --force "$TUTORIALS_BASE_URL/getting_started.ipynb" .
svn export --quiet --force "$TUTORIALS_BASE_URL/tutorials" .

