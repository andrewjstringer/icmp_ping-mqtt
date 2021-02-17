from icmplib import ping
import paho.mqtt.client as paho
import config
import time
import sys
import json

def ping_host(host):
    pingresponse = ping(host, count=1, timeout=2, privileged=True )
    print("Is alive?", pingresponse.is_alive)
    return pingresponse

def publish_to_mqtt(pubtopic, payload, qos):
    print("From in publish_to_mqtt", pubtopic, payload, qos)
    clientpub.publish(pubtopic, payload, qos)
    return


# main code
clientpub = paho.Client("clientsub-002")
clientpub.connect(config.broker)
print("publishing to ", config.publish_topic)


print("ping to ", config.ipaddress_1)

hostalive_1 = ping_host(config.ipaddress_1)
hostalive_2 = ping_host(config.ipaddress_2)

# logic
# test each host, if either is alive, then internet is ok.
# if both fail, retest both, if both fail again, then assume internet is down.

if hostalive_1.is_alive or hostalive_2.is_alive:
    print("1st test - Either hostalive_1 or 2 alive, 1:-", hostalive_1.is_alive, "2:-", hostalive_2.is_alive)
    host1 = {hostalive_1.address:{ "is_alive": hostalive_1.is_alive, "rtt": hostalive_1.min_rtt }}
    host2 = {hostalive_2.address:{ "is_alive": hostalive_2.is_alive, "rtt": hostalive_2.min_rtt }}
    teststatus = {"internet_ok":True}
    message = ["Internet_Status", teststatus, host1, host2]

    print(message)
    # publish internet is OK
    publish_to_mqtt(config.publish_topic,  json.dumps(message), 0)
    sys.exit(0)
else:
    # 2nd test
    hostalive_retest_1 = ping_host(config.ipaddress_1)
    hostalive_retest_2 = ping_host(config.ipaddress_2)

    host_retest_1 = {hostalive_retest_1.address: {"is_alive": hostalive_retest_1.is_alive, "rtt": hostalive_retest_1.min_rtt}}
    host_retest_2 = {hostalive_retest_2.address: {"is_alive": hostalive_retest_2.is_alive, "rtt": hostalive_retest_2.min_rtt}}

    if hostalive_retest_1.is_alive or hostalive_retest_2.is_alive:
        print("retest - Either hostalive_retest_1 or 2 alive, 1:-", hostalive_retest_1, "2:-", hostalive_retest_2.is_alive)
        reteststatus = {"internet_ok":True}
        message_retest = ["Internet_Status", reteststatus, host_retest_1, host_retest_2]

        print(message_retest)
        # publish internet is OK
        publish_to_mqtt(config.publish_topic,  json.dumps(message_retest), 0)
        sys.exit(0)
    else:
        print("Failed test and retest")
        reteststatus = {"internet_ok":False}
        message_retest = ["Internet_Status", reteststatus, host_retest_1, host_retest_2]

        print(message_retest)
        # publish internet is OK
        publish_to_mqtt(config.publish_topic,  json.dumps(message_retest), 0)

        sys.exit(1)

