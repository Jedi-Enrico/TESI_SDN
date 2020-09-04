#!/usr/bin/python

import pandas as pd
import time

# Constants
# Value of Interval Time in second
TIME = 300
TIME_MS = TIME * 1000
# Scale factor for the packet rate. It will be equal to [ pkts / scale ] per second.
SCALE = 400
# CSV Entries
SIZE = 576
# Simulation Time in CSV hours
SIM = 312
# Simulation in number of intevals
SIM_N = SIM * 12
computername="jedi"
# CSV File
CSV = '/home/'+computername+'/Scrivania/RyuDatapathMonitor-master/CSV/vlan_interfaccia1_DOS.csv'
# ToS 
SERV_0 = "0"
SERV_1 = "32"
SERV_2 = "72"
SERV_3 = "96"
SERV_4 = "136"
SERV_5 = "160"
SERV_6 = "192"
SERV_7 = "224"

# IDT_OPT
# constant
c_idt = "-C"
#poisson
p_idt = "-O"
#esponential
e_idt ="-E"

# PS_OPT
# constant
c_ps = "-c"
# poisson
p_ps = "-o"
# esponential
e_ps ="-e"

# default value for protocol and packet size 
DEFAULT_P = "UDP"
DEFAULT_PS = "512"

# Host Ip
src = "10.0.0.11"
dst = "10.0.0.13"

# Type of distribution
choice_i = c_idt
choice_s = c_ps


# Cmd creation
def createCmd(src, dst, tos, nPkts, avg, protocol=DEFAULT_P, ps_dim=DEFAULT_PS):
    #com = 'ITGManager ' + src + ' -a ' + dst + ' -b ' + tos + ' ' + choice_i + ' ' + str(avg) + ' ' + choice_s + ' ' + ps_dim + ' -z ' + str(nPkts)
    com = 'ITGManager ' + src + ' -a ' + dst + ' -b ' + tos + ' ' + choice_i + ' ' + str(avg) + ' ' + choice_s + ' ' + ps_dim + ' -t ' + str(TIME_MS-8000)
    return com

# Cmd creation
def createCmd_2(dst, port, tos, nPkts, avg, protocol=DEFAULT_P, ps_dim=DEFAULT_PS):
    #com = 'ITGSend -a ' + dst + ' -rp ' + str(port) + ' -b ' + tos + ' ' + choice_i + ' ' + str(avg) + ' ' + choice_s + ' ' + ps_dim + ' -z ' + str(nPkts) + ' &'		
    com = 'ITGSend -a ' + dst + ' -rp ' + str(port) + ' -b ' + tos + ' ' + choice_i + ' ' + str(avg) + ' ' + choice_s + ' ' + ps_dim + ' -t ' + str(TIME_MS-10000) + ' &'
    #com = 'ITGSend -a ' + dst + ' -b ' + tos + ' ' + choice_i + ' ' + str(avg) + ' ' + choice_s + ' ' + ps_dim + ' -t ' + str(TIME_MS-8000) + ' &'				
    return com

# Cmd creation Iperf
def createCmd_3(dst, port, tos, nPkts, avg, protocol=DEFAULT_P, ps_dim=DEFAULT_PS):
    #com = 'ITGSend -a ' + dst + ' -rp ' + str(port) + ' -b ' + tos + ' ' + choice_i + ' ' + str(avg) + ' ' + choice_s + ' ' + ps_dim + ' -z ' + str(nPkts) + ' &'		
    com = 'iperf3 -c ' + dst + ' -p ' + str(port) + ' -S ' + tos + ' ' + ' -k ' + str(nPkts) + ' &'		
    return com
