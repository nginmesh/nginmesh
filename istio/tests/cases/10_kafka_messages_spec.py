import requests,time
import configuration
import performance
from mamba import description, context, it
from expects import expect, equal

with description('Testing Kafka messages'):
    with before.all:
         #Read Config file
         configuration.setenv(self)
         configuration.generate_request(self)

with context('Starting test'):
    with it('Testing Kafka functionality'):

        proc_a = configuration.mp.Process(target=configuration.check_kafka_logs,args=(self,configuration.kafka_mp_output))
        proc_b = configuration.mp.Process(target=configuration.generate_kafka_mock_request)
        proc_a.start()
        proc_b.start()
        proc_a.join()
        proc_b.join()
        result=configuration.kafka_mp_output.get()
        for i in range(0,len(result)):
            try:
                expect(result[i]).to(equal(1))
            except:
                raise Exception(configuration.kafka_check_values[i]+" is not found")








       





