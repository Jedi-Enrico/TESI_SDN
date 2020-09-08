
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
import psutil
import SDL_DS1307


def f1():
    IP_SRC='169.254.207.222'
    IP_DST = "169.254.181.98"
    os.system('sudo ifconfig eth0 '+IP_SRC+' netmask 255.255.0.0')
    ds1307 = SDL_DS1307.SDL_DS1307(1, 0x68)
    time.sleep(2)
    now=ds1307.read_datetime()
    str_time='"'+str(now.year)+'-'+str(now.month)+'-'+str(now.day)+' '+str(now.hour)+':'+str(now.minute)+':'+str(now.second)+'"'
    os.system('sudo date --set '+str_time)

    print ('Csv Import')
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
    ### pkts
    n = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    # pkts per second
    avg = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    F0_max=2
    F0=F0_max
    F1=1
    F2=1
    print ('Wait for time alignment')
    wait=ditg.TIME/60
    check_time=False
    while check_time==False:
        now=datetime.datetime.now()
        time.sleep(0.1)
        try:
            if now.minute%wait==0:
                check_time=True
                if len(str(now.minute))==1:
                    starting_time=str(now.hour)+':0'+str(now.minute)
                else:
                    starting_time=str(now.hour)+':'+str(now.minute)
                print (starting_time)
                k=0
                for index in time_values:
                    if index==starting_time:
                        i=k
                        break
                    k=k+1
            else:
                time.sleep(0.5)
        except:
            time.sleep(0.1)
    print ('Starting Time: '+str(time_values[i]))
    while j < ditg.SIM_N:
        try:
            now=datetime.datetime.now()
            if len(str(now.minute))==1:
                starting_time=str(now.hour)+':0'+str(now.minute)
            else:
                starting_time=str(now.hour)+':'+str(now.minute)
                
                if starting_time==time_values[1]:
                    print (starting_time)
                else:
                    k=0
                    for index in time_values:
                        if index==starting_time:
                            i=k
                            break
                        k=k+1
        except:
            time.sleep(0.1)
        time.sleep(4)
        # Sum of packets
        sum_in = 0
        sum_out = 0


        # Serv 0 rx
        n[0] = int(serv_0_rx[i])*F0 / ditg.SCALE + 1
        avg[0] = n[0] / (ditg.TIME-10) + 1
        if avg[0] > 0 and n[0] > 0:
            com = ditg.createCmd_2(dst=IP_DST,port="10001",tos=ditg.SERV_0,nPkts=str(n[0]),avg=str(avg[0]))
            print(com)
            os.popen(com)
            sum_out = sum_out + n[0]

        # Serv 1 rx 
        n[1] = int(serv_1_rx[i])*F0 / ditg.SCALE + 1
        avg[1] = n[1] / (ditg.TIME-10) + 1
        if avg[1] > 0 and n[1] > 0:
            com = ditg.createCmd_2(dst=IP_DST,port="10002",tos=ditg.SERV_1,nPkts=str(n[1]),avg=str(avg[1]))
            print(com)
            os.popen(com)
            sum_out = sum_out + n[1]

        # Serv 2 rx
        n[2] = int(serv_2_rx[i])*F1 / ditg.SCALE + 1
        avg[2] = n[2] / (ditg.TIME-10) + 1
        if avg[2] > 0 and n[2] > 0:
            com = ditg.createCmd_2(dst=IP_DST,port="10003",tos=ditg.SERV_2,nPkts=str(n[2]),avg=str(avg[2]))
            print(com)
            os.popen(com)
            sum_out = sum_out + n[2]

        # Serv 3 rx
        n[3] = int(serv_3_rx[i])*F0 / ditg.SCALE + 1
        avg[3] = n[3] / (ditg.TIME-10) + 1
        if avg[3] > 0 and n[3] > 0:
            com = ditg.createCmd_2(dst=IP_DST,port="10004",tos=ditg.SERV_3,nPkts=str(n[3]),avg=str(avg[3]))
            print(com)
            os.popen(com)
            sum_out = sum_out + n[3]

        # Serv 4 rx
        n[4] = int(serv_4_rx[i])*F1 / ditg.SCALE + 1
        avg[4] = n[4] / (ditg.TIME-10) + 1
        if avg[4] > 0 and n[4] > 0:
            com = ditg.createCmd_2(dst=IP_DST,port="10005",tos=ditg.SERV_4,nPkts=str(n[4]),avg=str(avg[4]))
            print(com)
            os.popen(com)
            sum_out = sum_out + n[4]

        # Serv 5 rx
        n[5] = int(serv_5_rx[i])*F2 / ditg.SCALE + 1
        avg[5] = n[5] / (ditg.TIME-10) + 1
        if avg[5] > 0 and n[5] > 0:
            com = ditg.createCmd_2(dst=IP_DST,port="10006",tos=ditg.SERV_5,nPkts=str(n[5]),avg=str(avg[5]))
            print(com)
            os.popen(com)
            sum_out = sum_out + n[5]

        # Serv 6 rx
        n[6] = int(serv_6_rx[i])*F1 / ditg.SCALE + 1
        avg[6] = n[6] / (ditg.TIME-10) + 1
        if avg[6] > 0 and n[6] > 0:
            com = ditg.createCmd_2(dst=IP_DST,port="10007",tos=ditg.SERV_6,nPkts=str(n[6]),avg=str(avg[6]))
            print(com)
            os.popen(com)
            sum_out = sum_out + n[6]

        # Serv 7 rx
        n[7] = int(serv_7_rx[i])*F1 / ditg.SCALE + 1
        avg[7] = n[7] / (ditg.TIME-10) + 1
        if avg[7] > 0 and n[7] > 0:
            com = ditg.createCmd_2(dst=IP_DST,port="10008",tos=ditg.SERV_7,nPkts=str(n[7]),avg=str(avg[7]))
            print(com)
            os.popen(com)
            sum_out = sum_out + n[7]

        j = j+1
        i=i+1
        if i % ditg.SIZE==0 and i!=0:
            i=0
        print (i)
        print('Sum of Packets OUT: ' + str(sum_out))

        ##Wait next minute to avoid another detection
        check_time=False
        while check_time==False:
            now=datetime.datetime.now()
            try:
                if (now.minute== 4 or now.minute==17 or now.minute==31 or now.minute==41 or now.minute==54) and now.second==0:
                    now=ds1307.read_datetime()
                    str_time='"'+str(now.year)+'-'+str(now.month)+'-'+str(now.day)+' '+str(now.hour)+':'+str(now.minute)+':'+str(now.second)+'"'
                    os.system('sudo date --set '+str_time)
                    now=datetime.datetime.now()
                if now.minute%wait==1:
                    check_time=True
                else:
                    time.sleep(1)
            except:
                time.sleep(0.1)
                
        check_time=False
        while check_time==False:
            now=datetime.datetime.now()
            try:
                if (now.minute== 4 or now.minute==17 or now.minute==31 or now.minute==41 or now.minute==54) and now.second==0:
                    now=ds1307.read_datetime()
                    str_time='"'+str(now.year)+'-'+str(now.month)+'-'+str(now.day)+' '+str(now.hour)+':'+str(now.minute)+':'+str(now.second)+'"'
                    os.system('sudo date --set '+str_time)
                    now=datetime.datetime.now()
                if now.minute%wait==0:
                    check_time=True
                    print ("Time: "+str(now))
                    print ('Database Time: '+str(time_values[i]))
                else:
                    time.sleep(1)
            except:
                time.sleep(0.1)
        try:
            
            cmd = "pidof ITGRecv"
            PID = subprocess.check_output(cmd, shell=True).decode("utf-8")
            print ("pidof ITGRecv: "+str(PID))
            os.popen('sudo kill -9 '+str(PID))
            cmd = "pidof ITGSend"
            PID = subprocess.check_output(cmd, shell=True).decode("utf-8")
            print ("pidof ITGSend: "+str(PID))
            os.popen('sudo kill -9 '+str(PID))
        except:
            time.sleep(0.1)

def f2():
    while True:
        try:
            print("Start ITGRecv")
            os.popen('ITGRecv')
        except:
            time.sleep(1)
t1 = threading.Thread(target=f1, args=())
t2 = threading.Thread(target=f2, args=())
 
#Started the threads
t1.start()
time.sleep(4)
t2.start()
 
#Joined the threads
t1.join()
t2.join()
