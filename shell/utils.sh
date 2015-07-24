#!/bin/bash

download() {
  fullpath="$1"
  wget $fullpath
  if [[ "$fullpath" == *tar.gz ]]; then
    echo "Command => tar xfz ${fullpath##*/}"
    tar xfz ${fullpath##*/}
  else
    if [[ "$fullpath" == *tar.bz2 ]]; then
      echo "Command => tar xfj ${fullpath##*/}"
      tar xfj ${fullpath##*/}
    fi
  fi
}
