
# Install Istio on an existing Kubernetes cluster

Please follow the installation instructions from [istio.io](https://istio.io/docs/setup/kubernetes/quick-start.html).

## Directory structure
Files required for [installing Istio on a Kubernetes cluster](https://github.com/istio/istio/tree/master/install/kubernetes):

* [istio.yaml](https://github.com/istio/istio/blob/master/install/kubernetes/istio.yaml) - Use this file for installation without authentication enabled.
* [istio-auth.yaml](https://github.com/istio/istio/blob/master/install/kubernetes/istio-auth.yaml) - Use this file for installation with authentication enabled.
* [addons](https://github.com/istio/istio/blob/master/install/kubernetes/addons) - Directory contains optional components (Prometheus, Grafana, Service Graph, Zipkin, Zipkin to Stackdriver).

 Additional files to install NGiNX as a sidecar:
 
 * [updateVersion.sh](https://github.com/nginmesh/nginmesh/blob/release-doc-0.2.12/istio/release/updateVersion.sh) Use this file to regenerate Initializer file.
* [istio-initializer.yaml](https://github.com/nginmesh/nginmesh/blob/release-doc-0.2.12/istio/release/install/kubernetes/istio-initializer.yaml) - Use this file for installation of istio initializer for transparent injection.
* [templates](https://github.com/nginmesh/nginmesh/blob/release-doc-0.2.12/istio/release/install/kubernetes/templates) - Directory contains the template used to generate Initializer file.



# Install

1. Make sure alpha enabled kubernetes cluster up and running in Please see requisites for [quick installation](https://istio.io/docs/setup/kubernetes/quick-start.html#prerequisites)

2.  Download Istio release 0.2.12:

```
curl -L https://git.io/getLatestIstio | ISTIO_VERSION=0.2.12 sh -
```

3. Download latest nginmesh repo:
```
git clone https://github.com/nginmesh/nginmesh.git
```

3. Add the istioctl client to your PATH:
```
cd nginmesh
export PATH=$PWD/bin:$PATH
```
4. In Nginmesh repo update version:
```
./nginmesh/istio/updateVersion.sh
```
5. Create Istio deployment without authentication:
```
kubectl create -f install/kubernetes/istio.yaml
```
6. Deploy automatic sidecar injection initializer:
```
kubectl apply -f install/kubernetes/istio-initializer.yaml
```

7. Enable [Zipkin](https://istio.io/docs/tasks/telemetry/distributed-tracing.html#accessing-the-dashboard):
```
kubectl apply -f install/kubernetes/addons/zipkin.yaml
kubectl port-forward -n istio-system $(kubectl get pod -n istio-system -l app=zipkin -o jsonpath='{.items[0].metadata.name}') 9411:9411 &
```
Then open in browser: http://localhost:9411

8. Enable [Graphana](https://istio.io/docs/tasks/telemetry/using-istio-dashboard.html):
```
kubectl apply -f install/kubernetes/addons/grafana.yaml
kubectl -n istio-system port-forward $(kubectl -n istio-system get pod -l app=grafana -o jsonpath='{.items[0].metadata.name}') 3000:3000 &
```
Then open in browser: http://localhost:3000/dashboard/db/istio-dashboard 

9. Enable [Prometheus](https://istio.io/docs/tasks/telemetry/querying-metrics.html):
```
kubectl apply -f install/kubernetes/addons/prometheus.yaml
kubectl -n istio-system port-forward $(kubectl -n istio-system get pod -l app=prometheus -o jsonpath='{.items[0].metadata.name}') 9090:9090 &
```
Then open in browser: http://localhost:9090/graph 

10. Enable [ServiceGraph](https://istio.io/docs/tasks/telemetry/servicegraph.html):
```
kubectl apply -f install/kubernetes/addons/servicegraph.yaml
kubectl -n istio-system port-forward $(kubectl -n istio-system get pod -l app=servicegraph -o jsonpath='{.items[0].metadata.name}') 8088:8088 &
```
Then open in browser:  http://localhost:8088/dotviz

# Verify Install
```
kubectl get pods -n istio-system    #-- Istio pods status
kubectl get svc  -n istio-system      #-- Istio services status
```

# Uninstall
```
kubectl delete -f install/kubernetes/istio.yaml #-- Delete Istio without auth enabled
kubectl delete -f install/kubernetes/istio-auth.yaml #-- Delete Istio without auth enabled
kubectl delete -f install/kubernetes/istio-initializer.yaml #Delete Initializer
kubectl delete -f install/kubernetes/addons/zipkin.yaml #-- Delete Zipkin
kubectl delete -f install/kubernetes/addons/grafana.yaml #-- Delete Graphana
kubectl delete -f install/kubernetes/addons/prometheus.yaml #-- Delete Prometheus
kubectl delete -f install/kubernetes/addons/servicegraph.yaml #Delete ServiceGraph
killall kubectl #-- Remove any kubectl port-forward processes that may be running
```

#  Verify uninstall
```
kubectl get pods -n istio-system #-- Istio pods should be deleted
kubectl get svc  -n istio-system      #-- Istio services should be deleted
```
