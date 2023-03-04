#!/bin/bash
result=$( docker images -q fastapi )
if [[ -n "$result" ]]
then
  docker run -ti --rm --name fastapi -p 80:80 fastapi
else
  docker build -t fastapi . && docker run -ti --rm --name fastapi -p 80:80 fastapi
fi
