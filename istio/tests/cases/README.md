### Prerequisites

Make sure below requirements are met:

| Version | Name | Details |
| --- | ------ | ------ |
|1.9|Kubernetes cluster|Without alpha feature, [link](https://istio.io/docs/setup/kubernetes/quick-start.html#google-kubernetes-engine)|
|0.6.0|Istio|[link](https://istio.io/docs/setup/kubernetes/quick-start.html)|
|0.6.0|nginMesh|[link](https://github.com/nginmesh/nginmesh/blob/master/README.md)|
|1.5.0|Bookinfo Application|[link](https://github.com/istio/istio/blob/master/samples/bookinfo/src)|
|0.9.2|Mamba|[link](https://github.com/nestorsalceda/mamba)|
|4.1.0|Wrecker|[link](https://github.com/wg/wrk)|
|2.7|Python|[link](https://www.python.org)|
|1.10.0|Kubectl|[link](https://kubernetes.io/docs/tasks/tools/install-kubectl/)|

### Run Test 
1. Change directory to /cases directory in nginMesh repo:
```
cd tests/cases
```
2. Install python dependencies in virtual environment:
```
./install.sh
```
3. Run all spec tests for Bookinfo application:

```
pipenv run mamba --format documentation .
```
```
               _                           _
   _ __   __ _(_)_ __  _ __ ___   ___  ___| |__
  | `_ \ / _  | |  _ \|  _   _ \ / _ \/ __| |_ \
  | | | | (_| | | | | | | | | | |  __/\__ \ | | |
  |_| |_|\__, |_|_| |_|_| |_| |_|\___||___/_| |_|
         |___/

nginmesh Test 01
  Starting Test
 | V1 Hit=3 | V2 Hit=3 | V3 Hit=4 | Total Hit=10 |
  58 requests in 1.01s, 308.07KB read
Requests/sec:     57.28
Transfer/sec:    304.27KB
    ✓ it Bookinfo Basic Functionality test without rules (1.4192 seconds)

nginmesh Test 02
  Set environment
    ✓ it Bookinfo add Routing Rule (5.5916 seconds)
  Starting Test
 | V1 Hit=10 | V2 Hit=0 | V3 Hit=0 | Total Hit=10 |
  63 requests in 1.01s, 281.98KB read
Requests/sec:     62.17
Transfer/sec:    278.26KB
    ✓ it Bookinfo route all requests to V1 (1.3774 seconds)
  Clean Environment
    ✓ it Bookinfo delete Routing Rule (0.4968 seconds)

nginmesh Test 03
  Set environment
    ✓ it Bookinfo add Routing Rule (5.4144 seconds)
  Starting Test
 | V1 Hit=0 | V2 Hit=0 | V3 Hit=10 | Total Hit=10 |
  53 requests in 1.01s, 304.73KB read
Requests/sec:     52.30
Transfer/sec:    300.73KB
    ✓ it Bookinfo route all requests to V3 (1.3497 seconds)
  Clean Environment
    ✓ it Bookinfo delete Routing Rule (0.3102 seconds)

nginmesh Test 04
  Set environment
    ✓ it Bookinfo add Routing Rule (5.4183 seconds)
  Starting Test
 | V1 Hit=5 | V2 Hit=0 | V3 Hit=5 | Total Hit=10 |
  56 requests in 1.01s, 283.77KB read
Requests/sec:     55.28
Transfer/sec:    280.14KB
    ✓ it Bookinfo route all requests to V1 and V3 (1.3487 seconds)
  Clean Environment
    ✓ it Bookinfo delete Routing Rule (0.3179 seconds)

nginmesh Test 05
  Set environment
    ✓ it Bookinfo add Routing Rule (5.4257 seconds)
  Starting Test
 | V1 Hit=8 | V2 Hit=2 | V3 Hit=0 | Total Hit=10 |
  46 requests in 1.01s, 222.51KB read
Requests/sec:     45.33
Transfer/sec:    219.28KB
    ✓ it Bookinfo destination-weight test, route to V1-75%, V2-25% (1.3857 seconds)
  Clean Environment
    ✓ it Bookinfo delete Routing Rule (0.3212 seconds)

nginmesh Test 06
  Set environment
    ✓ it Bookinfo add Routing Rule (5.4258 seconds)
  Starting Test
 | V1 Hit=0 | V2 Hit=2 | V3 Hit=8 | Total Hit=10 |
  44 requests in 1.02s, 253.08KB read
Requests/sec:     43.27
Transfer/sec:    248.91KB
    ✓ it Bookinfo route all requests to V2 and V3 (1.3858 seconds)
  Clean Environment
    ✓ it Bookinfo delete Routing Rule (0.3415 seconds)

nginmesh Test 07
  Set environment
    ✓ it Bookinfo add Routing Rule (5.4394 seconds)
  Starting Test
  180 requests in 1.01s, 25.49KB read
Requests/sec:    178.27
Transfer/sec:     25.24KB
    ✓ it Bookinfo HTTP Redirect (2.1643 seconds)
  Clean Environment
    ✓ it Bookinfo delete Routing Rule (0.3151 seconds)

nginmesh Test 08
  Set environment
    ✓ it Bookinfo add Routing Rule (5.4263 seconds)
  Starting Test
Total Retry Hit=10
  67 requests in 1.01s, 385.20KB read
Requests/sec:     66.16
Transfer/sec:    380.40KB
    ✓ it Bookinfo HTTP Retry (16.0472 seconds)
  Clean Environment
    ✓ it Bookinfo delete Routing Rule (0.3148 seconds)

nginmesh Test 09
  Set environment
    ✓ it Bookinfo add Routing Rule (5.4206 seconds)
  Starting Test
 | V1 Hit=0 | V2 Hit=10 | V3 Hit=0 | Total Hit=10 |
  47 requests in 1.01s, 249.91KB read
Requests/sec:     46.36
Transfer/sec:    246.53KB
    ✓ it Bookinfo route "jason" User to V2 (2.5943 seconds)
  Clean Environment
    ✓ it Bookinfo delete Routing Rule (0.3134 seconds)

25 examples ran in 86.5055 seconds
```
4. To run selectively, please input one or multiple test cases:
```
pipenv run mamba --format documentation 1_bd_spec.py 2_route_all_v1_spec.py

```
```
nginmesh Test 01
  Starting Test
 | V1 Hit=3 | V2 Hit=4 | V3 Hit=3 | Total Hit=10 |
  73 requests in 1.01s, 387.94KB read
Requests/sec:     71.94
Transfer/sec:    382.29KB
    ✓ it Bookinfo Basic Functionality test without rules (1.3446 seconds)

nginmesh Test 02
  Set environment
    ✓ it Bookinfo add Routing Rule (5.6114 seconds)
  Starting Test
 | V1 Hit=10 | V2 Hit=0 | V3 Hit=0 | Total Hit=10 |
  60 requests in 1.02s, 268.56KB read
Requests/sec:     58.96
Transfer/sec:    263.92KB
    ✓ it Bookinfo route all requests to V1 (1.3744 seconds)
  Clean Environment
    ✓ it Bookinfo delete Routing Rule (0.4852 seconds)

4 examples ran in 10.9609 seconds
```