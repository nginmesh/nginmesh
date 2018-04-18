import requests
import time
import configuration
from mamba import description, context, it
from expects import expect, be_true, have_length, equal, be_a, have_property, be_none

headers = {'content-type': 'application/json','accept': 'application/json'}
with description('Zipkin tracing functionality'):
    with before.all:
         #Read Config file
         configuration.setenv(self)

    with context('Set environment'):
         with it('Add Zipkin tracing feature'):
            configuration.run_shell("kubectl apply -f "+configuration.nginmesh_install_path+"zipkin/zipkin.yaml","run")
            time.sleep(configuration.rule_apply_time)
            configuration.run_shell("kubectl -n istio-system port-forward $(kubectl -n istio-system get pod -l app=zipkin -o jsonpath='{.items[0].metadata.name}') 9411:9411 &","run")
            time.sleep(configuration.rule_apply_time)

    with context('Starting Test'):
        with it('Bookinfo Zipkin tracing feature'):
            for _ in range(10):
                r = requests.get(self.url)
                r.status_code
                expect(r.status_code).to(equal(200))
            r1=requests.get(self.zipkin)
            r1.status_code
            expect(r1.status_code).to(equal(200))
            if 'productpage' in r1.text:
                expect(0).to(equal(0))
            else:
                expect(0).not_to(equal(0))
            configuration.generate_request(self)

    with context('Clean Environment'):
        with it('Delete Zipkin tracing feature'):
            configuration.run_shell("kubectl delete -f "+configuration.nginmesh_install_path+"zipkin/zipkin.yaml","run")
            configuration.run_shell("ps -ef | grep zipkin | grep -v grep | awk '{print $2}' | xargs kill -9","run")







