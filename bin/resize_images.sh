#!/bin/bash

# for i in ../lib/data/images/4* ; do
#   if [ -f "$i" ]; then
#     echo "$i"
#     oiiotool "$i" --resize 128x128 -o "$i"
#   fi
# done

oiiotool ../lib/data/images/male.png --resize 128x128 -o ../lib/data/images/male.png
oiiotool ../lib/data/images/female.png --resize 128x128 -o ../lib/data/images/female.png