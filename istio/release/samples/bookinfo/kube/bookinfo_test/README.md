### Prerequisites

Make sure you meet below requirements:

```2.7``` python is installed.

```+0.3.0``` Latest python grequests library installed.
 
```+v2.18.4``` Latest python requests library installed.

```+1.9``` Kubernetes cluster with alpha feature disabled is up and running.

```0.6.0``` Istio is installed.

```0.6.0``` nginMesh is installed.

Istio Bookinfo Sample application is deployed.

Mamba behavior-driven test runner is installed. For details,[link](https://github.com/nestorsalceda/mamba).


wrk HTTP benchmarking tool is installed. For details,[link](https://github.com/wg/wrk).

kubectl Command line interface tool for Kubernetes clusters is installed. For details,[link](https://kubernetes.io/docs/tasks/tools/install-kubectl/).




### Run Test 
nginMesh requires installation of Istio first.

1. Change directory to bookinf_testt:
```
cd nginmesh-0.6.0/samples/bookinfo/kube/bookinfo_test
```
2. Run all spec tests for sample application :
```
mamba --format documentation .
```

Note: It is also possible, to run test cases independently, by specifiying name of test case instead of "." sign.
