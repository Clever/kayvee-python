#!/bin/bash

# Publishes package to pypi and creates git tags.
# Reads version from VERSION file.

set -eo pipefail

version=`cat VERSION`
changelog=CHANGELOG.md
grep $version $changelog >> /dev/null
if [[ $? -ne 0 ]]; then
  echo "Couldn't find version $version in $changelog"
  exit
fi

read -p "Publish and tag as v$version? " -n 1 -r
if [[ $REPLY =~ ^[Yy]$ ]]; then
  # publish to pypi
  python3 setup.py sdist bdist_wheel
  twine check dist/*
  TWINE_PASSWORD=$(ark secrets read production.kayvee-python pypi-publish-token | sed -n 2p) twine upload dist/* -u __token__
  # create git tags
  git tag -a v$version -m "version $version"
  git push --tags
fi
