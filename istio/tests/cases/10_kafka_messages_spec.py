import requests,time
import configuration
import performance
from mamba import description, context, it
from expects import expect, equal
import multiprocessing as mp

kafka_mock_hdr = {'content-type': 'MOCK_CONTENT_TYPE','User-Agent':'MOCK_UserAgent',"x-b3-spanid":"bbbbbbbbbbbbbbbb","x-b3-traceid":"aaaaaaaaaaaaaaaa","x-request-id":"MOCK_REQ_ID"}
kafka_check_values=('request_id','user_agent','req_path','response_code','response_duration','source_uid','content_type','trace_id','span_id')
kafka_mp_output = mp.Queue()

def generate_kafka_mock_request():
    x=0
    while x<configuration.kafka_req_count:
        r = requests.get("http://"+configuration.GATEWAY_URL+"/productpage", headers=kafka_mock_hdr )
        expect(r.status_code).to(equal(200))
        expect(int(r.elapsed.total_seconds())).to(equal(0))
        x+=1

def check_kafka_logs(self,out):
                out=configuration.run_shell("kubectl -n "+configuration.kafka_ns+" exec "+configuration.kafka_client_pod_name+" -- /usr/bin/kafka-console-consumer --topic "+configuration.kafka_topic+"  --bootstrap-server "+configuration.kafka_srv_svc+" --max-messages 10 ","check")
                request_id=0
                user_agent=0
                req_path=0
                response_code=0
                response_duration=0
                source_uid=0
                content_type=0
                trace_id=0
                span_id=0

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

with description('Testing Kafka messages'):
    with before.all:
         #Read Config file
         configuration.setenv(self)
         configuration.generate_request(self)

with context('Starting test'):
    with it('Testing Kafka functionality'):

        proc_a = mp.Process(target=check_kafka_logs,args=(self,kafka_mp_output))
        proc_b = mp.Process(target=generate_kafka_mock_request)
        proc_a.start()
        proc_b.start()
        proc_a.join()
        proc_b.join()
        result=kafka_mp_output.get()
        for i in range(0,len(result)):
            try:
                expect(result[i]).to(equal(1))
            except:
                raise Exception(kafka_check_values[i]+" is not found")








       





