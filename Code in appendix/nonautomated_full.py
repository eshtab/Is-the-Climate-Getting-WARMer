#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# data quality check


# In[ ]:


import pandas as pd
import datetime as dt
import numpy as np
import csv
import calendar

import dash
import dash_core_components as dcc
import dash_html_components as html

import os,sys,inspect
from dash.dependencies import Input, Output

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
from environmentVariables import environment_variables


# In[ ]:


climate=pd.read_excel(user_key['observed_raw_unclean']+'climate-daily-weatherstats.xlsx',sheet_name=1)
power=pd.read_csv(user_key['observed_raw_unclean']+'POWER-airportlocation.csv')


# In[ ]:


#drop all columns in climate except for, 
#Date, precipitation, avg_hourly_pressure_station,All Sky Surface Longwave Downward Irradiance
#ALLSKY_SFC_LW_DWN, avg_hourly_wind_speed,max_wind_speed, avg_hourly_temperature, max_temperature, min_temperature

climate_new = pd.DataFrame()
climate_new['Date'] = climate['date']
climate_new['precipitation'] = climate['precipitation']
climate_new['avg_hourly_pressure_station'] = climate['avg_hourly_pressure_station']
climate_new['avg_hourly_wind_speed'] = climate['avg_hourly_wind_speed']
climate_new['max_wind_speed'] = climate['max_wind_speed']
climate_new['avg_hourly_temperature'] = climate['avg_hourly_temperature']
climate_new['max_temperature'] = climate['max_temperature']
climate_new['min_temperature'] = climate['min_temperature']



power_new = pd.DataFrame()
power_new['Date'] = pd.to_datetime((power.YEAR*10000+power.MO*100+power.DY).apply(str),format='%Y%m%d')
power_new['ALLSKY_SFC_LW_DWN'] = power['ALLSKY_SFC_LW_DWN']


# In[ ]:


#power_new.ALLSKY_SFC_LW_DWN.count(-999)
power_new.eq(0).sum()
power_new.isnull().sum()


# In[ ]:


climate_new.isnull().sum()


# In[ ]:


#now we delete leap year columns

climate_new = climate_new[~((climate_new.Date.dt.month == 2) & (climate_new.Date.dt.day == 29))]

power_new = power_new[~((power_new.Date.dt.month == 2) & (power_new.Date.dt.day == 29))]


# In[ ]:


#sort the dates

climate_new = climate_new.sort_values(by="Date")
power_new = power_new.sort_values(by="Date")


# In[ ]:


climate_new.to_csv(user_key['observed_raw_clean']+'climate-daily-weatherstats_Cleaned.csv', index=None)
power_new.to_csv(user_key['observed_raw_clean']+'POWER-airportlocation_Cleaned.csv', index=None)


# In[ ]:


# step1.csv_data_extraction_CRCM


# In[ ]:


# import netCDF4
import pandas as pd
import datetime as dt
import numpy as np
import csv
import calendar

import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
from environmentVariables import environment_variables


# In[ ]:


# read files

data=pd.read_csv(user_key['path_in']+'tasmin/tasmin_20010101-20051231.csv', header=None)
data_time = pd.read_csv(user_key['path_in']+'tasmin/time_20010101-20051231.csv', header=None)


# In[ ]:


print(len(data))
# print(data)


# In[ ]:


# first position for toronto
var = data.iloc[119, 211] 
print(var)


# In[ ]:


# Calculate num of leap years


# In[ ]:


# Input list initialization
input_list = [1950, 1951, 1952, 1953, 1954, 1955,
         1956, 1957, 1958, 1959, 1960,
         1961, 1962, 1963, 1964, 1965, 
         1966, 1967, 1968, 1969, 1970, 
         1971, 1972, 1973, 1974, 1975, 
         1976, 1977, 1978, 1979, 1980, 
         1981, 1982, 1983, 1984, 1985
        ,1986, 1987, 1988, 1989, 1990
        ,1991, 1992, 1993, 1994, 1995
        ,1996, 1997, 1998, 1999, 2000
        ]


# In[ ]:


