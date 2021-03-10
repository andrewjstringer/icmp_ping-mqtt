# icmp_ping-mqtt

Python ping module based to send message to MQTT broker.
This was written to monitor the status of an internet 
connection delivered over an ADSL connection which was at 
times flaky.

Logic is as follows, test two high availability ipaddresses,
preference is to use ipadddresses rather than DNS names to
remove DNS resolution as a potential issue. 1.1.1.1 (Cloudflare)
and 8.8.4.4 (Google) would be good choices.
If either of these returns ok, then the Internet is available,
write stats to MQTT and quit.
But it both ip addresses fail, run a retest. 
If either of the two retests returns true, then assume 
Internet is ok, and write stats to MQTT Broker and quit.
If both retests fail the assume Internet is down, write fail
message to MQTT and quit

The MQTT topic will be monitored for a failure message by another 
process to initiate a router reload. 

Probably will be run inside a container from cron or similar.

