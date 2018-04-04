import requests
import configuration
import performance
from mamba import description, context, it
from expects import expect, be_true, have_length, equal, be_a, have_property, be_none

rule_name="route-rule-http-redirect.yaml"
Rule=configuration.Rule()

with description('nginmesh Test 07'):
    with before.all:
         #Read Config file
         configuration.setenv(self)

    with context('Set environment'):
         with it('Bookinfo add Routing Rule'):
            Rule.add(rule_name)

    with context('Starting Test'):
        with it('Bookinfo HTTP Redirect'):

            while self.total_count < 10:
                r = requests.get(self.url,allow_redirects=False)
                r.status_code
                expect(r.status_code).to(equal(301))
                self.total_count += 1
            configuration.generate_request(self,rule_name)

    with context('Clean Environment'):
        with it('Bookinfo delete Routing Rule'):
            Rule.delete(rule_name)
