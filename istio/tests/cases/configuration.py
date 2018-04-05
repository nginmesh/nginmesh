import subprocess
import grequests
import performance
import time
VERSION='0.6.0'
rule_apply_time=5
# istio_path="../../release/samples/bookinfo/kube/"
istio_path="nginmesh-0.6.0/samples/bookinfo/kube/"

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

def generate_request(self, rule_name=None):
    self.v1_count=0
    self.v2_count=0
    self.v3_count=0
    self.total_count = 0
    if rule_name !="route-rule-reviews-test-v2.yaml" and rule_name !="route-rule-http-redirect.yaml" and rule_name !="route-rule-http-retry.yaml" :
        urls = [self.url for i in range(10)]
        rs = (grequests.get(self.url,allow_redirects=False) for url in urls)
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
    else:
        pass

    if self.performance=='on':
        print performance.wrecker(self.GATEWAY_URL)
    else:
        pass

    return self.GATEWAY_URL,self.v1_count,self.v2_count,self.v3_count,self.total_count,self.VERSION, self.performance


class Rule:
     def add(self,rule_name):
         subprocess.call("kubectl create -f "+istio_path+rule_name+" > /dev/null 2>&1 | exit 0",universal_newlines=True,shell=True)
         time.sleep(rule_apply_time)

     def delete(self,rule_name):
         subprocess.call("kubectl delete -f "+istio_path+rule_name+" > /dev/null 2>&1 | exit 0",universal_newlines=True,shell=True)
     def delete_all(self):
              subprocess.call("kubectl delete routerules --all > /dev/null 2>&1 | exit 0",universal_newlines=True,shell=True)




