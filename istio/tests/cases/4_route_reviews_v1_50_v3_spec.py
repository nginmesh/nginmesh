import configuration
import performance
from mamba import description, context, it
from expects import expect, be_true, have_length, equal, be_a, have_property, be_none

rule_name="route-rule-reviews-50-v3.yaml"
Rule=configuration.Rule()

with description('nginmesh Test 04'):
    with before.all:
         #Read Config file
         configuration.setenv(self)

    with context('Set environment'):
         with it('Bookinfo add Routing Rule'):
            Rule.add(rule_name)

    with context('Starting Test'):
        with it('Bookinfo route all requests to V1 and V3'):
            configuration.generate_request(self,rule_name)
            expect(self.v1_count).not_to(equal(0))
            expect(self.v2_count).to(equal(0))
            expect(self.v3_count).not_to(equal(0))

    with context('Clean Environment'):
        with it('Bookinfo delete Routing Rule'):
            Rule.delete(rule_name)


