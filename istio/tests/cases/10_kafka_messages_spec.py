import requests,time
import configuration
import performance
from mamba import description, context, it
from expects import expect, equal,contain,have_key
import multiprocessing as mp

kafka_mock_hdr = {'content-type': 'MOCK_CONTENT_TYPE','User-Agent':'MOCK_UserAgent',"x-b3-spanid":"bbbbbbbbbbbbbbbb","x-b3-traceid":"aaaaaaaaaaaaaaaa","x-request-id":"MOCK_REQ_ID"}
kafka_mp_output = mp.Queue()

def generate_kafka_mock_request():
    x=0
    while x<configuration.kafka_req_count:
        r = requests.get("http://"+configuration.GATEWAY_URL+"/productpage", headers=kafka_mock_hdr )
        expect(r.status_code).to(equal(200))
        expect(int(r.elapsed.total_seconds())).to(equal(0))
        x+=1

def check_kafka_logs(self,out):
                out=configuration.run_shell("kubectl -n "+configuration.kafka_ns+" exec "+configuration.kafka_client_pod_name+" -- /usr/bin/kafka-console-consumer --topic "+configuration.kafka_topic+"  --bootstrap-server "+configuration.kafka_srv_svc+" --max-messages 1","check")
                return kafka_mp_output.put((out))

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
        expect(result).to(contain('MOCK_REQ_ID'))
        expect(result).to(contain('MOCK_UserAgent'))
        expect(result).to(contain('aaaaaaaaaaaaaaaa'))
        expect(result).to(contain('bbbbbbbbbbbbbbbb'))
        expect(result).to(contain('request_path'))
        expect(result).to(contain('source_uid'))








       





