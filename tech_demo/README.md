# Tech Demo Software

The software hosted here serves to:

 * Provide a proof of concept of the software architecture
 * Evaluate the Raspberry Pi Zero's performance
 * Assist the hardware team test out various hardware components quickly
 * Provide a starting point for software development

## Deployment Instructions

#### Get Raspbian running
* Burn an SD card with [Raspbian Jessy](https://www.raspberrypi.org/downloads/raspbian/)
* Boot and run through ```raspi-config``` expanding the filesystem, setting your locale and time zone, etc.
* ```reboot```

#### Update and set up the 1-wire interface for a temp sensor
* ```sudo apt-get update```
* ```sudo apt-get upgrade```
* Edit ```/boot/config.txt``` and a line at the end: 
```
dtoverlay=w1-gpio
``` 
If you want to use a pin other than GPIO 4 for a 1-wire temperature sensor, you can override the pin number by adding: 
```
dtoverlay=w1-gpio,gpiopin=27
```
* Edit ```/etc/modules``` and add the following two lines 
```
w1-gpio
w1-therm
```
* ```reboot```

#### Install prerequisites
* ```sudo apt-get install python-dev nginx-full uwsgi uwsgi-plugin-python``` Installing python-dev before Flask allows some of Flask's dependencies to compile native code optimizations for the Raspberry Pi
* ```sudo pip install flask gpiozero uwsgidecorators```

#### Run
* ```cd ~```
* ```git clone https://github.com/TheDukeZip/4tvc.git```
* Open a terminal and ```cd /home/pi/4tvc/tech_demo/services``` then run ```./run_services.sh```
* Open a terminal and run ```sudo nginx -c /home/pi/4tvc/tech_demo/diagnosticui/nginx.conf```
We'll integrate the real software with the built in services, this is just a quick and dirty way to get things running
* Open a browser to ```http://localhost:7000``` If all goes well you should see everything up and running!

#### Connecting Hardware
By default the hardware is connected to the following pins. In a future revision all the pins will be configurable through one config file. For now if you want to change them, edit the service code in ```/home/pi/4tvc/techdemo/services```

I tried to stay away from using any pins that serve a dual-purpose (SPI, UART, HW PWM, etc) so we can reserve them for future use.

* Syringe 1 motor forward: ```5```
* Syringe 1 motor reverse: ```6```
* Syringe 2 motor forward: ```23```
* Syringe 2 motor reverse: ```24```

Connect one end of the switches to ground, and the other to GPIO Pins:
* Syringe 1 forward stop: ```17```
* Syringe 1 reverse stop: ```27```
* Syringe 2 forward stop: ```22```
* Syringe 2 reverse stop: ```26```

* Stirrer: ```25``` If using an LED, don't forget a current limiting resistor

* Heater: ```16``` If using an LED, don't forget a current limiting resistor
* Temperature Sensor: ```4``` (Works minimally for 1-wire DS18B20 chipsets)


## Notes

There's a few spots to make the code more elegent, namely defining our own classes for the hardware. This code was quick and dirty - hoping to refactor a bit when I have some spare cycles.

The deployment is kinda manual, real code will be much simpler!


## Stubs

fivetwentysix suggested having some stubs for the services so he can play with this on the desktop. He also suggested setting it up in a docker container. The stubs are available but docker container is not.

* ```sudo apt-get install python-dev nginx-full```
* ```sudo pip install flask flask-cors``` 

* Pull latest code from github

* Edit ```4tvc/tech_demo/services_stubs/nginx.conf``` to have the directory where your wwwroot is located (the one within ```4tvc/tech_demo/services_stubs```
* Open four terminal windows and run one of the following in each:
  * ```4tvc/tech_demo/services_stubs/syringe_service.py```
  * ```4tvc/tech_demo/services_stubs/stirrer_service.py```
  * ```4tvc/tech_demo/services_stubs/heater_service.py```
  * ```nginx -c 4tvc/tech_demo/services_stubs/nginx.conf```

* Open a browser to ```http://localhost:7001``` and you should be able to play with the services