def findLeapYear(input_list):
    ans = 0
    for elem in input_list:
        if calendar.isleap(int(elem)):
            ans = ans + 1
    return ans

numleap = findLeapYear(input_list)
print(numleap)


# In[ ]:


# Extract based on rlat and rlon

rlon_x = 211 # adjusted from 212 since headers start at 0
rlat_y = 119 # adjusted from 120 since index starts at 0
counter = 0

list_of_vars = []

 
while (rlat_y+counter) < len(data)-1:
    var = data.iloc[rlat_y+counter, rlon_x]
    list_of_vars.append(var)
        
    counter+=260 

len(list_of_vars) #should always be 1825


# In[ ]:


#read data_time and transpose into column and append variable and date info to new df
data_all = data_time.transpose()
data_all.insert(1, 'Variable', list_of_vars)
data_all = data_all.rename(columns={0: 'Date'})


# In[ ]:


# Change time units


# In[ ]:


startdate = "12/01/1949"
temp = pd.to_datetime(startdate) + pd.DateOffset(days= 13171.5 +numleap)


# In[ ]:


# change time units from 'days since 12/01/1949' to actual date
startdate = "12/01/1949"
row_iterator = data_all.iterrows()
counter = 1

for i, row in row_iterator:
    if counter != len(data_all)+1:
        #temp = pd.to_datetime(startdate) + pd.DateOffset(days=data_all.at[i, 'Date']+9)
        #if temp.month != 2 and temp.day != 29:
            #data_all.at[i, 'Date_new'] = pd.to_datetime(temp)
        data_all.at[i, 'Date_new'] = pd.to_datetime(startdate) +                                      pd.DateOffset(days=data_all.at[i, 'Date']+numleap)
            #data_all.at[i, 'Date_new2'] = pd.to_datetime(data_all.at[i, 'Date_new']) + pd.DateOffset(days=9)
            
    counter += 1

data_all['Date_new'] = pd.to_datetime(data_all['Date_new']).dt.date


# In[ ]:


# flag leap years

row_iterator = data_all.iterrows()
counter = 1

for i, row in row_iterator:
    if counter != len(data_all)+1:
        if data_all.at[i, 'Date_new'].month == 2 and data_all.at[i, 'Date_new'].day == 29:
             data_all.at[i, 'flag'] = 'flag'

    counter += 1


# In[ ]:


# if flag, change flagged date to +1

row_iterator = data_all.iterrows()
counter2 = 1

for i, row in row_iterator:
    if counter2 != len(data_all)+1:
        if data_all.at[i, 'flag'] == 'flag':
            data_all.at[i, 'Date_2'] = data_all.at[i+1, 'Date_new']
    counter2+=1   


# In[ ]:


# copy over date from before if Date_2 is null 
# otherwise keep the value in Date_2

row_iterator = data_all.iterrows()
counter3 = 1
numberofflags = 0

for i, row in row_iterator:
    if counter3 != len(data_all)+1:
        if data_all.at[i, 'flag'] == 'flag':
            numberofflags+=1
        temp = data_all.at[i, 'Date_new'] + pd.DateOffset(days=numberofflags)
        if (temp.month == 2 and temp.day == 29):
            data_all.at[i, 'Date_2'] = data_all.at[i, 'Date_new'] + pd.DateOffset(days=numberofflags+1)
        else:
            data_all.at[i, 'Date_2'] = data_all.at[i, 'Date_new'] + pd.DateOffset(days=numberofflags)


    counter3+=1

data_all['Date_2'] = pd.to_datetime(data_all['Date_2']).dt.date


# In[ ]:


# OUTPUT


# In[ ]:


# delete unnecessary columns
del data_all['Date']
del data_all['Date_new']
del data_all['flag']

# rename column
data_all = data_all.rename(columns={'Date_2': 'Date'})


# In[ ]:


# reorder column
data_all = data_all[['Date', 'Variable']]


# In[ ]:


data_all.to_csv(user_key['model_raw_unclean']+'tasmin/tasmin_extrTO_2001-2005.csv', index=None)


