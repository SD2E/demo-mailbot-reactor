#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source "$DIR/common.sh"

MESSAGE='{"to": "matt.vaughn@gmail.com", "subject": "Hello, computer.", "body":"A keyboard... how quaint."}'
API_KEY=$(jq -r ._REACTOR_API_KEY ${DIR}/../secrets.json)

detect_ci

source reactor.rc

TEMP=`mktemp -d $PWD/tmp.XXXXXX`
echo "Working out of $TEMP"

docker run -t -v ${HOME}/.agave:/root/.agave:rw \
           -v ${TEMP}:/mnt/ephemeral-01:rw \
           -e _REACTOR_API_KEY=${API_KEY} \
           -e MSG='{"to": "matt.vaughn@gmail.com", "subject": "Hello, computer.", "body":"A keyboard... how quaint."}' \
           ${DOCKER_HUB_ORG}/${DOCKER_IMAGE_TAG}:${DOCKER_IMAGE_VERSION}

if [ "$?" == 0 ]; then
    rm -rf ${TEMP}
fi
