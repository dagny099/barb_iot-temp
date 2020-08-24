#!/bin/bash
source $HOME/.profile

if [ $# -lt 2 ]; then
  dbname='temp_project'
  configfile="${HOME}/keys/configMysql.cnf"
  pathnameDest="${HOME}/temp_project/data/interim/"
fi

if [ $# -lt 1 ]; then
  thisdate=$(date +'%Y-%m-%d')
else
  thisdate=$1
fi
filenameSrc="$pathnameDest${thisdate}.tsv"
filenameDest="$pathnameDest${thisdate}.pkl"

#echo $filenameSrc
#echo $filenameDest
#echo $configfile

#1- Chop day's db data into TSV file
echo "SELECT * FROM sensor_readings WHERE when_day_time LIKE '"$thisdate"%' ORDER BY when_day_time DESC;" | mysql --defaults-extra-file=$configfile $dbname > $filenameSrc
echo "SELECT COUNT(*) FROM sensor_readings WHERE when_day_time LIKE '"$thisdate"%';" | mysql --defaults-extra-file=$configfile $dbname

#2- From python, pickle the TSV file and delete it
python3 $HOME/temp_project/pyscript_pickle_tsv.py "$thisdate" "$filenameSrc"  "$filenameDest"
rm $filenameSrc
