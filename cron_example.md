## Example cron for running this

Cron needs to invoke python in the venv to get access to the installed packages.

/path/to/__/venv/bin/python3 icmp.py

Pointing to the python3 in the venv allows this without having to activate the venv which may not work well in cron due to the usual "source" needed.

For Ubuntu in ''/etc/cron.d/mqtt_test_internet''

*/5  * * * *  <user>  /home/sysadmin/scripts/mqtt-internet-check/venv/bin/python3 icmp.py

