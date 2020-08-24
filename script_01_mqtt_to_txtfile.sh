#!/bin/bash
source $HOME/.profile
if [ $# -lt 1 ]; then
  subscribe_topic=arabrab/nifi;  #arabrab/sensors
  broker=broker.mqtt-dashboard.com;
  pathname=$HOME/temp_project/data/raw/
  filename=$pathname$(date +'%Y-%m-%d'.'txt')
fi

#-----------
# Subscribe to topic
#-----------
mosquitto_sub -h $broker -t $subscribe_topic >> $filename
