
# Service Mesh with Istio and NGINX

This repo provides an implementation of sidecar proxy for Istio using NGINX open source version.

## What is Service Mesh and Istio?

Please see https://istio.io for detail explanation of service mesh provided by Istio.  
Combination of Nginx and Istio provides best service mesh for deploying micro-services.

## Production Status

This version of nginmesh work with with 0.2.12 release of Istio.
Please see below for Istio features we support.  Nginmesh is not production ready yet.  


<TBD>

## Architecture

Please see diagram below to see how Nginx Sidecar Proxy is implemented as of 0.16 version.
The sidecar run NGINX open source version with custom module to interface to Istio Mixer.

![Alt text](/images/nginx_sidecar.png?raw=true "Nginx Sidecar")

## Quick start

The sample app is copied from Istio project without modification.  We only support deployment using Kubernetes initializer.  

[Prerequisities](https://istio.io/docs/setup/kubernetes/quick-start.html#prerequisites)

[Installation steps]()

[Deploy Bookinfo Reference application]()

Optional: 

[In-Depth Telemetry]()

[Intelligent Routing]()
