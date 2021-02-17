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



if hostalive_1.is_alive and hostalive_2.is_alive:
    print("Both hostalive_1/2 Yes,", hostalive_1.is_alive, hostalive_2.is_alive)
    # hint - create dictionary for each host and combine as list
    #message = hostalive_1.address + str(hostalive_1.min_rtt) + hostalive_2.address + str(hostalive_2.min_rtt)
    host1 = {hostalive_1.address:{ "is_alive": hostalive_1.is_alive, "rtt": hostalive_1.min_rtt }}
    host2 = {hostalive_2.address:{ "is_alive": hostalive_2.is_alive, "rtt": hostalive_2.min_rtt }}
    message = ["Internet_Status", host1, host2]

    print(message)

    publish_to_mqtt(config.publish_topic,  json.dumps(message), 0)
    sys.exit(0)
else:
    stuff = True




#Internet:
#  - ip1:
#      is_alive: True
#      response_time: 19ms
#  - ip2:
#      is_alive: False
#      response_time:

#if hostalive:   # is True
#    print("hostalive Yes,", hostalive)
#    publish_to_mqtt(config.publish_topic,  config.ipaddress_1, 0)
#    sys.exit(0)
#else:
#    print("hostalive No, sleeping for retest", hostalive)
#    time.sleep(5)
#     hostalive2 = ping_host(config.ipaddress)

#     if hostalive2: # = True
#         publish_to_mqtt(success 2nd attempt)
#         return
#     else
#         host not reachable
#         publish_to_mqtt(message)
#         sys.exit(1)
