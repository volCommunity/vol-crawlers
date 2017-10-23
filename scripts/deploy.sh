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
echo "Preparing scrapinghub.yml.."
sed s/SCRAPY_API_KEY/${SCRAPY_API}/ < templates/scrapinghub.tmpl > scrapinghub.yml
echo "Generating requirements.txt for Scrapinghub.."
pipenv lock -r > requirements.txt
echo "Deploying to Scrapinghub.."
shub deploy
echo "Done!"
