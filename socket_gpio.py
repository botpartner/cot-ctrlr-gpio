#coding:utf-8

import socket, sys
import json
import RPi.GPIO
import logging
import time

#Loggin parameter
LOG_PATH='/var/log/socketGPIO.log'
Test_LOG_PATH='/var/log/test_socketGPIO.log'
LOG_FORMAT='[%(levelname)s] - %(message)s - %(name)s - %(asctime)s'

#Json format for __YOUR_COT_SMQ_DOMAINNAME__:__YOUR_COT_SMQ_PORT__
server ='__YOUR_COT_SMQ_DOMAINNAME__'
port = __YOUR_COT_SMQ_PORT__
SocketTimeout=1
vendor = '__YOUR_VENDER_ID__'
device = '__YOUR_DEVICE_ID__'
token  = '__YOUR_COT_SMQ_TOKEN__'
send_string={
    'vendor': vendor,
    'device': device,
    'uuid'  : '__YOUR_DEVICE_UUID__',
    'token' :  token,
    'action': 'update'
    }

# pin define
Led_0= 2
Led_1= 3
Led_2= 4
Led_3= 17
Led_4= 27
Led_5= 22
Led_6= 10
Led_7= 9
Led_8= 11
Led_9= 8

#RPi GPIO mode setting.
RPi.GPIO.setmode(RPi.GPIO.BCM)
RPi.GPIO.setwarnings(False)
RPi.GPIO.setup(Led_0, RPi.GPIO.OUT)
RPi.GPIO.setup(Led_1, RPi.GPIO.OUT)
RPi.GPIO.setup(Led_2, RPi.GPIO.OUT)
RPi.GPIO.setup(Led_3, RPi.GPIO.OUT)
RPi.GPIO.setup(Led_4, RPi.GPIO.OUT)
RPi.GPIO.setup(Led_5, RPi.GPIO.OUT)
RPi.GPIO.setup(Led_6, RPi.GPIO.OUT)
RPi.GPIO.setup(Led_7, RPi.GPIO.OUT)
RPi.GPIO.setup(Led_8, RPi.GPIO.OUT)
RPi.GPIO.setup(Led_9, RPi.GPIO.OUT)

logging.basicConfig(level=logging.WARNING,filename=LOG_PATH,format=LOG_FORMAT)     # This is for normal operation.
#logging.basicConfig(level=logging.INFO,filename=Test_LOG_PATH,format=LOG_FORMAT)  # This is for Debug it will record every meassage and will prduce very large log file.
logger=logging.getLogger()


def init():
    global sock
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(SocketTimeout)
    except socket.error, msg:
        logging.error("[ERROR 1] %s\n" % msg[0])
        time.sleep(1)
	return -1
    return 1

def connect():
    try:
        sock.connect((server,port))
    except socket.timeout:
        logging.warning("Connect Timeout")
        return 2 #Time out reconnect
    except socket.error, msg:
        #print "ERROR connect "
        #print msg,"\n"
        return -1   # Do close and init
    return 1

def create_daemon():
    import os, sys, time

    try:
        pid =os.fork()
        if pid >0:sys.exit(0)
    except OSError, error:
        logging.warning("socketGPIO_daemon fork 1 failed !")
        sys.exit(1)

    os.chdir("/")
    os.setsid()
    os.umask(0)

    try:
        pid = os.fork()
        if pid >0:sys.exit(0)
    except OSError,error:
        logging.warning("socketGPIO_daemon fork 2 failed")
        sys.exit(1)

    main()

def close():
    sock.close()

def recv():
    try:
        recv_string=json.loads(sock.recv(1024))
        #print recv_string
    except socket.timeout:
        logging.warning("Timeout")
        return
    except socket.error:
	logging.warning("recv sock error")
        return
    except ValueError:
        logging.warning("recv Value error")
	close()
        return



    if recv_string['token'] ==token :
        RPi.GPIO.output(Led_0,recv_string['data']['0'])
        RPi.GPIO.output(Led_1,recv_string['data']['1'])
        RPi.GPIO.output(Led_2,recv_string['data']['2'])
        RPi.GPIO.output(Led_3,recv_string['data']['3'])
        RPi.GPIO.output(Led_4,recv_string['data']['4'])
        RPi.GPIO.output(Led_5,recv_string['data']['5'])
        RPi.GPIO.output(Led_6,recv_string['data']['6'])
        RPi.GPIO.output(Led_7,recv_string['data']['7'])
        RPi.GPIO.output(Led_8,recv_string['data']['8'])
        RPi.GPIO.output(Led_9,recv_string['data']['9'])
        logging.info("Success")
    else:
        logging.warning("Token is wrong !")

def reinit():
    while True:
        if init()==1:
            return 1
        time.sleep(1)
        logging.info("reIniting")

def reconnect():
    while True:
        value= connect()
        if value==1:
            return 1
        elif value== -1:
            close()
            reinit()
        time.sleep(1)
        logging.info("reconnenct")

def main():
    #import socket, sys , time, logging

    while True:
        if init()>0:
            #print "Init"
            break;
        reinit()

    while True:
        if connect()>0:
            #print "connect"
            break;
        reconnect()

    #print "start"
    while True:

        try:
            sock.send(json.dumps(send_string))
        except socket.error:
            close()
            while True:
                if init()==1:
                    break
                time.sleep(1)
                logging.info( "Initing")
            logging.info("Do init")
            while True:
                value = connect()
                if value==1:
                    break
                elif value==2:
                    reconnect()
                    break
                elif value==-1:
                    logging.info("closing")
                    break
            logging.info("Do Connect")

        recv()
        #close()
        time.sleep(1)
if __name__ == '__main__':
    create_daemon()
