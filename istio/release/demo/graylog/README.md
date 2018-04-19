# Graylog deployment

Graylog is a powerful log management and analysis tool that has many use cases, from monitoring to debugging applications.

It has 3 main components:

**Server nodes:** Serves as a worker that receives and processes messages, and communicates with all other non-server components. Its performance is CPU dependent.

**Elasticsearch nodes:** Stores all of the logs/messages. Its performance is RAM and disk I/O dependent.

**MongoDB:** Stores metadata and does not experience much load.

## Architecture

![Alt text](images/graylog.png?raw=true "Graylog Architecture") 

Please, check [link](http://docs.graylog.org/en/2.4/) for documentation.

## Quick Start
1.Make sure below requirements are met:
  
  | Version | Name | Details |
  | --- | ------ | ------ |
  |1.9|Kubernetes cluster|Without alpha feature, [link](https://istio.io/docs/setup/kubernetes/quick-start.html#google-kubernetes-engine)|
  |0.6.0|Istio|[link](https://istio.io/docs/setup/kubernetes/quick-start.html)|
  |0.6.0|nginMesh|[link](https://github.com/nginmesh/nginmesh/blob/master/README.md)|
  |1.5.0|Bookinfo Application|[link](https://github.com/istio/istio/blob/master/samples/bookinfo/src)|
  |1.1.0|Kafka|[link](https://kafka.apache.org/downloadsc)|


2. Install graylog deployment in graylog namespace:
```
 kubectl create -f nginmesh-0.7.1/demo/graylog/graylog.yaml
```
3. Make sure following pods are up and running:

```
kubectl get pods -n graylog
```
```
NAME                            READY     STATUS    RESTARTS   AGE
elasticsearch-97c476698-7tmpd   1/1       Running   0          1m
graylog-c4d976795-vfhpf         1/1       Running   0          1m
mongo-6bb464754d-d6fd8          1/1       Running   0          1m
```

4. Make sure following services are up and running: 
```
kubectl get svc -n graylog
```
```
NAME            TYPE           CLUSTER-IP     EXTERNAL-IP       PORT(S)                          AGE
elasticsearch   ClusterIP      None           <none>            55555/TCP                        2m
graylog         LoadBalancer   10.55.242.76   100.100.100.100   9000:31927/TCP,12201:30371/TCP   2m
mongo           ClusterIP      None           <none>            55555/TCP                        2m

```

5. Activate port-forwarding for running graylog pod:
```
kubectl port-forward graylog-c4d976795-vfhpf -n graylog 9000:9000
```

6. Access to Graylog Dashboard from browser:

```
http://127.0.0.1:9000/
```
Note: Check graylog deployment file for username/password passed as environment variable. 

7. Add Raw/Plaintext type Kafka input:

![Alt text](images/input_conf.png?raw=true "Input Conf")

8. Generate requests towards sample application deployed and check:

![Alt text](images/search.png?raw=true "Search ")

9. Add JSON type extractor to input:

![Alt text](images/extractor_conf.png?raw=true "Extractor Conf")

10. Add to dahboard required metrics:

![Alt text](images/dashboard.png?raw=true "Dashboard")
