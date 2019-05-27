#!/usr/bin/env python
"""
Python script for operating on traffic lights module for a raspberry pi via MQTT
"""

# pylint: disable=no-member
# pylint: disable=unused-argument

import argparse
import ConfigParser as configparser
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt

MQTT_INI = "/etc/mqtt.ini"
MQTT_SEC = "mqtt"

def setup_lights():
    """ Setup GPIO output"""
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(9, GPIO.OUT)
    GPIO.setup(10, GPIO.OUT)
    GPIO.setup(11, GPIO.OUT)

def all_lights_off():
    """Turn off all lights when program shuts down"""
    GPIO.output(9, False)
    GPIO.output(10, False)
    GPIO.output(11, False)
    GPIO.cleanup()

def on_connect(client, userdata, flags, rc):
    """On connecting to the MQTT broker, subscribe to a topic in userdata"""
    print "Connected with rc: " + str(rc)
    #client.subscribe("srp/demo/led")
    client.subscribe(userdata)

def on_message(client, userdata, msg):
    """Process a message and take action"""
    print "Topic: " + msg.topic + "\nMessage: "+ str(msg.payload)
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

def main():
    """Main program function, parse arguments, read configuration,
    setup client, listen for messages"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', default=MQTT_INI, help="configuration file")
    parser.add_argument('-s', '--section', default=MQTT_SEC, help="configuration file section")
    parser.add_argument('-d', '--detach', action='store_true',
                        help="fork and detach process, run as daemon")
    parser.add_argument('-v', '--verbose', action='store_true', help="verbose messages")
    args = parser.parse_args()

    mqtt_conf = configparser.ConfigParser()
    mqtt_conf.read(args.config)

    mqtt_client = mqtt.Client(userdata=mqtt_conf.get(args.section, 'topic'))
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    if (mqtt_conf.has_option(args.section, 'username') and
            mqtt_conf.has_option(args.section, 'password')):
        username = mqtt_conf.get(args.section, 'username')
        password = mqtt_conf.get(args.section, 'password')
        mqtt_client.username_pw_set(username=username, password=password)

    host = mqtt_conf.get(args.section, 'host')
    port = int(mqtt_conf.get(args.section, 'port'))

    mqtt_client.connect(host, port, 60)

    setup_lights()

    # Loop forever
    try:
        mqtt_client.loop_forever()
    # Catches SigINT
    except KeyboardInterrupt:
        all_lights_off()
        mqtt_client.disconnect()
        print "Exiting main thread"

if __name__ == '__main__':
    main()
