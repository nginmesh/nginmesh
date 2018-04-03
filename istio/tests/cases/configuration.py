import subprocess
import grequests
VERSION='0.6.0'

def setenv(self):
    self.GATEWAY_URL = str(subprocess.check_output("kubectl get svc -n istio-system | grep -E 'istio-ingress' | awk '{ print $4 }'", universal_newlines=True,shell=True)).rstrip()
    self.url = "http://"+self.GATEWAY_URL+"/productpage"
   # self.zipkin="http://localhost:9412/api/v2/services"
   # self.prometheus="http://localhost:9090/api/v1/query?query=http_requests_total"
   # self.servicegraph="http://localhost:8088/graph"
   # self.grafana="http://localhost:3000/api/dashboards/db/istio-dashboard"
    self.VERSION='0.6.0'
    self.performance='on'
    self.install_istio='on'
    self.deploy_bookinfo_app='on'
    self.v1_count=0
    self.v2_count=0
    self.v3_count=0
    self.total_count = 0
    return self.performance,self.GATEWAY_URL,self.v1_count,self.v2_count,self.v3_count,self.total_count,self.VERSION

class Istio:
    def install_istio(self):
         subprocess.call("kubectl apply -f ../../release/samples/bookinfo/kube/istio.yaml > /dev/null 2>&1 | exit 0",universal_newlines=True,shell=True)
    def uninstall_istio(self):
             subprocess.call("kubectl apply -f ../../release/samples/bookinfo/kube/istio.yaml > /dev/null 2>&1 | exit 0",universal_newlines=True,shell=True)

class Bookinfo:
    def deploy_bookinfo(self):
         subprocess.call("kubectl apply -f ../../release/samples/bookinfo/kube/bookinfo.yaml > /dev/null 2>&1 | exit 0",universal_newlines=True,shell=True)
    def clean_bookinfo(self):
             subprocess.call("../../release/samples/bookinfo/kube/cleanup.sh > /dev/null 2>&1 | exit 0",universal_newlines=True,shell=True)

def generate_request(self):
    self.v1_count=0
    self.v2_count=0
    self.v3_count=0
    self.total_count = 0
    urls = [self.url for i in range(10)]
    rs = (grequests.get(self.url) for url in urls)
    results = grequests.map(rs)
    for r in results:
        if r.status_code==200 and 'color="black"' not in r.text and 'color="red"' not in r.text:
           self.total_count += 1
           self.v1_count+=1
        elif r.status_code==200 and 'color="black"' in r.text:
           self.total_count += 1
           self.v2_count+=1
        elif r.status_code==200 and 'color="red"' in r.text:
           self.total_count += 1
           self.v3_count+=1
        else:
           self.total_count += 1
    print(" | V1 Hit="+str(self.v1_count)+" | V2 Hit="+str(self.v2_count)+" | V3 Hit="+str(self.v3_count)+" | Total Hit="+str(self.total_count)+ " |")
    return self.GATEWAY_URL,self.v1_count,self.v2_count,self.v3_count,self.total_count,self.VERSION, self.performance


class Rule:
     def add(self,rule_name):
         subprocess.call("kubectl create -f ../../release/samples/bookinfo/kube/"+rule_name+" > /dev/null 2>&1 | exit 0",universal_newlines=True,shell=True)

     def delete(self,rule_name):
         subprocess.call("kubectl delete -f ../../release/samples/bookinfo/kube/"+rule_name+" > /dev/null 2>&1 | exit 0",universal_newlines=True,shell=True)
     def delete_all(self):
              subprocess.call("kubectl delete routerules --all > /dev/null 2>&1 | exit 0",universal_newlines=True,shell=True)



'''
# Using Request module in Python
while self.total_count < 10:
    r = requests.get(self.url)
    r.status_code
    expect(r.status_code).to(equal(200))
    if 'color="black"' not in r.text and 'color="red"' not in r.text:
  #      print("V1 'is' here!")
        self.total_count += 1
        self.v1_count+=1
    elif 'color="black"' in r.text:
  #      print("V2 Black 'is' here!")
        self.total_count += 1
        self.v2_count+=1
    elif 'color="red"' in r.text:
 #       print("V3 Red 'is' here!")
        self.total_count += 1
        self.v3_count+=1
    else:
 #       print("App does not work!")
         self.total_count += 1
 '''


