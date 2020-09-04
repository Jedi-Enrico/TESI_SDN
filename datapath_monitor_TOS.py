from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types
from operator import attrgetter
import threading
import time
import datetime

import subprocess
import json
import sys

from Controller_commands import *
import numpy as np

from subprocess import call
import random
import os

now=datetime.datetime.now()
year=str(now.year)
month=str(now.month)
day=str(now.day)
date=year+"-"+month+"-"+day+"_"
computername="jedi"
file = open("/home/"+computername+"/Scrivania/RyuDatapathMonitor-master/DataLog/"+date+"flowstat.txt","a")
stringa="time"+"\t"+"datapath"+"\t"+"in-port"+"\t"+"eth-dst"+"\t"+"out-port"+"\t"+"packets"+"\t"+"bytes"+"\t"+"ip_dscp"+"\t"+"SET_QUEUE\n"
file.write(stringa)
file.close()

file = open("/home/"+computername+"/Scrivania/RyuDatapathMonitor-master/DataLog/"+date+"queuestat.txt","a")
stringa="time"+"\t"+"datapath"+"\t"+"port_no"+"\t"+"queue_id"+"\t"+"tx_bytes"+"\t"+"tx_packets"+"\t"+"tx_errors"+"\t"+"duration_sec"+"\t"+"duration_nsec\n"
file.write(stringa)
file.close()

file = open("/home/"+computername+"/Scrivania/RyuDatapathMonitor-master/DataLog/"+date+"portstat.txt","a")
stringa="time"+"\t"+"datapath"+"\t"+"port"+"\t"+"rx-pkts"+"\t"+"rx-bytes"+"\t"+"rx_error"+"\t"+"tx-pkts"+"\t"+"tx-bytes"+"\t"+"tx-error"+"\t"+"rx-dropped"+"\t"+"tx-dropped"+"\t"+"rx-crc-err"+"\t"+"collisions"+"\n"
file.write(stringa)
file.close()

file = open("/home/"+computername+"/Scrivania/RyuDatapathMonitor-master/DataLog/"+date+"queueconfig.txt","a")
stringa="time"+"\t"+"datapath"+"\t"+"queue_id"+"\t"+"type_of_rule"+"\t"+"rate\n"
file.write(stringa)
file.close()

def get_switchis():
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
    except:
        output="No NET"
    return output

def save_flow_stat(datapath):
    datapath_in=datapath
    mom_datapath= ['0' for i in range(16-len(datapath))]
    mom_datapath=''.join(mom_datapath)
    datapath=mom_datapath+datapath
    try:
        output = subprocess.check_output(
             "curl -X GET http://localhost:8080/stats/flow/"+datapath,
             shell=True)
        i=0
        output = output[output.find("{")+1:]
        end_response = output.find("}]}")+2
        list1=list(output)
        list1[end_response-2]='}'
        list1[end_response-1]=','
        output=''.join(list1)
        while i<end_response:
            output_i=output[i:]
            i=i+output[i:].find("},")+2
            otp = output_i[output_i.find("{"):]
            otp = otp[0:otp.find("},")+1]
            otp =eval(otp)
            data = otp
            json_str = json.dumps(data)
            jsonList = json.loads(json_str)
            if jsonList['priority']!=0 and jsonList['match'].get('in_port'):
                porta=str(jsonList['actions'])
                prc = porta.find('T:')
                #Check if there is "OUTPUT:" in the string
                if prc >= 0:
                    porta=porta[prc+2:]
                    porta = int(porta[0:porta.find(']')-1])
    ##                        self.logger.info('%016x %8x %17s %8x %8d %8d',
    ##                                         1,
    ##                                         jsonList['match'].get('in_port'), jsonList['match'].get('dl_dst'),
    ##                                         porta, jsonList['packet_count'],
    ##                                         jsonList['byte_count'])
                    file = open("/home/"+computername+"/Scrivania/RyuDatapathMonitor-master/DataLog/"+date+"flowstat.txt","a")
                    now=datetime.datetime.now()
                    stringa=str(now)+"\t"+datapath_in+"\t"+str(jsonList['match'].get('in_port'))+"\t"+str(jsonList['match'].get('dl_dst'))+"\t"+str(porta)+"\t"+str(jsonList['packet_count'])+"\t"+str(jsonList['byte_count'])+"\t None"+"\t None"+"\n"
                    file.write(stringa)
                    file.close()
            if jsonList['priority']!=0 and str(jsonList['actions']).find('UE:')>=0:
                SET_QUEUE=str(str(jsonList['actions'])[str(jsonList['actions']).find('UE:')+3:str(jsonList['actions']).find(',')-1])
