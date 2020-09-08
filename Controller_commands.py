from subprocess import call
import threading
import subprocess
import random
import os
import time
import json
import sys

def ovsdb_addr(datapath):
    datapath_in=datapath
    mom_datapath= ['0' for i in range(16-len(datapath))]
    mom_datapath=''.join(mom_datapath)
    datapath=mom_datapath+datapath
    print "Set ovsdb on switch "+datapath
    try:
        os.popen("sudo -S curl -X PUT -d '\"tcp:127.0.0.1:6632\"' http://localhost:8080/v1.0/conf/switches/"+datapath+"/ovsdb_addr", 'w').write("Ao70pa45")
        print "\n"
        time.sleep(2)
    except:
        print "ovsdb: ERROR"

def ovssctl_set_bridge(switch_name):
    print "Set ovssctl on switch "+switch_name
    try:
        os.popen("sudo -S ovs-vsctl set Bridge "+switch_name+" protocols=OpenFlow13", 'w').write("Ao70pa45")
        print "\n"
    except:
        print "ovssctl_set_bridge: ERROR"

def get_switchis():
    print "Get switches id"
    try:
        output = subprocess.check_output(
             "curl -X GET http://localhost:8080/stats/switches",
             stderr=subprocess.STDOUT,
             shell=True)
        output=output[output.find("["):]
        end_response=output.find("]")
        list1=list(output)
        list1[end_response]=','
        output=''.join(list1)+"]"
        print "\n"
    except:
        output="NO NET"
    return output

def switch_ports_name(datapath):
    datapath_in=datapath
    mom_datapath= ['0' for i in range(16-len(datapath))]
    mom_datapath=''.join(mom_datapath)
    datapath=mom_datapath+datapath
    print "Get names on switch "+datapath
    try:
        output = subprocess.check_output(
             "curl -X GET http://localhost:8080/stats/portdesc/"+datapath,
             stderr=subprocess.STDOUT,
             shell=True)
        i=0
        output = output[output.find("{")+1:]
        end_response = output.find("}]}")+2
        list1=list(output)
        list1[end_response-2]='}'
        list1[end_response-1]=','
        output=''.join(list1)
        names = []
        while i<end_response:
            output_i=output[i:]
            i=i+output[i:].find("},")+2
            otp = output_i[output_i.find("{"):]
            otp = otp[0:otp.find("},")+1]
            otp =eval(otp)
            data = otp
            json_str = json.dumps(data)
            jsonList = json.loads(json_str)
            if jsonList['port_no']=="LOCAL":
                names.append(str(jsonList['name']))
            else:
                names.append(str(jsonList['name']))
        print "\n"
        return names
    

    except:
        print "Switch port name: ERROR"


def queue_rule(datapath, port_number, ip_dscp, queue_number):
    mom_datapath= ['0' for i in range(16-len(datapath))]
    mom_datapath=''.join(mom_datapath)
    datapath=mom_datapath+datapath
    print "Set queue rule on switch "+datapath+" on port "+port_number
    try:
        os.popen("curl -X POST -d '{\"match\": {\"ip_dscp\": \""+ip_dscp+"\"}, \"actions\":{\"queue\": \""+queue_number+"\"}}' http://localhost:8080/qos/rules/"+datapath, 'w').write("Ao70pa45")
        time.sleep(0.1)
        print "\n"
    except:
        print "Set queue rule: Error"

def queue_rule_byIP(datapath, port_number, ip_dscp, queue_number, ip_dst):
    mom_datapath= ['0' for i in range(16-len(datapath))]
    mom_datapath=''.join(mom_datapath)
    datapath=mom_datapath+datapath
    print "Set queue rule on switch "+datapath+" on port "+port_number
    try:
        os.popen("curl -X POST -d '{\"match\": {\"nw_dst\": \""+ip_dst+"\", \"ip_dscp\": \""+ip_dscp+"\"}, \"actions\":{\"queue\": \""+queue_number+"\"}}' http://localhost:8080/qos/rules/"+datapath, 'w').write("Ao70pa45")
        time.sleep(0.1)
        print "\n"
    except:
        print "Set queue rule: Error"

