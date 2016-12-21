#!/bin/bash

PYTHON=python3.5
VIRTUALENV_FOLDER=".virtualenv"

if [ ! -d "$VIRTUALENV_FOLDER" ]; then
  virtualenv -p $PYTHON $VIRTUALENV_FOLDER
fi;

source $VIRTUALENV_FOLDER/bin/activate

pip install -r requirements.txt

deactivate
