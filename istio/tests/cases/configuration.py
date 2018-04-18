import subprocess
import grequests
import requests
import performance
import time
import os
import multiprocessing as mp
from expects import expect, equal

rule_apply_time=5
nginmesh_rule_path="../../release/samples/bookinfo/kube/"
nginmesh_install_path="../../release/install/"
count_init=0
request_count=10
performance_status='on'
performance_thread='1'
performance_connection='10'
performance_duration='1s'
app_namespace=os.environ.get('app_namespace','default')

# Kafka test dependencies
kafka_topic="nginmesh"
kafka_mp_output = mp.Queue()
kafka_ns="kafka"
kafka_client_pod_name="testclient"
kafka_srv_svc="my-kafka-kafka:9092"
kafka_req_count=40
kafka_mock_hdr = {'content-type': 'MOCK_CONTENT_TYPE','User-Agent':'MOCK_UserAgent',"x-b3-spanid":"bbbbbbbbbbbbbbbb","x-b3-traceid":"aaaaaaaaaaaaaaaa","x-request-id":"MOCK_REQ_ID"}
kafka_check_values=('request_id','user_agent','req_path','response_code','response_duration','source_uid','content_type','trace_id','span_id')

def run_shell(self,type):
    if type=="check":
        return str(subprocess.check_output(self, universal_newlines=True,shell=True)).rstrip()
    elif type=="run":
        subprocess.call(self+" > /dev/null 2>&1 | exit 0",universal_newlines=True,shell=True)
        time.sleep(rule_apply_time)
        return

GATEWAY_URL =run_shell("kubectl get svc -n istio-system | grep -E 'istio-ingress' | awk '{ print $4 }'","check")

def setenv(self):
    self.url = "http://"+GATEWAY_URL+"/productpage"
    self.zipkin="http://localhost:9411/api/v2/services"
    self.performance=performance_status
    self.v1_count=count_init
    self.v2_count=count_init
    self.v3_count=count_init
    self.total_count=count_init
    self.request_count=request_count
    return self.performance,self.v1_count,self.v2_count,self.v3_count,self.request_count,self.total_count

def generate_kafka_mock_request():
    x=count_init
    while x<kafka_req_count:
        r = requests.get("http://"+GATEWAY_URL+"/productpage", headers=kafka_mock_hdr )
        expect(r.status_code).to(equal(200))
        expect(int(r.elapsed.total_seconds())).to(equal(0))
        x+=1

def check_kafka_logs(self,out):
                out=run_shell("kubectl -n "+kafka_ns+" exec "+kafka_client_pod_name+" -- /usr/bin/kafka-console-consumer --topic "+kafka_topic+"  --bootstrap-server "+kafka_srv_svc+" --max-messages 10 ","check")
                request_id=count_init
                user_agent=count_init
                req_path=count_init
                response_code=count_init
                response_duration=count_init
                source_uid=count_init
                content_type=count_init
                trace_id=count_init
                span_id=count_init

                if kafka_mock_hdr.get('x-request-id') in out:
                    request_id+=1
                if kafka_mock_hdr.get('User-Agent') in out:
                    user_agent+=1
                if kafka_mock_hdr.get('content-type') in out:
                    content_type+=1
                if kafka_mock_hdr.get('x-b3-traceid') in out:
                    trace_id+=1
                if kafka_mock_hdr.get('x-b3-spanid') in out:
                    span_id+=1
                if  'request_path' in out:
                    req_path+=1
                if 'response_code' in out:
                    response_code+=1
                if 'response_duration' in out:
                    response_duration+=1
                if 'source_uid' in out:
                    source_uid+=1
             #   print(out)
                kafka_mp_output.put((request_id,user_agent,req_path,response_code,response_duration,source_uid,content_type,trace_id,span_id))


def generate_request(self, rule_name=None):
    if rule_name !="route-rule-reviews-test-v2.yaml" and rule_name !="route-rule-http-redirect.yaml" and rule_name !="route-rule-http-retry.yaml" :
        urls = [self.url for i in range(self.request_count)]
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
        print performance.wrecker(GATEWAY_URL,performance_thread,performance_connection,performance_duration)
    else:
        pass

class Rule:
     def add(self,rule_name):
         run_shell("kubectl create -f "+nginmesh_rule_path+rule_name+" -n"+app_namespace,"run")
     def delete(self,rule_name):
         run_shell("kubectl delete -f "+nginmesh_rule_path+rule_name+" -n"+app_namespace,"run")