def set_queue(datapath, port_id, max_rate, queue_rate_list):
    mom_datapath= ['0' for i in range(16-len(datapath))]
    mom_datapath=''.join(mom_datapath)
    datapath=mom_datapath+datapath
    print "Set queue on port "+port_id+" of switch "+datapath
    print queue_rate_list
    try:
        output = subprocess.check_output("curl -X POST -d '{\"port_name\": \""+port_id+"\", \"type\": \"linux-htb\", \"max_rate\": \""+max_rate+"\", \"queues\": ["+queue_rate_list+"]}' http://localhost:8080/qos/queue/"+datapath,
             stderr=subprocess.STDOUT,
             shell=True)
        time.sleep(0.1)
        print "\n"
    except:
        print "Set queue: Error"


def set_Telecom_queue(datapath, port_number, IP_flag, IP_dst):
    port=port_number
    mom_datapath= ['0' for i in range(16-len(datapath))]
    mom_datapath=''.join(mom_datapath)
    datapath=mom_datapath+datapath
    if IP_flag==True:
        queue_rule_byIP(datapath, port, "0", "0", IP_dst)#Service 0
        queue_rule_byIP(datapath, port, "8", "0", IP_dst)#Service 1
        queue_rule_byIP(datapath, port, "10", "0", IP_dst)#Service 1
        queue_rule_byIP(datapath, port, "12", "0", IP_dst)#Service 1
        queue_rule_byIP(datapath, port, "14", "0", IP_dst)#Service 1
        queue_rule_byIP(datapath, port, "24", "0", IP_dst)#Service 3
        queue_rule_byIP(datapath, port, "26", "0", IP_dst)#Service 3
        queue_rule_byIP(datapath, port, "28", "0", IP_dst)#Service 3
        queue_rule_byIP(datapath, port, "30", "0", IP_dst)#Service 3

        queue_rule_byIP(datapath, port, "16", "1", IP_dst)#Service 2
        queue_rule_byIP(datapath, port, "18", "1", IP_dst)#Service 2
        queue_rule_byIP(datapath, port, "20", "1", IP_dst)#Service 2
        queue_rule_byIP(datapath, port, "22", "1", IP_dst)#Service 2
        queue_rule_byIP(datapath, port, "32", "1", IP_dst)#Service 4
        queue_rule_byIP(datapath, port, "34", "1", IP_dst)#Service 4
        queue_rule_byIP(datapath, port, "36", "1", IP_dst)#Service 4
        queue_rule_byIP(datapath, port, "38", "1", IP_dst)#Service 4
        queue_rule_byIP(datapath, port, "48", "1", IP_dst)#Service 6
        queue_rule_byIP(datapath, port, "56", "1", IP_dst)#Service 7

        queue_rule_byIP(datapath, port, "40", "2", IP_dst)#Service 5
        queue_rule_byIP(datapath, port, "46", "2", IP_dst)#Service 5

    if IP_flag==False:
        #Default Queue (queue_id = 0)
        queue_rule(datapath, port, "0", "0")#Service 0
        queue_rule(datapath, port, "8", "0")#Service 1
        queue_rule(datapath, port, "10", "0")#Service 1
        queue_rule(datapath, port, "12", "0")#Service 1
        queue_rule(datapath, port, "14", "0")#Service 1
        queue_rule(datapath, port, "24", "0")#Service 3
        queue_rule(datapath, port, "26", "0")#Service 3
        queue_rule(datapath, port, "28", "0")#Service 3
        queue_rule(datapath, port, "30", "0")#Service 3
        #Premium Queue (queue_id = 1)
        queue_rule(datapath, port, "16", "1")#Service 2
        queue_rule(datapath, port, "18", "1")#Service 2
        queue_rule(datapath, port, "20", "1")#Service 2
        queue_rule(datapath, port, "22", "1")#Service 2
        queue_rule(datapath, port, "32", "1")#Service 4
        queue_rule(datapath, port, "34", "1")#Service 4
        queue_rule(datapath, port, "36", "1")#Service 4
        queue_rule(datapath, port, "38", "1")#Service 4
        queue_rule(datapath, port, "48", "1")#Service 6
        queue_rule(datapath, port, "56", "1")#Service 7
        #Gold Queue (queue_id = 2)
        queue_rule(datapath, port, "40", "2")#Service 5
        queue_rule(datapath, port, "46", "2")#Service 5
    


