#!/usr/bin/env python

import paho.mqtt.client as mqtt
import ConfigParser as configparser
import RPi.GPIO as GPIO
import signal
import sys

MQTT_INI="/etc/mqtt.ini"
MQTT_SEC="mqtt"

# Turn off all lights when user ends demo
def allLightsOff():
    GPIO.output(9, False)
    GPIO.output(10, False)
    GPIO.output(11, False)
    GPIO.cleanup()

def on_connect(client, userdata, flags, rc):
    print ("Connected with rc: " + str(rc))
    #client.subscribe("srp/demo/led")
    client.subscribe(userdata)

def on_message(client, userdata, msg):
    print ("Topic: "+ msg.topic+"\nMessage: "+str(msg.payload))
    if "green" in msg.payload:
        #print("  Green on!")
        GPIO.output(11, True)
    else:
        #print("  Green off!")
        GPIO.output(11, False)
    if "yellow" in msg.payload:
        #print("  Yellow on!")
        GPIO.output(10, True)
    else:
        #print("  Yellow off!")
        GPIO.output(10, False)
    if "red" in msg.payload:
        #print("  Red on!")
        GPIO.output(9, True)
    else:
        #print("  Red off!")
        GPIO.output(9, False)
        
mqttConf = configparser.ConfigParser()
mqttConf.read(MQTT_INI)

client = mqtt.Client(userdata=mqttConf.get(MQTT_SEC, 'topic'))
client.on_connect = on_connect
client.on_message = on_message

#if MQTT_USER is not None and MQTT_PASS is not None:
#    print('Using username: {un} and password: {pw}'.format(un=MQTT_USER, pw='*' * len(MQTT_PASS)))
#client.username_pw_set(username=MQTT_USER, password=MQTT_PASS)
client.username_pw_set(username=mqttConf.get(MQTT_SEC, 'username'), password=mqttConf.get(MQTT_SEC, 'password'))
client.connect(mqttConf.get(MQTT_SEC, 'host'), int(mqttConf.get(MQTT_SEC, 'port')), 60)

GPIO.setmode(GPIO.BCM)
GPIO.setup(9, GPIO.OUT)
GPIO.setup(10, GPIO.OUT)
GPIO.setup(11, GPIO.OUT)

# Loop forever
try:
    client.loop_forever()
# Catches SigINT
except KeyboardInterrupt:
    allLightsOff()
    global exit_me
    exit_me = True
    client.disconnect()
    print("Exiting main thread")
