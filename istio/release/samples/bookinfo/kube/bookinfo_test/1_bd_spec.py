import time
import performance
import configuration
# import logo
from mamba import description, context, it
from expects import expect, be_true, have_length, equal, be_a, have_property, be_none

with description('Bookinfo Basic Functionality test'):
    with before.all:
         #Read Config file
         configuration.setenv(self)

    with context('Starting Test'):
        with it('Bookinfo deploy without rules'):
            configuration.generate_request(self)

            expect(self.v1_count).not_to(equal(0))
            expect(self.v2_count).not_to(equal(0))
            expect(self.v3_count).not_to(equal(0))
            if self.performance=='on':
                print performance.wrecker(self.GATEWAY_URL)
            else:
                pass

