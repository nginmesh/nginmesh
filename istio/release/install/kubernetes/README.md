
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

```
1.Create alpha enabled kube cluster:
gcloud container clusters create nginmesh \
--enable-kubernetes-alpha \
--machine-type=n1-standard-2 \
--num-nodes=4 \
--no-enable-legacy-authorization \
--zone=us-central1-a

2 Downloand latest nginmesh repo:
git clone https://github.com/nginmesh/nginmesh.git
3. Add the istioctl client to your PATH:
cd nginmesh
export PATH=$PWD/bin:$PATH

4. In Nginmesh repo update version:
./nginmesh/istio/updateVersion.sh

5. Create Istio deployment without authentication:
kubectl create -f install/kubernetes/istio.yaml

6. Deploy automatic sidecar injection initializer:
kubectl apply -f install/kubernetes/istio-initializer.yaml

7. Enable Zipkin:
kubectl apply -f install/kubernetes/addons/zipkin.yaml
kubectl port-forward -n istio-system $(kubectl get pod -n istio-system -l app=zipkin -o jsonpath='{.items[0].metadata.name}') 9411:9411 &
Then open in browser: http://localhost:9411

8. Enable Graphana:
kubectl apply -f install/kubernetes/addons/grafana.yaml
kubectl -n istio-system port-forward $(kubectl -n istio-system get pod -l app=grafana -o jsonpath='{.items[0].metadata.name}') 3000:3000 &
Then open in browser: http://localhost:3000/dashboard/db/istio-dashboard 

9. Enable Prometheus:
kubectl apply -f install/kubernetes/addons/prometheus.yaml
kubectl -n istio-system port-forward $(kubectl -n istio-system get pod -l app=prometheus -o jsonpath='{.items[0].metadata.name}') 9090:9090 &
Then open in browser: http://localhost:9090/graph 

10. Enable ServiceGraph:
kubectl apply -f install/kubernetes/addons/servicegraph.yaml
kubectl -n istio-system port-forward $(kubectl -n istio-system get pod -l app=servicegraph -o jsonpath='{.items[0].metadata.name}') 8088:8088 &

Then open in browser: http://localhost:8088/dotviz

kubectl create f samples/bookinfo/kube/bookinfo.yaml #-- Deploy Bookinfo Reference application
```
# Verify Install

kubectl get pods -n kube-system   #-- Kube cluster pods status
kubectl get svc -n kube-system     #-- Kube cluster services status
kubectl get pods -n istio-system    #-- Istio pods status
kubectl get svc -n istio-system      #-- Istio services status
kubectl get pods                           #-- Bookinfo pods status check
kubectl get svc -n istio-system     #-- Bookinfo service status check
kubectl get ingress -o wide          #-- Ingress IP and Port
export GATEWAY_URL=104.196.5.186:80 #-- Set Variable to Ingress address
curl -o /dev/null -s w "%{http_code}\n" http://${GATEWAY_URL}/productpage  #-- Check Bookinfo application status
istioctl get routerules                   #-- Check Istio rules list

Open in browser Bookinfo application, make sure successfully run :
http://${GATEWAY_URL}/productpage


# Uninstall
```
./samples/bookinfo/kube/cleanup.sh #-- Delete the routing rules and terminate the application pods
kubectl delete -f install/kubernetes/addons/zipkin.yaml #-- Delete Zipkin
kubectl apply -f install/kubernetes/addons/grafana.yaml #-- Delete Graphana
kubectl apply -f install/kubernetes/addons/prometheus.yaml #-- Delete Prometheus
kubectl delete -f install/kubernetes/addons/servicegraph.yaml #Delete ServiceGraph
killall kubectl #-- Remove any kubectl port-forward processes that may be running
kubectl delete -f install/kubernetes/istio-initializer.yaml #Delete Initializer
kubectl delete -f install/kubernetes/istio.yaml #-- Delete Istio
gcloud container clusters delete nginmesh --zone=us-central1-a #-- Delete Kube cluster in GCP
kubectl config delete-cluster nginmesh #Delete cluster in kubeconfig 
```

#  Verify uninstall
```
istioctl get routerules #-- There should be no more routing rules
kubectl get pods #-- BookInfo pods should be deleted
kubectl get pods -n istio-system #-- Istio pods should be deleted
kubectl get pods -n kube-system #-- Kube pods should be deleted
gcloud container clusters list #-- Kube cluster should be deleted
kubectl config get-contexts #-- Kube cluster config be deleted
```
