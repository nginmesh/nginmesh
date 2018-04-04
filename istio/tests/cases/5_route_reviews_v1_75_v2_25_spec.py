import configuration
import performance
from mamba import description, context, it
from expects import expect, be_true, have_length, equal, be_a, have_property, be_none

rule_name="route-rule-destination-weight.yaml"
Rule=configuration.Rule()

with description('nginmesh Test 05'):
    with before.all:
         #Read Config file
         configuration.setenv(self)

    with context('Set environment'):
         with it('Bookinfo add Routing Rule'):
            Rule.add(rule_name)

    with context('Starting Test'):
        with it('Bookinfo destination-weight test, route to V1-75%, V2-25%'):
            configuration.generate_request(self,rule_name)
            expect(self.v1_count).not_to(equal(0))
            expect(self.v2_count).not_to(equal(0))
            expect(self.v3_count).to(equal(0))
            expect(self.v1_count>self.v2_count).to(be_true)

    with context('Clean Environment'):
        with it('Bookinfo delete Routing Rule'):
            Rule.delete(rule_name)


