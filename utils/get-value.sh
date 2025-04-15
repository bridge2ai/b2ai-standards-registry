#!/bin/sh
# get the value of a key in the about.yaml file
# https://stackoverflow.com/questions/1221833/pipe-output-and-capture-exit-status-in-bash

set -o pipefail # ensures the exit status of the script is 1 (failure) if any part of the script fails

grep ^$1: about.yaml | sed "s/$1:[[:space:]]//" || exit 1
