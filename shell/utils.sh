#!/bin/bash

download() {
  wget $1
}

extract() {
  fullpath="$1"
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
