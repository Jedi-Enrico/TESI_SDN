from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
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

        
def myNetwork():
    max_rate_queue=100#Mbps
    max_rate_queue=max_rate_queue*1000000
    Default=str(max_rate_queue*20/100)#20%
    Premium=str(max_rate_queue*80/100)#80%
    Gold=str(max_rate_queue*100/100)#100%

    change_values=6#change every number*5 minutes
    Q0=False
    #Stress Queue 1 (2,4,6,7)
    Q1=False
    #Stress Queue 2 (5)
    Q2=False
    #moltiplicator initialization
    F0_max=2
    F1_max=300
    F2_max=300
    F0=1
    F1=1
    F2=1
    
    net=Mininet( topo=None,
                 build=False,
                 ipBase='10.0.0.0/8')

    info( '***Adding controller\n')
    c0=net.addController(name='c0',
                         controller=RemoteController,
                         ip='127.0.0.1',
                         protocol='tcp',
                         port=6633)
    
    info( '***Adding switches\n')
    s1 = net.addSwitch('s1',dpid='0000000000000001',protocols="OpenFlow13")
    s2 = net.addSwitch('s2',dpid='0000000000000002',protocols="OpenFlow13")

    info( '***Adding Host\n')
    h0 = net.addHost('h0', ip='10.10/24', mac='00:00:00:00:00:0a')
    h1 = net.addHost('h1', ip='10.11/24', mac='00:00:00:00:00:0b')
    h2 = net.addHost('h2', ip='10.12/24', mac='00:00:00:00:00:0c')
    h3 = net.addHost('h3', ip='10.13/24', mac='00:00:00:00:00:0d')
    h4 = net.addHost('h4', ip='10.14/24', mac='00:00:00:00:00:0e')
    h5 = net.addHost('h5', ip='10.15/24', mac='00:00:00:00:00:0f')

    info( '***Adding Link\n')
    net.addLink(s1,s2,2,2)
    
    net.addLink(s1, h0,3,0)
    net.addLink(s1, h1,4,0)
    net.addLink(s1, h2,5,0)
    net.addLink(s2, h3,3,0)
    net.addLink(s2, h4,4,0)
    net.addLink(s2, h5,5,0)

    info( '***Starting Network\n')
    net.build()

    info( '***Starting Controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '***Starting Switches\n')
    net.get('s1').start([c0])
    net.get('s2').start([c0])


    #Activation of manager in listening on port 6632
    os.popen("sudo -S ovs-vsctl set-manager ptcp:6632", 'w').write("Ao70pa45")
    time.sleep(2)
    NET = get_switchis()
    if NET != "NO NET" and NET!="[,]":
        i=1
        while i<NET.find("]"):
            mom_NET=NET[i:]
            datapath=NET[i:i+mom_NET.find(",")]
            i=i+mom_NET.find(",")+2
            port_id = switch_ports_name(datapath)
            for k in range(0,len(port_id)):
                if len(port_id[k])<=2:
                    pp=port_id[k]
                    print pp
                    ovssctl_set_bridge(port_id[k])
        time.sleep(0.2)
        i=1
        while i<NET.find("]"):
            mom_NET=NET[i:]
            datapath=NET[i:i+mom_NET.find(",")]
            i=i+mom_NET.find(",")+2
            port_id = switch_ports_name(datapath)
            ovsdb_addr(datapath)
            IP_Flag=True
            for index in range(0,len(port_id)):
                if port_id[index]=="s1-eth2" or port_id[index]=="s2-eth2":
                    set_queue(datapath, port_id[index], str(max_rate_queue), "{\"max_rate\": \""+Default+"\"}, {\"max_rate\": \""+Premium+"\"}, {\"min_rate\": \""+Gold+"\"}")
                    port = port_id[index][port_id[index].find("h")+1:]
                    if port_id[index]=="s1-eth2":
                        IP_Destination="10.0.0.11"
                    if port_id[index]=="s2-eth2":
                        IP_Destination="10.0.0.13"
                    set_Telecom_queue(datapath, port, IP_Flag, IP_Destination)
            for index in range(0,len(port_id)):
                if port_id[index]=="s1-eth4" or port_id[index]=="s2-eth3":
                    port = port_id[index][port_id[index].find("h")+1:]
                    if port_id[index]=="s1-eth4":
                        IP_Destination="10.0.0.13"
                    if port_id[index]=="s2-eth3":
                        IP_Destination="10.0.0.11"
                    set_Telecom_queue(datapath, port, IP_Flag, IP_Destination)

    # Import CSV data
    print 'Csv Import'
    serv = ditg.pd.read_csv(ditg.CSV, sep=';', usecols=[0], skiprows=[0]) # serv 0 tx
    time_values = serv.values
    serv = ditg.pd.read_csv(ditg.CSV, sep=';', usecols=[1], skiprows=[0]) # serv 0 tx
    serv_0_tx = serv.values
    serv = ditg.pd.read_csv(ditg.CSV, sep=';', usecols=[2], skiprows=[0]) # serv 0 rx
    serv_0_rx = serv.values
    serv = ditg.pd.read_csv(ditg.CSV, sep=';', usecols=[3], skiprows=[0]) # serv 1 tx
    serv_1_tx = serv.values
    serv = ditg.pd.read_csv(ditg.CSV, sep=';', usecols=[4], skiprows=[0]) # serv 1 rx
    serv_1_rx = serv.values
    serv = ditg.pd.read_csv(ditg.CSV, sep=';', usecols=[5], skiprows=[0]) # serv 2 tx
    serv_2_tx = serv.values
    serv = ditg.pd.read_csv(ditg.CSV, sep=';', usecols=[6], skiprows=[0]) # serv 2 rx
    serv_2_rx = serv.values
    serv = ditg.pd.read_csv(ditg.CSV, sep=';', usecols=[15], skiprows=[0]) # serv 3 tx
    serv_3_tx = serv.values
    serv = ditg.pd.read_csv(ditg.CSV, sep=';', usecols=[16], skiprows=[0]) # serv 3 rx
    serv_3_rx = serv.values
    serv = ditg.pd.read_csv(ditg.CSV, sep=';', usecols=[11], skiprows=[0]) # serv 4 tx
    serv_4_tx = serv.values
    serv = ditg.pd.read_csv(ditg.CSV, sep=';', usecols=[12], skiprows=[0]) # serv 4 rx
    serv_4_rx = serv.values
    serv = ditg.pd.read_csv(ditg.CSV, sep=';', usecols=[7], skiprows=[0]) # serv 5 tx
    serv_5_tx = serv.values
    serv = ditg.pd.read_csv(ditg.CSV, sep=';', usecols=[8], skiprows=[0]) # serv 5 rx
    serv_5_rx = serv.values
    serv = ditg.pd.read_csv(ditg.CSV, sep=';', usecols=[9], skiprows=[0]) # serv 6 tx
    serv_6_tx = serv.values
    serv = ditg.pd.read_csv(ditg.CSV, sep=';', usecols=[10], skiprows=[0]) # serv 6 rx
    serv_6_rx = serv.values
    serv = ditg.pd.read_csv(ditg.CSV, sep=';', usecols=[13], skiprows=[0]) # serv 7 tx
    serv_7_tx = serv.values
    serv = ditg.pd.read_csv(ditg.CSV, sep=';', usecols=[14], skiprows=[0]) # serv 7 rx
    serv_7_rx = serv.values
    
    i = 0
    j = 0
    # pkts
    n = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    # pkts per second
    avg = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    F0=F0_max
    F1=1
    F2=1
    print 'Wait for time alignment'
    wait=ditg.TIME/60
    check_time=False
    while check_time==False:
        now=datetime.datetime.now()
        time.sleep(0.1)
        if now.minute%wait==0:
            check_time=True
            if len(str(now.minute))==1:
                starting_time=str(now.hour)+':0'+str(now.minute)
            else:
                starting_time=str(now.hour)+':'+str(now.minute)
            print starting_time
            k=0
            for index in time_values:
                if index==starting_time:
                    i=k
                    break
                k=k+1
    print 'Starting Time: '+str(time_values[i])
    while j < ditg.SIM_N:
        #calculate the moltiplicators

        if Q0:
            if j%change_values==0:
                if F0==1:
                    F0=F0_max
                else:
                    F0=1
        if Q1:
            if j%change_values==0:
                if F1==1:
                    F1=F1_max
                else:
                    F1=1
        if Q2:
            if j%change_values==0:
                if F2==1:
                    F2=F2_max
                else:
                    F2=1



        # Server start
        print 'Start ITGRecv'
        h1.cmd('ITGRecv &')
        h3.cmd('ITGRecv &')
        time.sleep(2)
        # Sum of packets
        sum_in = 0
        sum_out = 0
        # Serv 0 tx
        n[0] = int(serv_0_tx[i])*F0 / ditg.SCALE + 1
        avg[0] = n[0] / (ditg.TIME-10) + 1
        if avg[0] > 0 and n[0] > 0:
            com = ditg.createCmd_2(dst=ditg.dst,port="10001",tos=ditg.SERV_0,nPkts=str(n[0]),avg=str(avg[0]))
            print(com)
            h1.cmd(com)
            sum_in = sum_in + n[0]

        # Serv 0 rx
        n[0] = int(serv_0_rx[i])*F0 / ditg.SCALE + 1
        avg[0] = n[0] / (ditg.TIME-10) + 1
        if avg[0] > 0 and n[0] > 0:
            com = ditg.createCmd_2(dst=ditg.src,port="10001",tos=ditg.SERV_0,nPkts=str(n[0]),avg=str(avg[0]))
            print(com)
            h3.cmd(com)
            sum_out = sum_out + n[0]

        # Serv 1 tx 
        n[1] = int(serv_1_tx[i])*F0 / ditg.SCALE + 1
        avg[1] = n[1] / (ditg.TIME-10) + 1
        if avg[1] > 0 and n[1] > 0:
            com = ditg.createCmd_2(dst=ditg.dst,port="10002",tos=ditg.SERV_1,nPkts=str(n[1]),avg=str(avg[1]))
            print(com)
            h1.cmd(com)
            sum_in = sum_in + n[1]

        # Serv 1 rx 
        n[1] = int(serv_1_rx[i])*F0 / ditg.SCALE + 1
        avg[1] = n[1] / (ditg.TIME-10) + 1
        if avg[1] > 0 and n[1] > 0:
            com = ditg.createCmd_2(dst=ditg.src,port="10002",tos=ditg.SERV_1,nPkts=str(n[1]),avg=str(avg[1]))
            print(com)
            h3.cmd(com)
            sum_out = sum_out + n[1]

        # Serv 2 tx
        n[2] = int(serv_2_tx[i])*F1 / ditg.SCALE + 1
        avg[2] = n[2] / (ditg.TIME-10) + 1
        if avg[2] > 0 and n[2] > 0:
            com = ditg.createCmd_2(dst=ditg.dst,port="10003",tos=ditg.SERV_2,nPkts=str(n[2]),avg=str(avg[2]))
            print(com)
            h1.cmd(com)
            sum_in = sum_in + n[2]

        # Serv 2 rx
        n[2] = int(serv_2_rx[i])*F1 / ditg.SCALE + 1
        avg[2] = n[2] / (ditg.TIME-10) + 1
        if avg[2] > 0 and n[2] > 0:
            com = ditg.createCmd_2(dst=ditg.src,port="10003",tos=ditg.SERV_2,nPkts=str(n[2]),avg=str(avg[2]))
            print(com)
            h3.cmd(com)
            sum_out = sum_out + n[2]

        # Serv 3 tx
        n[3] = int(serv_3_tx[i])*F0 / ditg.SCALE + 1
        avg[3] = n[3] / (ditg.TIME-10) + 1
        if avg[3] > 0 and n[3] > 0:
            com = ditg.createCmd_2(dst=ditg.dst,port="10004",tos=ditg.SERV_3,nPkts=str(n[3]),avg=str(avg[3]))
            print(com)
            h1.cmd(com)
            sum_in = sum_in + n[3]

        # Serv 3 rx
        n[3] = int(serv_3_rx[i])*F0 / ditg.SCALE + 1
        avg[3] = n[3] / (ditg.TIME-10) + 1
        if avg[3] > 0 and n[3] > 0:
            com = ditg.createCmd_2(dst=ditg.src,port="10004",tos=ditg.SERV_3,nPkts=str(n[3]),avg=str(avg[3]))
            print(com)
            h3.cmd(com)
            sum_out = sum_out + n[3]

        # Serv 4 tx
        n[4] = int(serv_4_tx[i])*F1 / ditg.SCALE + 1
        avg[4] = n[4] / (ditg.TIME-10) + 1
        if avg[4] > 0 and n[4] > 0:
            com = ditg.createCmd_2(dst=ditg.dst,port="10005",tos=ditg.SERV_4,nPkts=str(n[4]),avg=str(avg[4]))
            print(com)
            h1.cmd(com)
            sum_in = sum_in + n[4]

        # Serv 4 rx
        n[4] = int(serv_4_rx[i])*F1 / ditg.SCALE + 1
        avg[4] = n[4] / (ditg.TIME-10) + 1
        if avg[4] > 0 and n[4] > 0:
            com = ditg.createCmd_2(dst=ditg.src,port="10005",tos=ditg.SERV_4,nPkts=str(n[4]),avg=str(avg[4]))
            print(com)
            h3.cmd(com)
            sum_out = sum_out + n[4]

        # Serv 5 tx
        n[5] = int(serv_5_tx[i])*F2 / ditg.SCALE + 1
        avg[5] = n[5] / (ditg.TIME-10) + 1
        if avg[5] > 0 and n[5] > 0:
            com = ditg.createCmd_2(dst=ditg.dst,port="10006",tos=ditg.SERV_5,nPkts=str(n[5]),avg=str(avg[5]))
            print(com)
            h1.cmd(com)
            sum_in = sum_in + n[5]

        # Serv 5 rx
        n[5] = int(serv_5_rx[i])*F2 / ditg.SCALE + 1
        avg[5] = n[5] / (ditg.TIME-10) + 1
        if avg[5] > 0 and n[5] > 0:
            com = ditg.createCmd_2(dst=ditg.src,port="10006",tos=ditg.SERV_5,nPkts=str(n[5]),avg=str(avg[5]))
            print(com)
            h3.cmd(com)
            sum_out = sum_out + n[5]

        # Serv 6 tx
        n[6] = int(serv_6_tx[i])*F1 / ditg.SCALE + 1
        avg[6] = n[6] / (ditg.TIME-10) + 1
        if avg[6] > 0 and n[6] > 0:
            com = ditg.createCmd_2(dst=ditg.dst,port="10007",tos=ditg.SERV_6,nPkts=str(n[6]),avg=str(avg[6]))
            print(com)
            h1.cmd(com)
            sum_in = sum_in + n[6]

        # Serv 6 rx
        n[6] = int(serv_6_rx[i])*F1 / ditg.SCALE + 1
        avg[6] = n[6] / (ditg.TIME-10) + 1
        if avg[6] > 0 and n[6] > 0:
            com = ditg.createCmd_2(dst=ditg.src,port="10007",tos=ditg.SERV_6,nPkts=str(n[6]),avg=str(avg[6]))
            print(com)
            h3.cmd(com)
            sum_out = sum_out + n[6]


        # Serv 7 tx
        n[7] = int(serv_7_tx[i])*F1 / ditg.SCALE + 1
        avg[7] = n[7] / (ditg.TIME-10) + 1
        if avg[7] > 0 and n[7] > 0:
            com = ditg.createCmd_2(dst=ditg.dst,port="10008",tos=ditg.SERV_7,nPkts=str(n[7]),avg=str(avg[7]))
            print(com)
            h1.cmd(com)
            sum_in = sum_in + n[7]

        # Serv 7 rx
        n[7] = int(serv_7_rx[i])*F1 / ditg.SCALE + 1
        avg[7] = n[7] / (ditg.TIME-10) + 1
        if avg[7] > 0 and n[7] > 0:
            com = ditg.createCmd_2(dst=ditg.src,port="10008",tos=ditg.SERV_7,nPkts=str(n[7]),avg=str(avg[7]))
            print(com)
            h3.cmd(com)
            sum_out = sum_out + n[7]

        j = j+1
        i=i+1
        if i % ditg.SIZE==0 and i!=0:
            i=0
        print i
        print('Sum of Packets IN: ' + str(sum_in))
        print('Sum of Packets OUT: ' + str(sum_out))

	time.sleep(61)
        check_time=False
        while check_time==False:
            now=datetime.datetime.now()
            if now.minute%wait==0:
                check_time=True
                print "Time: "+str(now)
                print 'Database Time: '+str(time_values[i])
            else:
                time.sleep(1)
        h1.cmd('kill %ITGSend')
        h1.cmd('kill %ITGRecv')
    CLI(net)
    net.stop()

if __name__=='__main__':
    setLogLevel( 'info' )
    myNetwork()
