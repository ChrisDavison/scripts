#!/usr/bin/env bash
if not docker ps -a | grep -q 'jupyter$'; then
    docker run -it -d -p 8890:8888 -v /home/davison:/home/jovyan --name=jupyter jupyter:latest
else
    docker start jupyter
fi

