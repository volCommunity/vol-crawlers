#!/usr/bin/env bash

set -eo pipefail

clean () {
    ARG=$?
    if [[ $CI == True ]] ;then
        echo "Running from CI, removing scrapinghub.yml"
        rm scrapinghub.yml
    fi
    exit $ARG
}

trap clean EXIT
if [[ $SCRAPY_API == "" ]] ; then
    echo "Need SCRAPY_API to be set, bailing"
    exit 1
fi
sed s/SCRAPY_API_KEY/${SCRAPY_API}/ < templates/scrapinghub.tmpl > scrapinghub.yml
echo "Deploying to Scrapinghub.."
shub deploy
