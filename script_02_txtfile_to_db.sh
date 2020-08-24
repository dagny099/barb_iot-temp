#!/bin/bash
source $HOME/.profile
#-----------
# Write to db
#-----------
dbname=$1
if [ $# -lt 2 ]; then
  dbname='temp_project';
  tblname='sensor_readings';
  configfile="${HOME}/keys/configMysql.cnf"
  pathname="${HOME}/temp_project/data/raw/"
fi

if [ $# -lt 1 ]; then
  filename=$pathname$(date +'%Y-%m-%d'.'txt')
else
  filename="$pathname$1.txt"
fi

#echo $filename
#echo $configfile
#-----------
#READ TXT FILE:
#-----------

mysql --defaults-extra-file=$configfile $dbname --local-infile=1 <<EOF

LOAD DATA LOCAL INFILE '$filename'
IGNORE
INTO TABLE sensor_readings 
FIELDS TERMINATED BY ',' 
LINES TERMINATED BY '\n' 
(sensor_id,location_id,when_day_time,tempF,humidity,@dvar);

EOF


