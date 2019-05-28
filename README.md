[![Build Status](https://travis-ci.org/Scott8586/TrafficLight.svg?branch=master)](https://travis-ci.org/Scott8586/TrafficLight)

## MQTT Traffic Light

Python code for controlling a Rasperry Pi [Traffic Light LED](https://www.amazon.com/Pi-Traffic-Light-Raspberry-pack/dp/B00RIIGD30) stack
from [low voltage labs](http://lowvoltagelabs.com), using paho MQTT.
The main script connects to a MQTT broker, listens for commands on a designated topic, and operates the LEDs of the Traffic Light accordingly.


### Requirements

	paho.mqtt
	RPi.GPIO

These can be installed like so:

```
sudo pip install paho-mqtt
sudo pip install RPi.GPIO
```

### Example

Use the [example configuration file](mqtt.ini.example) to test the operation.
The IP address is associated witha free MQTT broker, so don't publish anything
sensitive.  The code needs to be run as root in order for the GPIO code to access
/dev/mem under normal circumstances.

```
sudo python traffic_light.py -c mqtt.ini.example
```

Then communicate with a mosquitto_client:

```
mosquitto_pub -h 85.119.83.194 -t pi/demo/led -m green
mosquitto_pub -h 85.119.83.194 -t pi/demo/led -m off
```

You should see your green traffic light LED turn on, then off with the different messages.

