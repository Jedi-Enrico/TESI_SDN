#!/usr/bin/python  
import serial
import time  
import datetime  
import os

os.popen("sudo chmod a+rw /dev/ttyACM0", 'w').write("Ao70pa45")


def read_all(port, chunk_size=200):
    """Read all characters on the serial port and return them."""
    if not port.timeout:
        raise TypeError('Port needs to have a timeout set!')

    read_buffer = b''

    while True:
        # Read in chunks. Each chunk will wait as long as specified by
        # timeout. Increase chunk_size to fail quicker
        byte_chunk = port.read(size=chunk_size)
        read_buffer += byte_chunk
        if not len(byte_chunk) == chunk_size:
            break

    return read_buffer

#'COM3'
ser = serial.Serial(
    port = '/dev/ttyACM0',
    baudrate = 115200,
    parity = serial.PARITY_NONE,
    stopbits = serial.STOPBITS_ONE,
    bytesize = serial.EIGHTBITS,
    timeout=0.5, # IMPORTANT, can be lower or higher
    inter_byte_timeout=0.1 # Alternative
    )   
time.sleep(5)
flag = 0;   
first_loop=0;
bufsize=0;  
while True:  
        ts = datetime.datetime.now();  

        sec_mom=ts.second;
        minute_mom=ts.minute;
        hour_mom=ts.hour;
        DAY_mom=ts.day;
        MONTH_mom=ts.month;
        YEAR=str(ts.year);
        
        if sec_mom<10:
            sec='0'+str(ts.second);
        else:
            sec=str(ts.second);
        if minute_mom<10:
            minute='0'+str(ts.minute);
        else:
            minute=str(ts.minute);
        if hour_mom<10:
            hour='0'+str(ts.hour);
        else:
            hour=str(ts.hour);
        if DAY_mom<10:
            DAY='0'+str(ts.day);
        else:
            DAY=str(ts.day);
        if MONTH_mom<10:
            MONTH='0'+str(ts.month);
        else:
            MONTH=str(ts.month);

        DATA=YEAR+' '+MONTH+' '+DAY+' '+hour+' '+minute+' '+sec;
        
        if minute_mom%13==0 and sec_mom==0:
            flag=0;
        if flag==0:
	    if first_loop==0:
                print("Time aligned at:")
                print(DATA)
                first_loop=1
	               
            ser.write(DATA.encode()) #Send data to arduino. Activate arduino read pin and write to serial  
            time.sleep(2)
            byteData = read_all(ser) 
            if byteData.decode("utf-8")=="1":
                flag=1;
            else:
                print("ERROR--->resend data")
                flag=0;
            time.sleep(1)
        else:
            time.sleep(0.2)