##                print "SET_QUEUE: "+SET_QUEUE
                file = open("/home/"+computername+"/Scrivania/RyuDatapathMonitor-master/DataLog/"+date+"flowstat.txt","a")
                now=datetime.datetime.now()
                stringa=str(now)+"\t"+datapath_in+"\t"+str(jsonList['match'].get('in_port'))+"\t"+str(jsonList['match'].get('nw_dst'))+"\t"+"None"+"\t"+str(jsonList['packet_count'])+"\t"+str(jsonList['byte_count'])+"\t"+str(jsonList['match'].get('ip_dscp'))+"\t"+SET_QUEUE+"\n"
##                print "ip_dscp: "+str(jsonList['match'].get('ip_dscp'))
##                print stringa
                file.write(stringa)
                file.close()                

    except:
        print "FlowStat: No NET"

def save_port_stat(datapath):
    datapath_in=datapath
    mom_datapath= ['0' for i in range(16-len(datapath))]
    mom_datapath=''.join(mom_datapath)
    datapath=mom_datapath+datapath
    try:
        output = subprocess.check_output(
             "curl -X GET http://localhost:8080/stats/port/"+datapath,
             shell=True)
        i=0
        output = output[output.find("{")+1:]
        end_response = output.find("}]}")+2
        list1=list(output)
        list1[end_response-2]='}'
        list1[end_response-1]=','
        output=''.join(list1)
        while i<end_response:
            output_i=output[i:]
            i=i+output[i:].find("},")+2
            otp = output_i[output_i.find("{"):]
            otp = otp[0:otp.find("},")+1]
            otp =eval(otp)
            data = otp
            json_str = json.dumps(data)
            jsonList = json.loads(json_str)
            if jsonList['port_no']!="LOCAL":
##                        self.logger.info('%016x %8x %17s %8x %8d %8d',
##                                         1,
##                                         jsonList['match'].get('in_port'), jsonList['match'].get('dl_dst'),
##                                         porta, jsonList['packet_count'],
##                                         jsonList['byte_count'])
                file = open("/home/"+computername+"/Scrivania/RyuDatapathMonitor-master/DataLog/"+date+"portstat.txt","a")
                now=datetime.datetime.now()
                stringa=str(now)+"\t"+datapath_in+"\t"+str(jsonList['port_no'])+"\t"+str(jsonList['rx_packets'])+"\t"+str(jsonList['rx_bytes'])+"\t"+str(jsonList['rx_errors'])+"\t"+str(jsonList['tx_packets'])+"\t"+str(jsonList['tx_bytes'])+"\t"+str(jsonList['tx_errors'])+"\t"+str(jsonList['rx_dropped'])+"\t"+str(jsonList['tx_dropped'])+"\t"+str(jsonList['rx_crc_err'])+"\t"+str(jsonList['collisions'])+"\n"
                file.write(stringa)
                file.close() 

    except:
        print "PortStat: No NET"

def save_queue_stat(datapath):
    datapath_in=datapath
    mom_datapath= ['0' for i in range(16-len(datapath))]
    mom_datapath=''.join(mom_datapath)
    datapath=mom_datapath+datapath
    try:
        output = subprocess.check_output(
             "curl -X GET http://localhost:8080/qos/queue/status/"+datapath,
             shell=True)
        i=0
        output = output[output.find("ult")+1:]
        output = output[output.find("{")+1:]
        end_response = output.find("}]}")+2
        list1=list(output)
        list1[end_response-2]='}'
        list1[end_response-1]=','
        output=''.join(list1)
        if output[output.find(":")+2:output.find(":")+4]!="[]":
            while i<end_response:
                output_i=output[i:]
                i=i+output[i:].find("},")+2
                otp = output_i[output_i.find("{"):]
                otp = otp[0:otp.find("},")+1]
##                print otp
                otp = eval(otp)
                data = otp
                json_str = json.dumps(data)
                jsonList = json.loads(json_str)
                file = open("/home/"+computername+"/Scrivania/RyuDatapathMonitor-master/DataLog/"+date+"queuestat.txt","a")
                now=datetime.datetime.now()
                stringa=str(now)+"\t"+datapath_in+"\t"+str(jsonList['port_no'])+"\t"+str(jsonList['queue_id'])+"\t"+str(jsonList['tx_bytes'])+"\t"+str(jsonList['tx_packets'])+"\t"+str(jsonList['tx_errors'])+"\t"+str(jsonList['duration_sec'])+"\t"+str(jsonList['duration_nsec'])+"\n"
                file.write(stringa)
                file.close() 

    except:
        print "QueueStat: No NET"

