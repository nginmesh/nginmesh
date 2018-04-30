#!/bin/bash
pkill -f port-forward
../../install/kafka/ksql-portforward.sh &
./elastic-portforward.sh &
./grafana-portforward.sh &
../../install/kafka/connect-porforward.sh &
../../install/kafka/ksql-portforward.sh &
