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
mamba --format documentation .
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
 | V1 Hit=3 | V2 Hit=4 | V3 Hit=3 | Total Hit=10 |
  73 requests in 1.01s, 389.22KB read
Requests/sec:     72.24
Transfer/sec:    385.14KB
    ✓ it Bookinfo Basic Functionality test without rules (1.4009 seconds)

nginmesh Test 02
  Set environment
    ✓ it Bookinfo add Routing Rule (5.6201 seconds)
  Starting Test
 | V1 Hit=10 | V2 Hit=0 | V3 Hit=0 | Total Hit=10 |
  61 requests in 1.01s, 273.04KB read
Requests/sec:     60.20
Transfer/sec:    269.44KB
    ✓ it Bookinfo route all requests to V1 (1.3265 seconds)
  Clean Environment
    ✓ it Bookinfo delete Routing Rule (0.4897 seconds)

nginmesh Test 03
  Set environment
    ✓ it Bookinfo add Routing Rule (5.4418 seconds)
  Starting Test
 | V1 Hit=0 | V2 Hit=0 | V3 Hit=10 | Total Hit=10 |
  43 requests in 1.02s, 247.24KB read
Requests/sec:     42.02
Transfer/sec:    241.61KB
    ✓ it Bookinfo route all requests to V3 (1.3857 seconds)
  Clean Environment
    ✓ it Bookinfo delete Routing Rule (0.3197 seconds)

nginmesh Test 04
  Set environment
    ✓ it Bookinfo add Routing Rule (5.4277 seconds)
  Starting Test
 | V1 Hit=4 | V2 Hit=0 | V3 Hit=6 | Total Hit=10 |
  56 requests in 1.02s, 290.14KB read
Requests/sec:     55.02
Transfer/sec:    285.07KB
    ✓ it Bookinfo route all requests to V1 and V3 (1.3554 seconds)
  Clean Environment
    ✓ it Bookinfo delete Routing Rule (0.3163 seconds)

nginmesh Test 05
  Set environment
    ✓ it Bookinfo add Routing Rule (10.4325 seconds)
  Starting Test
 | V1 Hit=6 | V2 Hit=4 | V3 Hit=0 | Total Hit=10 |
  69 requests in 1.01s, 329.27KB read
Requests/sec:     68.02
Transfer/sec:    324.59KB
    ✓ it Bookinfo destination-weight test, route to V1-75%, V2-25% (1.3306 seconds)
  Clean Environment
    ✓ it Bookinfo delete Routing Rule (0.3108 seconds)

nginmesh Test 06
  Set environment
    ✓ it Bookinfo add Routing Rule (5.4312 seconds)
  Starting Test
 | V1 Hit=0 | V2 Hit=6 | V3 Hit=4 | Total Hit=10 |
  50 requests in 1.02s, 287.58KB read
Requests/sec:     49.24
Transfer/sec:    283.23KB
    ✓ it Bookinfo route all requests to V2 and V3 (1.3572 seconds)
  Clean Environment
    ✓ it Bookinfo delete Routing Rule (0.3078 seconds)

nginmesh Test 07
  Set environment
    ✓ it Bookinfo add Routing Rule (10.4294 seconds)
  Starting Test
  171 requests in 1.03s, 24.38KB read
Requests/sec:    166.80
Transfer/sec:     23.78KB
    ✓ it Bookinfo HTTP Redirect (2.1790 seconds)
  Clean Environment
    ✓ it Bookinfo delete Routing Rule (0.3294 seconds)

nginmesh Test 08
  Set environment
    ✓ it Bookinfo add Routing Rule (10.4303 seconds)
  Starting Test
Total Retry Hit=10
  59 requests in 1.01s, 339.23KB read
Requests/sec:     58.23
Transfer/sec:    334.78KB
    ✓ it Bookinfo HTTP Retry (15.6707 seconds)
  Clean Environment
    ✓ it Bookinfo delete Routing Rule (0.3163 seconds)

nginmesh Test 09
  Set environment
    ✓ it Bookinfo add Routing Rule (5.4297 seconds)
  Starting Test
 | V1 Hit=0 | V2 Hit=10 | V3 Hit=0 | Total Hit=10 |
    ✓ it Bookinfo route "jason" User to V2 (1.4443 seconds)
  Clean Environment
    ✓ it Bookinfo delete Routing Rule (0.3238 seconds)

25 examples ran in 102.7347 seconds
```
4. To run selectively, please input one or multiple test cases:
```
mamba --format documentation 1_bd_spec.py 2_route_all_v1_spec.py

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