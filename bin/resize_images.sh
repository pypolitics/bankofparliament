#!/bin/bash

for i in ../lib/images/* ; do
  if [ -f "$i" ]; then
    echo "$i"
    oiiotool "$i" --resize 128x128 -o "$i.jpg"
  fi
done