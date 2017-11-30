
# Install Istio on an existing Kubernetes cluster

Please follow the installation instructions from [istio.io](https://istio.io/docs/setup/kubernetes/quick-start.html).

## Directory structure
This directory contains additional files required for [installing Istio on a Kubernetes cluster](https://github.com/istio/istio/tree/master/install/kubernetes).

* [istio.yaml](https://github.com/istio/istio/blob/master/install/kubernetes/istio.yaml) - Use this file for installation without authentication enabled
* [istio-auth.yaml](https://github.com/istio/istio/blob/master/install/kubernetes/istio-auth.yaml) - Use this file for installation with authentication enabled
* [istio-initializer.yaml](https://github.com/nginmesh/nginmesh/blob/release-doc-0.2.12/istio/release/install/kubernetes/istio-initializer.yaml) - use this file for installation of istio initializer for transparent injection.
* [templates](https://github.com/nginmesh/nginmesh/blob/release-doc-0.2.12/istio/release/install/kubernetes/templates) - directory contains the templates used to generate istio.yaml and istio-auth.yaml
* [addons](https://github.com/istio/istio/blob/master/install/kubernetes/addons) - directory contains optional components (Prometheus, Grafana, Service Graph, Zipkin, Zipkin to Stackdriver)
* updateVersion.sh in the parent directory can be run to regenerate installation files

# Installation Steps

# 
