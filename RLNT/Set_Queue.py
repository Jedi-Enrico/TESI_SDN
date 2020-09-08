from subprocess import call
import threading
import subprocess
import random
import os
import time
import datetime
import json
import sys
import ditg

from Controller_commands import *

max_rate_queue=100#Mbps
max_rate_queue=max_rate_queue*1000000
Default=str(max_rate_queue*20/100)#20%
Premium=str(max_rate_queue*80/100)#80%
Gold=str(max_rate_queue*100/100)#100%

def set_queue_eth2():
    NET = get_switchis()
    if NET != "NO NET" and NET!="[,]":
        i=1
        while i<NET.find("]"):
            mom_NET=NET[i:]
            datapath=NET[i:i+mom_NET.find(",")]
            i=i+mom_NET.find(",")+2
            port_id = switch_ports_name(datapath)
        time.sleep(0.2)
        i=1
        while i<NET.find("]"):
            mom_NET=NET[i:]
            datapath=NET[i:i+mom_NET.find(",")]
            i=i+mom_NET.find(",")+2
            port_id = switch_ports_name(datapath)
            ovsdb_addr(datapath)

            print(port_id)
            IP_Flag=True
            for index in range(0,len(port_id)):
                if port_id[index]=="eth2" or port_id[index]=="eth1":
                    print "Port_ID: "+port_id[index]
                    port = port_id[index][port_id[index].find("h")+1:]
                    if port_id[index]=="eth2":
                        set_queue(datapath, port_id[index], str(max_rate_queue), "{\"max_rate\": \""+Default+"\"}, {\"max_rate\": \""+Premium+"\"}, {\"min_rate\": \""+Gold+"\"}")
                        IP_Destination="169.254.181.98"
                        set_Telecom_queue(datapath, port, IP_Flag, IP_Destination)

try:
    os.popen("sudo -S curl -X DELETE http://localhost:8080/qos/queue/0000000000000002", 'w').write("Ao70pa45")
    print "\n"
    set_queue_eth2()
except:
    print "ERROR"

                  
