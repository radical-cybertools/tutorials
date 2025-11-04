#!/bin/bash

WORK_DIR="$PWD"

TUTORIAL_URL_BASE="https://github.com/radical-cybertools"
TUTORIAL_PATH="*/examples/tutorials/*"
TUTORIAL_REPO=(\
 "radical.asyncflow/tarball/main" \
 "ROSE/tarball/main"
)

for repo in "${TUTORIAL_REPO[@]}"; do

    IFS="/" read -r tutorial_dir _ <<< "$repo" ;
    mkdir -p "$WORK_DIR/$tutorial_dir" ;
    cd "$WORK_DIR/$tutorial_dir" || true

    curl -sL "$TUTORIAL_URL_BASE/$repo" | \
         tar --transform='s/.*\///' --wildcards -xz $TUTORIAL_PATH

    if [[ -f ./setup.sh ]] ; then
        bash setup.sh && rm ./setup.sh ;
    fi

    if [[ -f ./environment.yml ]] ; then
        mamba env update -n base -f ./environment.yml && rm environment.yml ;
    fi

    if [[ -f ./pyproject.toml ]] ; then
        pip install -e .[$(python -c "import tomllib; print(','.join(tomllib.load(open('pyproject.toml','rb'))['project']['optional-dependencies'].keys()))")] ;
        rm -rf *.egg-info ;
    fi

done

