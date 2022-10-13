#!/bin/bash

docker-compose -f docker-compose.yml up --build -d db db-authenticator;
python3 -m pip install virtualenv
python3 -m virtualenv env
source env/bin/activate

services=()

for directory in * ; do
    if [ -d $directory ] ; then
        services+=($directory)
    fi
done

for service in ${services[@]} ; do

    if [ "$service" = "reverse_proxy" ] || [ "$service" = "env" ] ; then
        continue
    fi
    echo "=> Testing service $service"
    echo
    cd $service
    sh test_runner/before_install.sh
    sh test_runner/test.sh
    cd ..
    echo
done
