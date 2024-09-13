#!/bin/bash
SCRIPT_DIR=$(dirname -- $0)
pushd . > /dev/null
cd $SCRIPT_DIR

DOCKER_IMAGE_NAME="can-pretty-printer"

if [ "$1" != "--no_build" ]; then
    docker build -t $DOCKER_IMAGE_NAME --progress=plain ./

    if [ ! $? -eq 0 ]; then
        echo [Build failed]
        exit 1
    fi

    docker rmi $(docker images -f "dangling=true" -q) 2> /dev/null
fi

docker run --rm -it $DOCKER_IMAGE_NAME

popd > /dev/null
