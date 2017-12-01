
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
Below are instructions to setup the Istio service mesh in a Kubernetes cluster using NGiNX as a sidecar.
 

### [Prerequisities](https://istio.io/docs/setup/kubernetes/quick-start.html#prerequisites) Make sure alpha enabled kubernetes cluster up and running in Google Container Engine.

### [Installation steps](https://github.com/nginmesh/nginmesh/tree/release-doc-0.2.12/istio/release/install/kubernetes) Instructions for installing Istio with NGiNX as a sidecar in application pods.

1.  Download Istio release 0.2.12:

```
curl -L https://git.io/getLatestIstio | ISTIO_VERSION=0.2.12 sh -
```

2. Download Nginmesh release 0.2.12:
```
curl -L https://github.com/nginmesh/nginmesh/releases/tag/0.2.12-RC2
```

3. In nginmesh folder update version:
```
./nginmesh/istio/updateVersion.sh
```
4. Create Istio deployment without authentication:
```
kubectl create -f install/kubernetes/istio.yaml
```
5. Deploy automatic sidecar injection initializer:
```
kubectl apply -f install/kubernetes/istio-initializer.yaml
```

#### Verify Install
```
kubectl get pods -n istio-system    #-- Istio pods status
kubectl get svc  -n istio-system      #-- Istio services status
```

#### Uninstall
```
kubectl delete -f install/kubernetes/istio.yaml #-- Delete Istio without auth enabled
kubectl delete -f install/kubernetes/istio-auth.yaml #-- Delete Istio without auth enabled
kubectl delete -f install/kubernetes/istio-initializer.yaml #Delete Initializer
```

####  Verify uninstall
```
kubectl get pods -n istio-system #-- Istio pods should be deleted
kubectl get svc  -n istio-system      #-- Istio services should be deleted
```

### [Deploy Bookinfo Reference application](https://istio.io/docs/guides/bookinfo.html) 
The sample app is copied from Istio project without modification.  We only support deployment using Kubernetes initializer. 



Optional: 

[In-Depth Telemetry](https://istio.io/docs/guides/telemetry.html) This sample demonstrates how to obtain uniform metrics, logs, traces across different services using NGiNX sidecar.

[Intelligent Routing](https://istio.io/docs/guides/intelligent-routing.html) Refer to Michael README.md ? Difference in delay with Istio.

