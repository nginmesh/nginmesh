#!/bin/bash

: '
os=`uname`
if [[ "$os" == 'Darwin' ]]; then
    echo "macOS is detected."

    python --version && pip -v > /dev/null 2>&1
    if [ ! $? -eq 0 ]; then
    echo "install Python and pip"
    brew install python2 && easy_install pip
    fi

    wrk -v > /dev/null 2>&1
    if [ ! $? -eq 0 ]; then
    echo "install wrk HTTP benchmart tool"
    brew install wrk
    fi
    echo "install kubectl"
    curl -LO https://storage.googleapis.com/kubernetes-release/release/`curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt`/bin/darwin/amd64/kubectl

else

    echo "Linux is detected"

    wrk -v > /dev/null 2>&1
    if [ ! $? -eq 0 ]; then
    echo "install wrk HTTP benchmart tool"
    curl -L# https://github.com/wg/wrk/archive/3.1.0.tar.gz | tar zx --strip 1 && make && mv wrk /bin
    fi

    kubectl -v > /dev/null 2>&1
    if [ ! $? -eq 0 ]; then
    echo "install kubectl"
    curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl
    fi
fi
'
virtualenv env
env/bin/pip install -r requirements.txt



