#!/bin/bash

# setup pypy3
if ! hash pypy3.3 2>/dev/null; then
  echo 'Need to install pypy3.3.'
  # download pypy
  wget "https://bitbucket.org/pypy/pypy/downloads/pypy3.3-v5.5.0-alpha-linux64.tar.bz2"
  # extract the folder
  tar xvjf pypy3.3-v5.5.0-alpha-linux64.tar.bz2
  # remove the zipped file
  rm pypy3.3-v5.5.0-alpha-linux64.tzr.bz2
  # move the file to the opt folder
  mv pypy3.3-v5.5.0-linux64/ /opt
  # create the link so we can use 'pypy3.3' instead of writing the full path
  ln -s "/opt/pypy3.3-v5.5.0-linux64/bin/pypy3.3" "/usr/local/bin/"
else
  echo 'PyPy3.3 already installed on system.'
fi
