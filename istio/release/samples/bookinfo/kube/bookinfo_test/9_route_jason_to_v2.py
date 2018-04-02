import requests
import subprocess
import time
import configuration
import performance
from mamba import description, context, it
from expects import expect, be_true, have_length, equal, be_a, have_property, be_none

rule_name="route-rule-reviews-test-v2.yaml"
Rule=configuration.Rule()

with description('Bookinfo route "Jason" User to V2 only'):
    with before.all:
         #Read Config file
         configuration.setenv(self)

    with context('Set environment'):
         with it('Bookinfo add Routing Rule'):
               Rule.add(rule_name)
               time.sleep(5)

    with context('Starting Test'):
        with it('Bookinfo route "jason" User to V2'):
            while self.total_count < 10:
                #cookie = {'user': 'jason'}
                u=self.url
                r = requests.post('http://'+self.GATEWAY_URL+'/productpage', data = {'username':'jason','passwd':''})

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

            print(" | V1 Hit="+str(self.v1_count)+" | V2 Hit="+str(self.v2_count)+" | V3 Hit="+str(self.v3_count)+" | Total Hit="+str(self.total_count)+ " |")
            expect(self.v1_count).to(equal(0))*
            expect(self.v2_count).not_to(equal(0))
            expect(self.v3_count).to(equal(0))


    with context('Clean Environment'):
        with it('Bookinfo delete Routing Rule'):
              Rule.delete(rule_name)
