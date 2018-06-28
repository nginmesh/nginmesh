# NGINX Architecture with Istio Service Mesh
This repository provides an implementation of a NGINX based service mesh (nginMesh).  nginMesh is compatible with Istio.  It leverages NGINX as a sidecar proxy. 

## What is Service Mesh and Istio?
Please check https://istio.io for a detailed explanation of the service mesh.  

## Production Status
The current version of nginMesh is designed to work with Istio release 0.7.1. It should not be used in production environments.  

## Architecture
The diagram below depicts how an NGINX sidecar proxy is implemented. Sidecar uses the open source version of NGINX compiled with modules for tracing and monitoring.

![Alt text](/images/nginx_sidecar.png?raw=true "NGINX Sidecar")

To learn more about the sidecar implementation, see [this document](istio/agent).

## Quick Start
Below are instructions to quickly install and configure nginMesh.  Currently, only Kubernetes environment is supported.

### Prerequisites
Make sure you have a Kubernetes cluster with at least 1.9 or greater due to fact only automatic sidecar injection is supported and no alpha feature is enabled. Please see [Prerequisites](https://istio.io/docs/setup/kubernetes/quick-start.html) for setting up a kubernetes cluster.

### Install Istio and nginMesh
nginMesh requires installation of Istio first.

1. Download and install Istio 0.7.1:
```
curl -L https://git.io/getLatestIstio | ISTIO_VERSION=0.7.1 sh -
```
2. Download nginMesh release 0.7.1:
```
curl -L https://github.com/nginmesh/nginmesh/releases/download/0.7.1/nginmesh-0.7.1.tar.gz | tar zx
```

3. Deploy Istio between sidecars:
```
kubectl create -f istio-0.7.1/install/kubernetes/istio.yaml
```


4. Ensure the following Kubernetes services are deployed: istio-pilot, istio-mixer, istio-ingress:
```
kubectl get svc  -n istio-system  
```
```
istio-ingress            LoadBalancer   10.47.252.40    35.237.173.47   80:32171/TCP,443:32198/TCP                   19h
istio-mixer              ClusterIP      10.47.251.225   <none>          9091/TCP,15004/TCP,9093/TCP,9094/TCP,9102/TCP,9125/UDP,42422/TCP    19h
istio-pilot              ClusterIP      10.47.254.118   <none>          15003/TCP,15005/TCP,15007/TCP,15010/TCP,8080/TCP,9093/TCP,443/TCP   19h
istio-sidecar-injector   ClusterIP      10.47.242.139   <none>          443/TCP                                       9h
```

5. Ensure the following Kubernetes pods are up and running: istio-pilot-* , istio-mixer-* , istio-ingress-*  and istio-initializer-* :
```
kubectl get pods -n istio-system    
```
```
istio-ca-86f55cc46f-nprhw                1/1       Running   0          19h
istio-ingress-5bb556fcbf-c7tgt           1/1       Running   0          19h
istio-mixer-86f5df6997-fvzjx             3/3       Running   0          19h
istio-pilot-67d6ddbdf6-xhztz             2/2       Running   0          19h
istio-sidecar-injector-5b8c78fd6-8dvq6   1/1       Running   0          9h
```


6. Automatic sidecar:
To set up sidecar injection, please run following script which will install Istio webhook with nginMesh customization.
```
nginmesh-0.7.1/install/kubernetes/install-sidecar.sh
```

7. Verify that istio-injection label is not labeled for the default namespace :
```
kubectl get namespace -L istio-injection
```
```
NAME           STATUS        AGE       ISTIO-INJECTION
default        Active        1h        
istio-system   Active        1h        
kube-public    Active        1h        
kube-system    Active        1h
```

### Install Zipkin
1. Install Zipkin:
```
kubectl apply -f istio-0.7.1/install/kubernetes/addons/zipkin.yaml
```

2. Activate port-forward for Zipkin and open [dashboard](http://localhost:9411):
```
kubectl port-forward -n istio-system $(kubectl get pod -n istio-system -l app=zipkin -o jsonpath='{.items[0].metadata.name}') 9411:9411 &
```



### Deploy a Sample Application
In this section we deploy the Bookinfo application, which is taken from the Istio samples. Please see [Bookinfo](https://istio.io/docs/guides/bookinfo.html)  for more details.

1. Label the default namespace with istio-injection=enabled:

```
kubectl label namespace default istio-injection=enabled
```

2. Deploy the application:

```
kubectl apply -f  istio-0.7.1/samples/bookinfo/kube/bookinfo.yaml
```

3. Confirm that all application services are deployed: productpage, details, reviews, ratings:

```
kubectl get services
```
```
NAME                       CLUSTER-IP   EXTERNAL-IP   PORT(S)              AGE
details                    10.0.0.31    <none>        9080/TCP             6m
kubernetes                 10.0.0.1     <none>        443/TCP              7d
productpage                10.0.0.120   <none>        9080/TCP             6m
ratings                    10.0.0.15    <none>        9080/TCP             6m
reviews                    10.0.0.170   <none>        9080/TCP             6m
```

4. Confirm that all application pods are running --details-v1-* , productpage-v1-* , ratings-v1-* , reviews-v1-* , reviews-v2-* and reviews-v3-* :
```
kubectl get pods
```
```
NAME                                        READY     STATUS    RESTARTS   AGE
details-v1-1520924117-48z17                 2/2       Running   0          6m
productpage-v1-560495357-jk1lz              2/2       Running   0          6m
ratings-v1-734492171-rnr5l                  2/2       Running   0          6m
reviews-v1-874083890-f0qf0                  2/2       Running   0          6m
reviews-v2-1343845940-b34q5                 2/2       Running   0          6m
reviews-v3-1813607990-8ch52                 2/2       Running   0          6m
```

5. Get the public IP of the Istio Ingress controller. If the cluster is running in an environment that supports external load balancers:

```
kubectl get svc -n istio-system | grep -E 'EXTERNAL-IP|istio-ingress'
```

OR

```
kubectl get ingress -o wide       
```

6. Open the Bookinfo application in a browser using the following link:
```
http://<Public-IP-of-the-Ingress-Controller>/productpage
```

Note 1: For E2E routing rules and performace testing you could refer to [E2E Test](istio/tests/README.md).
Note 2: Alternatively, you could install NGINX MRA Application, refer to [Ingenious](istio/release/samples/ingenious/kube/README.md).


### Uninstall the Application
1. To uninstall application, run:

```
./istio-0.7.1/samples/bookinfo/kube/cleanup.sh
```

### Uninstall Istio
1. To uninstall the Istio core components:

```
kubectl delete -f istio-0.7.1/install/kubernetes/istio.yaml
```


2. To uninstall the initializer, run:

```
nginmesh-0.7.1/install/kubernetes/delete-sidecar.sh
```
### Uninstall Zipkin
1. Uninstall Zipkin:
```
kubectl delete -f istio-0.7.1/install/kubernetes/addons/zipkin.yaml
```
2. Deactivate port-forward:
```
ps -ef | grep zipkin | grep -v grep | awk '{print $2}' | xargs kill -9 
```

## Limitations
nginMesh has the following limitations:
* TCP and gRPC traffic is not supported.
* Quota Check is not supported.
* Only Kubernetes is supported.

All sidecar-related limitations and supported traffic management rules are described [here](istio/agent).
