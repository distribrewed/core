#!/bin/sh

echo -n "Rebuild $REPO "
URL=$(echo $REPO | sed 's/\//%2F/g')
curl -X POST \
--write-out '%{http_code}' --silent --output /dev/null \
-H "Content-Type: application/json" \
-H "Travis-API-Version: 3" \
-H "Accept: application/json" \
-H "Authorization: token $TRAVIS_TOKEN" \
-d '{"request": {"branch": "master"}}' https://api.travis-ci.org/repo/${URL}/requests