#!/bin/bash

python heater_service.py &
python syringe_service.py &
python stirrer_service.py &
nginx
