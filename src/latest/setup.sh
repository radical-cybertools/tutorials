#!/bin/bash

WORK_DIR="$PWD"
TUTORIALS_TARBALL_URL="\
https://api.github.com/repos/radical-cybertools/tutorials/tarball/main"

mkdir tutorials_src; cd tutorials_src || true
curl -sL $TUTORIALS_TARBALL_URL | \
  tar --strip-components=2 --wildcards -xz '*/src/*'

for tutorial in radical-pilot radical-entk parsl-rp deepdrivemd; do

    mv "$WORK_DIR/tutorials_src/$tutorial" "$WORK_DIR/$tutorial" ;
    cd "$WORK_DIR/$tutorial" || true

    if [[ -f ./setup.sh ]] ; then
        bash setup.sh && rm ./setup.sh ;
    fi

    if [[ -f ./environment.yml ]] ; then
        mamba env update -n base -f ./environment.yml && rm environment.yml ;
    fi

done

rm -rf "$WORK_DIR/tutorials_src"

