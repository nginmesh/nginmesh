#!/bin/bash
./nginx-inject -proxy-image gcr.io/nginmesh/istio-nginx-sidecar:0.27-alpha-dev -init-image gcr.io/nginmesh/istio-nginx-init:0.27-alpha-dev -f bookinfo.yaml  | kubectl create -f -
