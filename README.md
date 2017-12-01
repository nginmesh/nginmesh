
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
 

### Prerequisities 

Make sure you have  kubernetes cluster with alpha fearture enabled. Please, refer [Prerequisites](https://istio.io/docs/setup/kubernetes/quick-start.html#prerequisites) to Istio project for setting up cluster for your environment.

#### Installation Istio and Nginmesh
Below are instructions for installing Istio with NGiNX as a sidecar in application pods.

1.  Download Istio release 0.2.12:

```
curl -L https://git.io/getLatestIstio | ISTIO_VERSION=0.2.12 sh -
```

2. Download Nginmesh release 0.2.12:
```
curl -L https://github.com/nginmesh/nginmesh/releases/tag/0.2.12-RC2
```

3. Create Istio deployment without authentication:
```
kubectl create -f install/kubernetes/istio.yaml
```
4. Deploy automatic sidecar injection initializer:
```
kubectl apply -f install/kubernetes/istio-initializer.yaml
```

5. Ensure the corresponding Kubernetes pods are deployed and all containers are up and running: istio-pilot-*, istio-mixer-*, istio-ingress-*, istio-egress-* and istio-initializer-*.
```
kubectl get pods -n istio-system    #-- Istio pods status
kubectl get svc  -n istio-system      #-- Istio services status
```

#### Deploy Application
The sample app is copied from Istio project without modification. Please, refer to [Bookinfo](https://istio.io/docs/guides/bookinfo.html) for more details.  

Note: We only support deployment using Kubernetes initializer. 

1. Change directory to the root of the Nginmesh installation directory

2. Deploy the application containers:

```
kubectl apply -f samples/bookinfo/kube/bookinfo.yaml
```

3. Confirm all services and pods are correctly defined and running: details-v1-*, productpage-v1-*, ratings-v1-*, ratings-v1-*, reviews-v1-*, reviews-v2-*, reviews-v3-*.

```
kubectl get pods
kubectl get services
```

4. If cluster is running in an environment that supports external load balancers, the IP address of ingress can be obtained by the following command:
```
kubectl get ingress -o wide          #-- Ingress IP and Port
```
5. Set Variable to Ingress address obtained in Step 4:
```
export GATEWAY_URL=104.196.5.186:80
```
6. To confirm that the BookInfo application is running:

a) Run the following curl command and check received response code:

```
curl -o /dev/null -s -w "%{http_code}\n" http://${GATEWAY_URL}/productpage
```

OR:

b) Open in browser Bookinfo application, make sure successfully running :
```
http://${GATEWAY_URL}/productpage
```
#### Cleanup Application

1. Uninstall from Kubernetes environment:
```
./samples/bookinfo/kube/cleanup.sh 
```

2. Verify cleanup:
```
kubectl get pods #-- Application pods should be deleted
kubectl get svc  #-- Application services should be deleted
```

#### Cleanup Istio

1. Uninstall from Kubernetes environment:
```
kubectl delete -f install/kubernetes/istio.yaml #-- Delete Istio without auth enabled
kubectl delete -f install/kubernetes/istio-auth.yaml #-- Delete Istio without auth enabled
kubectl delete -f install/kubernetes/istio-initializer.yaml #-- Delete Initializer
```

2. Verify cleanup:
```
kubectl get pods -n istio-system #-- Istio pods should be deleted
kubectl get svc  -n istio-system #-- Istio services should be deleted
kubectl get pods #-- Application pods should be deleted
kubectl get svc  #-- Application services should be deleted
```

#### Optional: 

[In-Depth Telemetry](https://istio.io/docs/guides/telemetry.html) This sample demonstrates how to obtain uniform metrics, logs, traces across different services using NGiNX sidecar.

[Intelligent Routing](https://istio.io/docs/guides/intelligent-routing.html) Refer to Michael README.md ? Difference in delay with Istio.


