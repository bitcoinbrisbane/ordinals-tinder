#!/bin/bash
# docker stop ordinals
# docker rm ordinals
git stash
git checkout main
git pull
docker build -t ordinals .
docker run -d -p 8000:8000 ordinals