# In[ ]:


data_all.to_csv(user_key['model_raw_unclean']+'tasmin/tasmin_extrTO_2001-2005.csv', index=None)


# In[ ]:



import pandas as pd
import datetime as dt
import numpy as np
import csv
import calendar

import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
from environmentVariables import environment_variables


# In[ ]:


# read files

data_one=pd.read_csv(user_key['model_raw_unclean']+'pr/pr_extrTO_1986-1990.csv')
data_two=pd.read_csv(user_key['model_raw_unclean']+'pr/pr_extrTO_1991-1995.csv')
data_three=pd.read_csv(user_key['model_raw_unclean']+'pr/pr_extrTO_1996-2000.csv')
data_four=pd.read_csv(user_key['model_raw_unclean']+'pr/pr_extrTO_2001-2005.csv')


# In[ ]:


# MERGE
frames = [data_one, data_two, data_three, data_four]
result = pd.concat(frames)


# In[ ]:


result.to_csv(user_key['model_raw_clean']+'pr/pr_all_extrTO_1986-2005.csv', index=None)


# In[ ]:


# step3.5_dq_fillin


# In[ ]:


import pandas as pd
import datetime as dt
import numpy as np
import csv
import calendar

import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
from environmentVariables import environment_variables


# In[ ]:


# read file created by step 3
data=pd.read_csv(user_key['observed_raw_clean']+'climate-daily-weatherstats_Cleaned.csv')

# read fill in data observed data
dataFillIn=pd.read_csv(user_key['observed_raw_clean']+'DQ Report/projectedvsobserved_fillin.csv')


# In[ ]:


# loop through the data file, if the precipitation is null then 
# look through the fill in file if it has that date, if so fill in the value from fill in to the data

# make the date column the index for searching 
dataFillIn.set_index('Date',inplace = True)

row_iterator = data.iterrows()   
for i, row in row_iterator:
    if (pd.isnull(data.at[i,"precipitation"])):
        print(data.at[i,"Date"])
       # print(dataFillIn.index.values)
        #if null then replace with variable from fill in
        data.at[i,"precipitation"] = dataFillIn.loc[data.at[i,"Date"],"precipitation"]
        print(dataFillIn.loc[data.at[i,"Date"],"precipitation"])
        
        
#print(data)


# In[ ]:


#write to file
data.to_csv(user_key['observed_raw_clean']+'climate-daily-weatherstats_Cleaned.csv', index=None)


# In[ ]:


# step3.Unit_Conversion


# In[ ]:


import pandas as pd
import datetime as dt
import numpy as np
import csv
import calendar

import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
from environmentVariables import environment_variables


# In[ ]:


# read files
data=pd.read_csv(user_key['model_raw_clean']+'pr/pr_all_extrTO_1986-2005.csv')

# conversion equation based on variable name
variableName = "pr"


# In[ ]:



# loop through the rows creating a new converted column    
row_iterator = data.iterrows()   
for i, row in row_iterator:
    currVar = (data.at[i,'Variable'])
    if (currVar != "Variable" ):
        if (variableName == "pr"):
            #1 kg/m2/s = 86400 mm/day
            data.at[i, 'Variable_converted'] = (float(currVar) *  (86400))
        elif (variableName == "ps"):
            #1 pa	0.001 kP
             data.at[i, 'Variable_converted'] = (float(currVar) *  (0.001))
        elif (variableName == "rlds"):
            data.at[i, 'Variable_converted'] = (float(currVar))
        elif (variableName == "sfcWind"):
            #1 m/s	3.6km/h
            data.at[i, 'Variable_converted'] = (float(currVar) *  (3.6))
        elif (variableName == "sfcWindmax"):
            #1 m/s	3.6km/h
            data.at[i, 'Variable_converted'] = (float(currVar) *  (3.6))
        elif (variableName == "tas"):
            # 1K = -273 degrees celsius
            data.at[i, 'Variable_converted'] = (float(currVar) - (273.15))
        elif (variableName == "tasmax"):
            # 1K = -273 degrees celsius
            data.at[i, 'Variable_converted'] = (float(currVar) - (273.15))
        elif (variableName == "tasmin"):
            # 1K = -273 degrees celsius
            data.at[i, 'Variable_converted'] = (float(currVar) - (273.15))
                                  
        
