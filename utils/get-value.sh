#!/bin/sh
# get the value of a key in the about.yaml file
# https://stackoverflow.com/questions/1221833/pipe-output-and-capture-exit-status-in-bash

result=$(grep "^$1:" about.yaml)
if [ $? -eq 0 ]; then
  echo "$result" | sed "s/^$1:[[:space:]]*//"
else
  exit 1
fi
