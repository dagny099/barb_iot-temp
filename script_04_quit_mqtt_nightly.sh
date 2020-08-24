#!/bin/bash

#-----------
# Kill the mosquitto process just before midnight
#-----------
kill $(pgrep -fa mosquitto_sub | awk '{ print $1 }')
