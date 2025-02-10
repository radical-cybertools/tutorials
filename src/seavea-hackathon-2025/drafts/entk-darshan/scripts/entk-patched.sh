#!/bin/bash

SCRIPTS_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]:-$0}"; )/" &> /dev/null \
                && pwd 2> /dev/null; )"

REPO_DIR="$HOME/entk"
git clone --single-branch --branch master \
    https://github.com/radical-cybertools/radical.entk.git "$REPO_DIR"

cd "$REPO_DIR" || true
git apply "$SCRIPTS_DIR/entk.patch"
pip install .

