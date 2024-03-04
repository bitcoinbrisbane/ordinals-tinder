#!/bin/bash
docker stop $1
docker rm $1

git stash
git checkout main
git pull
docker build -t ordinals .
docker run -d -p 8000:8000 ordinals