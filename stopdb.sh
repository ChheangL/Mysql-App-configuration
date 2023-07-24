#! /usr/bin/sh

docker rm -f $(docker ps -a -q)
docker image rm $(docker image ls -q)