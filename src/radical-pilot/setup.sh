#!/bin/bash

sudo apt-get update  -y && \
sudo apt-get install -y subversion

BRANCH="docs/nb_section3"
TUTORIALS_URL="\
https://github.com/radical-cybertools/radical.pilot/\
branches/$BRANCH/docs/source/tutorials"

echo "Export tutorials from $TUTORIALS_URL"
svn export --quiet --force "$TUTORIALS_URL" .

