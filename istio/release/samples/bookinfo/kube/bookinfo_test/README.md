### Prerequisites

Make sure you meet below requirements:

```2.7``` python is installed.

```0.3.0``` Latest python grequests library is installed.
 
```2.18.4``` Latest python requests library is installed.

```0.8.0``` Latest python expects library is installed.

```0.1.0``` Latest python args  library is installed.
Note: You can use ```pip``` package manager to install upper listed libraries:

```
pip install grequests requests expects args
```
```1.9``` Kubernetes cluster with alpha feature disabled is up and running.

```0.6.0``` Istio is installed.

```0.6.0``` nginMesh is installed.

```1.5.0``` Istio Bookinfo Sample application is deployed.

```0.9.2``` Mamba behavior-driven test runner is installed. For details, [link](https://github.com/nestorsalceda/mamba).


```4.1.0``` wrk HTTP benchmarking tool is installed. For details, [link](https://github.com/wg/wrk).

```1.10.0``` Kubectl Command line interface tool for Kubernetes clusters is installed. For details, [link](https://kubernetes.io/docs/tasks/tools/install-kubectl/).




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
