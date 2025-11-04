#!/bin/bash

(sudo apt-get update  -y && \
 sudo apt-get install -y bc) &> /dev/null || true

