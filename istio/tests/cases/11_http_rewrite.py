import requests
import subprocess
import time
import configuration
import performance
from mamba import description, context, it
from expects import expect, be_true, have_length, equal, be_a, have_property, be_none

rule_name="route-rule-http-rewrite.yaml"
Rule=configuration.Rule()

with description('nginmesh Test 09'):
    with before.all:
         #Read Config file
         configuration.setenv(self)

    with context('Set environment'):
         with it('Bookinfo add Routing Rule'):
            Rule.add_addon(rule_name)
            time.sleep(10)

    with context('Starting Test'):
        with it('Bookinfo HTTP Rewrite'):
            while self.total_count < 10:
                r = requests.get(self.url,allow_redirects=False)
                r.status_code
                expect(r.status_code).to(equal(200))
                self.total_count += 1

                output=str(subprocess.check_output("kubectl logs $(kubectl get pod -n istio-system | grep istio-mixer | awk '{ print $1 }') -n istio-system mixer | grep 'request.path                  : /v1/bookRatings/0'", universal_newlines=True,shell=True)).rstrip()
                if 'bookRatings' in output:
                    print("HTTP Rewrite  Test -- Passed")
                    print("| Total Rewrite Hit=",self.total_count," |")
                elif self.total_count==0:
                    print("HTTP Rewrite does not work!")

                if self.performance=='on':
                    print performance.wrecker(self.GATEWAY_URL)
                else:
                    pass

    with context('Clean Environment'):
        with it('Bookinfo delete Routing Rule'):
            Rule.delete_addon(rule_name)

