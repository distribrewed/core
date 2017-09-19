#!/bin/sh

echo -n "Rebuild distribrewed/master "
curl -X POST \
--write-out '%{http_code}' --silent --output \
-H "Content-Type: application/json" \
-H "Travis-API-Version: 3" \
-H "Accept: application/json" \
-H "Authorization: token $TRAVIS_TOKEN" \
-d '{"request": {"branch": "master"}}' 'https://api.travis-ci.org/repo/distribrewed%2Fmaster/requests'
echo ""

echo -n "Rebuild distribrewed/workers "
curl -X POST \
--write-out '%{http_code}' --silent --output \
-H "Content-Type: application/json" \
-H "Travis-API-Version: 3" \
-H "Accept: application/json" \
-H "Authorization: token $TRAVIS_TOKEN" \
-d '{"request": {"branch": "master"}}' 'https://api.travis-ci.org/repo/distribrewed%2Fworkers/requests'