def save_queue_config(datapath):
    datapath_in=datapath
    mom_datapath= ['0' for i in range(16-len(datapath))]
    mom_datapath=''.join(mom_datapath)
    datapath=mom_datapath+datapath
    try:
        output = subprocess.check_output(
             "curl -X GET http://localhost:8080/qos/queue/"+datapath,
             shell=True)
        i=0
        output=output[1:len(output)-1]
        jsonList = json.loads(output)
        config = jsonList['command_result'].get('details')
        for queue in config:
            if queue=='2':
                rate = jsonList['command_result'].get('details').get(queue).get('config').get('min-rate')
                type_of_rule='min_rate'
            else:
                rate = jsonList['command_result'].get('details').get(queue).get('config').get('max-rate')
                type_of_rule='max_rate'
            file = open("/home/"+computername+"/Scrivania/RyuDatapathMonitor-master/DataLog/"+date+"queueconfig.txt","a")
            now=datetime.datetime.now()
            stringa=str(now)+"\t"+datapath_in+"\t"+str(queue)+"\t"+str(type_of_rule)+"\t"+str(rate)+"\n"
            file.write(stringa)
            file.close() 
    except:
        print "QueueConfig: No NET"

class DatapathMonitor():
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, args):
        self.datapath_list = args["dp"]

        self.monitor = threading.Thread(target=self.switch_monitor_thread)
        self.delta = args["step"]
        self.logger = args["logger"]

        self.started = False

    def start(self):
        self.monitor.start()
        self.started = True

    def update(self, dplist):
        self.datapath_list = dplist

    def switch_monitor_thread(self):
        max_rate_queue=100#Mps
        max_rate_queue=max_rate_queue*1000000
        minute_wait=20
        Time_queue=minute_wait*60
        Change_flag=Time_queue/self.delta
        counter=Change_flag
        c_q2=0
        c_q1=1
        c_q0=1
        q2=np.arange(70, 101, 10)*1000000
        q1=np.arange(0, 101, 10)*1000000
        q0=np.arange(0, 101, 10)*1000000
##        time.sleep(40)
        
        print 'Wait for time alignment'
        wait=self.delta/60
        check_time=False
        while check_time==False:
            now=datetime.datetime.now()
            if now.minute%wait==0:
                check_time=True
            else:
                time.sleep(1)
        print 'Starting Save Data'
        
        while True:
            check_time=False
            while check_time==False:
                now=datetime.datetime.now()
                if now.minute%wait==0:
                    check_time=True
                    print "Save Time: "+str(now)
                else:
                    time.sleep(1)
            NET=get_switchis()
##            print "NET="+NET
            t_sleep = 0.9
            if NET != "NO NET" and NET!="[,]":
##                end_response = output.find("]")
                i=1
                while i<NET.find("]"):
                    mom_NET=NET[i:]
                    datapath=NET[i:i+mom_NET.find(",")]
##                    time.sleep(1)
                    i=i+mom_NET.find(",")+2
                    save_flow_stat(datapath)
##                    time.sleep(0.9)
                    save_port_stat(datapath)
##                    time.sleep(t_sleep)
                    save_queue_stat(datapath)
##                    time.sleep(t_sleep)
                    save_queue_config(datapath)
                print counter
                if counter >= Change_flag:
                    set_queue("1", "s1-eth2", str(max_rate_queue), "{\"max_rate\": \""+str(q0[c_q0])+"\"}, {\"max_rate\": \""+str(q1[c_q1])+"\"}, {\"min_rate\": \""+str(q2[c_q2])+"\"}")
                    set_queue("2", "s2-eth2", str(max_rate_queue), "{\"max_rate\": \""+str(q0[c_q0])+"\"}, {\"max_rate\": \""+str(q1[c_q1])+"\"}, {\"min_rate\": \""+str(q2[c_q2])+"\"}")
                    counter=0
                    c_q0=c_q0+1
                    if c_q0>len(q0)-1:
                        c_q0=1
                        c_q1=c_q1+1
                        if c_q1>len(q1)-1:
                            c_q1=1
                            c_q2=c_q2+1
                            if c_q2>len(q2)-1:
                                c_q2=0
                else:
                    counter=counter+1
                    
            else:
                print "No Network"

