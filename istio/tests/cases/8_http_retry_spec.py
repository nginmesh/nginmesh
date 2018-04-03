import requests
import subprocess
import time
import configuration
import performance
from mamba import description, context, it
from expects import expect, be_true, have_length, equal, be_a, have_property, be_none

rule_name="route-rule-http-retry.yaml"
Rule=configuration.Rule()

with description('nginmesh Test 08'):
    with before.all:
         #Read Config file
         configuration.setenv(self)

    with context('Set environment'):
         with it('Bookinfo add Routing Rule'):
            Rule.add(rule_name)
            time.sleep(10)

    with context('Starting Test'):
        with it('Bookinfo HTTP Retry'):
            while self.total_count < 10:
                r = requests.get(self.url,allow_redirects=False)
                r.status_code
                expect(r.status_code).to(equal(200))
                self.total_count += 1
                output=str(subprocess.check_output("kubectl exec -it $(kubectl get pod | grep productpage | awk '{ print $1 }') -c istio-proxy cat /etc/istio/proxy/conf.d/http_0.0.0.0_9080.conf", universal_newlines=True,shell=True)).rstrip()

            if 'proxy_next_upstream_timeout' in output and 'proxy_next_upstream_tries' in output :
                    print("Total Retry Hit="+str(self.total_count))
                    expect(self.total_count).not_to(equal(0))
            if self.performance=='on':
                print performance.wrecker(self.GATEWAY_URL)
            else:
                pass

    with context('Clean Environment'):
        with it('Bookinfo delete Routing Rule'):
            Rule.delete(rule_name)


