from icmplib import ping
import paho.mqtt.client as paho
import config  # Import config file for variables
import sys
import json


def ping_host(host):
    ping_response = ping(host, count=1, timeout=2, privileged=False )
    # print("Is alive?", host, ping_response.is_alive)
    return ping_response


def publish_to_mqtt(pub_topic, payload, qos):
    # print("From in publish_to_mqtt", pub_topic, payload, qos)
    client_pub.publish(pub_topic, payload, qos)
    return

# Example output:-
# ["Internet_Status", {"internet_ok": true}, {"1.1.1.1": {"is_alive": true, "rtt": 13.46}}, {"8.8.4.4": {"is_alive": true, "rtt": 13.343}}]

# Main code
client_pub = paho.Client("clientsub-002")
client_pub.connect(config.broker)
# print("publishing to ", config.publish_topic)


# print("ping to ", config.ipaddress_1)

hostalive_1 = ping_host(config.ipaddress_1)
hostalive_2 = ping_host(config.ipaddress_2)

# logic
# test each host, if either is alive, then internet is ok.
# if both fail, retest both, if both fail again, then assume internet is down.

if hostalive_1.is_alive or hostalive_2.is_alive:
    # print("1st test - Either hostalive_1 or 2 alive, 1:-", hostalive_1.is_alive, "2:-", hostalive_2.is_alive)
    host1 = {hostalive_1.address:{ "is_alive": hostalive_1.is_alive, "rtt": hostalive_1.min_rtt }}
    host2 = {hostalive_2.address:{ "is_alive": hostalive_2.is_alive, "rtt": hostalive_2.min_rtt }}
    teststatus = {"internet_ok":True}
    message = ["Internet_Status", teststatus, host1, host2]

    result = json.dumps(message)
    print(result)
    # publish internet is OK
    publish_to_mqtt(config.publish_topic, result, 0)
    sys.exit(0)
else:
    # 2nd test
    hostalive_retest_1 = ping_host(config.ipaddress_1)
    hostalive_retest_2 = ping_host(config.ipaddress_2)

    host_retest_1 = {hostalive_retest_1.address: {"is_alive": hostalive_retest_1.is_alive, "rtt": hostalive_retest_1.min_rtt}}
    host_retest_2 = {hostalive_retest_2.address: {"is_alive": hostalive_retest_2.is_alive, "rtt": hostalive_retest_2.min_rtt}}

    if hostalive_retest_1.is_alive or hostalive_retest_2.is_alive:
        # print("retest - Either hostalive_retest_1 or 2 alive, 1:-", hostalive_retest_1, "2:-", hostalive_retest_2.is_alive)
        reteststatus = {"internet_ok":True}
        message_retest = ["Internet_Status", reteststatus, host_retest_1, host_retest_2]

        retest_result = json.dumps(message_retest)
        print(retest_result)
        # publish internet is OK
        publish_to_mqtt(config.publish_topic, retest_result, 0)
        sys.exit(0)
    else:
        # print("Failed test and retest")
        reteststatus = {"internet_ok":False}
        message_retest = ["Internet_Status", reteststatus, host_retest_1, host_retest_2]

        retest_result = json.dumps(message_retest)
        print(retest_result)
        # publish internet is NOT ok
        publish_to_mqtt(config.publish_topic, retest_result, 0)
        sys.exit(1)