print(data)


# In[ ]:


# delete unnecessary columns
del data['Variable']

# rename column
data = data.rename(columns={'Variable_converted': 'Variable'})


# In[ ]:


data.to_csv(user_key['model_raw_clean']+'pr/pr_allCONV_extrTO_1986-2005.csv', index=None)


# In[ ]:


# step4.mapping_model_to_observed


# In[ ]:


import pandas as pd
import datetime as dt
import numpy as np
import csv
import calendar

import dash
import dash_core_components as dcc
import dash_html_components as html

import os,sys,inspect
from dash.dependencies import Input, Output

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
from environmentVariables import environment_variables


# In[ ]:



#variable (change to read user input)
variable = 'pr'


# In[ ]:


#use inputs to select file for climate model

# need to figure out the time 

data=pd.read_csv(user_key['model_raw_clean']+variable+'/'+variable+'_allCONV_extrTO_1986-2005.csv')


# In[ ]:


# read observational climate csv

if variable =='rlds':
    observeData=pd.read_csv(user_key['observed_raw_clean']+'POWER-airportlocation_Cleaned.csv')
else:
    observeData=pd.read_csv(user_key['observed_raw_clean']+'climate-daily-weatherstats_Cleaned.csv')


# In[ ]:


data['Date'] =  pd.to_datetime(data['Date'], format='%Y-%m-%d')


# In[ ]:


# read column based on the variable 

 
if variable == 'tas':
            #then it is TEMP in the data, find the column
    column = 'avg_hourly_temperature'
    
elif variable == 'pr' :
    column = 'precipitation'
            
elif variable == 'ps' :
    column = 'avg_hourly_pressure_station'
            
elif variable == 'sfcWind' :
    column = 'avg_hourly_wind_speed'
            
elif variable == 'sfcWindmax' :
    column = 'max_wind_speed'
            
elif variable == 'tasmax' :
    column = 'max_temperature'
            
elif variable == 'tasmin' :
    column = 'min_temperature'

elif variable == 'rlds':
    column = 'ALLSKY_SFC_LW_DWN'
          

row_iterator = observeData.iterrows()
counter =0

dates = []
observedData = []
modelData = []

#the for loop will loop through the observed data file (weatherstats)
for i, row in row_iterator:
        if counter != len(observeData):
            dates.append(observeData.at[i,'Date'])
            observedData.append(observeData.at[i,column])
            counter += 1

row_ittr2 = data.iterrows()
counter =0
#the for loop will loop through the model data file 
for i, row in row_ittr2:
         if counter != len(data):
            modelData.append(data.at[i,'Variable'])
            counter += 1


            

#now we have all the variables in array now we create a dataframe
data_all = pd.DataFrame()
data_all.insert(0, 'Date', dates)
data_all.insert(1, 'Observed'+variable, observedData)
data_all.insert(2, 'Model'+variable, modelData)
        
print(data_all)


# In[ ]:


data_all.to_csv(user_key['projectedvsobserved_mapped']+ variable+'_comparison_output.csv', index=None)


# In[ ]:


# Step5.biascalc


# In[ ]:


import pandas as pd
import datetime as dt
import numpy as np
import csv
import calendar

import dash
import dash_core_components as dcc
import dash_html_components as html

import os,sys,inspect
from dash.dependencies import Input, Output

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
from environmentVariables import environment_variables


# In[ ]:


variables = ['pr','ps','rlds','sfcWind','sfcWindmax','tas','tasmax','tasmin']

for variable in variables:
    data=pd.read_csv(user_key['projectedvsobserved_mapped']+ variable+'_comparison_output.csv')

    biasData = data['Model'+variable] - data['Observed'+variable]

    data["Bias"] = biasData
    data.to_csv(user_key['projectedvsobservedbias_mapped']+ variable+'_comparison_bias_output.csv', index=None)

