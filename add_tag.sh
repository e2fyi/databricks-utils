#!/usr/bin/bash
set -e
if [ -z "$*" ];
  sed -i "s/version='[0-9]*.[0-9]*.[0-9]*'/version='$1'/" setup.py
  git add .
  git commit -m "Release v$1"
  git tag -a $1 -m "Release v$1"
  git push && git push origin --tags
then
  echo "No version provided!";
fi
