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
