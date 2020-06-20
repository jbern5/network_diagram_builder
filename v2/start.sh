#!/usr/bin/env bash
docker rmi -f $(docker images -a -q)
docker build --rm -t python-docker-dev .
docker run --rm -it -v /Users/justinbernstein/Documents/GitHub/network_diagram_builder/v2/src/graphs:/graphs --name pyyed_1 python-docker-dev