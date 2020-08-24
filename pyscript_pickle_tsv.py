import pandas as pd
import numpy as np
from datetime import date
import sys
import os

# print('Number of arguments passed: ',len(sys.argv))
currentDir = os.getcwd()
if len(sys.argv) == 4:
  thisdate=str(sys.argv[1])
  filenameSrc=str(sys.argv[2])
  filenameDest=str(sys.argv[3])
else:
  if len(sys.argv) == 2:
    thisdate=sys.argv[1]
  else:
    thisdate=str(date.today())
  filenameDest=currentDir+'/data/interim/'+thisdate+'.pkl'
  filenameSrc=currentDir+'/data/interim/'+thisdate+'.tsv'

#I imagine this should impact the size of resulting pickled Df
resampleFreq = '30S'

#If .TSV file exists, pickle it & save
if os.path.isfile(filenameSrc):
  df = pd.read_csv(filenameSrc, sep='\t', header=0).set_index('record_id')
  #print('Imported: ' + filenameSrc)

  #Preprocess: remove un-used column
  df.drop('when_stored', axis=1, inplace=True)

  #Preprocess: change datatypes
  df['when_day_time'] = pd.to_datetime(df['when_day_time'])
  df[['tempF','humidity']] = df[['tempF', 'humidity']].astype('float64')
  
  #Preprocess: pivoting dataframe
  resamp = df.pivot(index='when_day_time', columns='sensor_id', values=['tempF', 'humidity']).resample(resampleFreq)
  newDf = resamp.agg(np.nanmean)

  #Preprocess: PICKLE!
  newDf.to_pickle(filenameDest)
  print(newDf.tail(10))

  #Output whether successful
  if os.path.isfile(filenameDest):
    print('Exported: ' + filenameDest)
  else:
    print('Tried to pickle but file didnt create: ' + filenameDest)
#Otherwise, no such TSV file exists yet
else:
  print('No such file: ' + filenameSrc)

