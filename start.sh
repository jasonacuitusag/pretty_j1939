#!/bin/bash
SCRIPT_DIR=$(dirname -- $0)
pushd . > /dev/null
cd $SCRIPT_DIR

./dockerrun.sh --no_build

popd > /dev/null
