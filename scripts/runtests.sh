#!/bin/bash

PYTHON=python3.5
VIRTUALENV_FOLDER='.virtualenv-tests'

if [ ! -d "$VIRTUALENV_FOLDER" ]; then
  virtualenv -q -p $PYTHON $VIRTUALENV_FOLDER
fi;

source $VIRTUALENV_FOLDER/bin/activate

pip install -q -r requirements-test.txt

# Run tests
.virtualenv-tests/bin/nosetests --with-coverage \
                                --cover-xml \
                                --cover-package=nout
