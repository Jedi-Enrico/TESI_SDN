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

while True:
    try:
        print("Start ITGRecv")
        os.popen('ITGRecv')
    except:
        time.sleep(1)
