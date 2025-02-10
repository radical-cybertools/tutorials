#!/bin/bash

if ! test -z "$(which darshan-config)"; then
  echo "Darshan installed"
  exit 0
fi

SCRIPTS_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]:-$0}"; )/" &> /dev/null \
                && pwd 2> /dev/null; )"

# patch EnTK with Darshan related fixes
"$SCRIPTS_DIR/entk-patched.sh"

(sudo apt-get update  -y && \
 sudo apt-get install -y \
      autoconf build-essential cmake libtool tar) \
 &> /dev/null || true

DARSHAN_VER=3.4.6

cd "$HOME" || true
wget -q "https://web.cels.anl.gov/projects/darshan/releases/darshan-$DARSHAN_VER.tar.gz"
tar -xvzf "darshan-$DARSHAN_VER.tar.gz"

cd "$HOME/darshan-$DARSHAN_VER/darshan-runtime/" || true
../prepare.sh
MAKE=gmake ./configure \
  --prefix="/usr/local/" \
  --with-log-path-by-env=DARSHAN_LOG_DIR_PATH \
  --with-jobid-env=NONE --without-mpi CC=gcc
sudo make && sudo make install

cd "$HOME/darshan-$DARSHAN_VER/darshan-util" || true
../prepare.sh
./configure --prefix="/usr/local/"
sudo make && sudo make install

