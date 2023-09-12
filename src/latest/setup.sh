#!/bin/bash

sudo apt-get update  -y && \
sudo apt-get install -y subversion

WORK_DIR="$PWD"
BASE_URL="\
https://github.com/radical-cybertools/tutorials/\
branches/main/src"

for tutorial in radical-pilot radical-entk parsl-rp deepdrivemd; do

    svn export --quiet --force "$BASE_URL/$tutorial" "$WORK_DIR/$tutorial" ;
    cd "$WORK_DIR/$tutorial" || true

    if [[ -f ./setup.sh ]] ; then
        bash setup.sh && rm ./setup.sh ;
    fi

    if [[ -f ./environment.yml ]] ; then
        mamba env update -n base -f ./environment.yml && rm environment.yml ;
    fi

done

