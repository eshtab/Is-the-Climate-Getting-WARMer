#!/usr/bin/env python
# coding: utf-8

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


Userdata=pd.read_csv('AutomatedSteps/userInput.csv', header=[0])
SummaryDF = pd.DataFrame(columns=['Variable'])
directory_list = list()

for root, dirs, files in os.walk(user_key['path_in'], topdown=False):
    for name in dirs:
        directory_list.append(name)

print(directory_list)

for col in Userdata.columns:
    #if the column name exists in the data variables then add to list
    
    if col == 'T2M':
        col = 'tas'
    elif col == 'PRECTOTCORR' :
        col = 'pr'
    elif col == 'PS' :
        col = 'ps'
    elif col == 'WS10M' :
        col = 'sfcWind'
    elif col == 'WS10M_MAX' :
        col = 'sfcWindmax'
    elif col == 'T2M_MAX' :
        col = 'tasmax'
    elif col == 'T2M_MIN' :
        col = 'tasmin'
    elif col == 'ALLSKY_SFC_LW_DWN':
        col = 'rlds'
    #col = col.lower()
    print(col)
    if col in directory_list:
        
        SummaryDF = SummaryDF.append({'Variable':col}, ignore_index=True)

print(SummaryDF)



#logic to create an output for data 

#create counts 

outputDF = pd.DataFrame(columns=['Column'])
NA = []
blanks = []
 
for col in Userdata.columns:
    #use each column
   
    tempNA = 0
    tempBlanks = 0
    outputDF = outputDF.append({'Column': col}, ignore_index=True)
    for index, row in Userdata.iterrows():
        #look at each item in each column
        if Userdata.loc[index,col] == -999 :
            tempNA = tempNA + 1
        
        if Userdata.loc[index,col] == '' :
            tempBlanks = tempBlanks + 1
            
    print(tempNA)
    NA.append(tempNA)
    blanks.append(tempBlanks)

print(NA)
print(outputDF)
print(blanks)
outputDF['Nulls'] = NA
outputDF['Blanks'] = blanks 
    


# In[ ]:


SummaryDF.to_csv('AutomatedSteps/variableList.csv', index=None)
outputDF.to_csv('AutomatedSteps/outputFeedback.csv', index=None)


# In[ ]:


# step1.csv_data_extraction_CRCM


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

#we must automate all the files here

#the variable decides which file to select as data
#load in the csv with the selected options
selections=pd.read_csv('AutomatedSteps/optionSelection.csv', header=[0])
#now we allocate all variables (rlat,rlong,variable)
variable = ""
rlat = 0
rlong = 0
for index, row in selections.iterrows():
    if selections.at[index,'option'] == 'rlat':
        rlat = selections.at[index,'selection']
    if selections.at[index,'option'] == 'rlong':
        rlong = selections.at[index,'selection']
    if selections.at[index,'option'] == 'variable':
        variable = selections.at[index,'selection']
    if selections.at[index,'option'] == 'startDate':
        startDate = selections.at[index,'selection']
    if selections.at[index,'option'] == 'endDate':
        endDate = selections.at[index,'selection']
    if selections.at[index,'option'] == 'currYear':
        currYear = selections.at[index,'selection']
        
#now that selections are set we continue
#decide file based on date
rlat = int(rlat)
rlong = int(rlong)
#now based on how many files exist with variable name and date
if currYear == '1986':
    print("1986 here")
    dtStr = "19860101-19901231"
    dtOutStr = "1986-1990"
elif currYear == '1991':
    dtStr = "19910101-19951231"
    dtOutStr = "1991-1995"
elif currYear == '1996':
    dtStr = "19960101-20001231"
    dtOutStr = "1996-2000"
elif currYear == '2001':
    dtStr = "20010101-20051231"
    dtOutStr = "2001-2005"

    

    
data=pd.read_csv(user_key['path_in']+ variable + '/' + variable + '_' + dtStr + '.csv', header=None)
data_time = pd.read_csv(user_key['path_in']+ variable + '/' +'time_' + dtStr + '.csv', header=None)


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


# In[ ]:


rlon_x = rlong 
rlat_y = rlat  
counter = 0

list_of_vars = []

 
while (rlat_y+counter) < len(data)-1:
    var = data.iloc[rlat_y+counter, rlon_x]
    list_of_vars.append(var)
        
    counter+=260 

len(list_of_vars) 


# In[ ]:


#read data_time and transpose into column and append variable and date info to new df
data_all = data_time.transpose()
data_all.insert(1, 'Variable', list_of_vars)
data_all = data_all.rename(columns={0: 'Date'})


# In[ ]:


# Change time units -


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


data_all.to_csv('AutomatedSteps/' + variable +'_'+dtOutStr +'.csv', index=None)


# In[ ]:


# step2.combine_years_into_one_var_file


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

#this will be based on variable in the user input


selections=pd.read_csv('AutomatedSteps/optionSelection.csv', header=[0])


for index, row in selections.iterrows():
    if selections.at[index,'option'] == 'variable':
        variable = selections.at[index,'selection']

data_one=pd.read_csv('AutomatedSteps/'+ variable + '_1986-1990.csv')
data_two=pd.read_csv('AutomatedSteps/'+ variable + '_1991-1995.csv')
data_three=pd.read_csv('AutomatedSteps/'+ variable + '_1996-2000.csv')
data_four=pd.read_csv('AutomatedSteps/'+ variable + '_2001-2005.csv')


# In[ ]:


# merge
frames = [data_one, data_two, data_three, data_four]
result = pd.concat(frames)


# In[ ]:


result.to_csv('AutomatedSteps/'+ variable + '.csv', index=None)

#clean up and delete those files
os.remove('AutomatedSteps/'+ variable + '_1986-1990.csv')
os.remove('AutomatedSteps/'+ variable + '_1991-1995.csv')
os.remove('AutomatedSteps/'+ variable + '_1996-2000.csv')
os.remove('AutomatedSteps/'+ variable + '_2001-2005.csv')


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


# In[ ]:


# read files
selections=pd.read_csv('AutomatedSteps/optionSelection.csv', header=[0])
for index, row in selections.iterrows():
    if selections.at[index,'option'] == 'variable':
        variable = selections.at[index,'selection']
        
        
data=pd.read_csv('AutomatedSteps/'+variable +'.csv')
observedData=pd.read_csv('AutomatedSteps/userInput.csv')

# conversion equation based on variable name
variableName = variable


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
                                  
        
#print(data)

row_iterator2 = observedData.iterrows()   
for i, row in row_iterator2:
    if (variableName == "sfcWind"):
        currVar = (observedData.at[i,'WS10M'])
        #1 m/s	3.6km/h
        observedData.at[i, 'WS10M'] = (float(currVar) *  (3.6))
    elif (variableName == "sfcWindmax"):
        currVar = (observedData.at[i,'WS10M_MAX'])
        #1 m/s	3.6km/h
        observedData.at[i, 'WS10M_MAX'] = (float(currVar) *  (3.6))
                        
#print(observedData)


# In[ ]:


# delete unnecessary columns
del data['Variable']

# rename column
data = data.rename(columns={'Variable_converted': 'Variable'})


# In[ ]:


data.to_csv('AutomatedSteps/'+variable +'_converted.csv', index=None)
observedData.to_csv('AutomatedSteps/userInput.csv', index=None)


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


#use inputs to select file for climate model
selections=pd.read_csv('AutomatedSteps/optionSelection.csv', header=[0])
for index, row in selections.iterrows():
    if selections.at[index,'option'] == 'variable':
        variable = selections.at[index,'selection']
        

data=pd.read_csv('AutomatedSteps/'+variable+'_converted.csv')


# In[ ]:


# read observational climate csv provided by user

observeData=pd.read_csv('AutomatedSteps/userInput.csv')


# In[ ]:


data['Date'] =  pd.to_datetime(data['Date'], format='%Y-%m-%d')


# In[ ]:


# read column based on the variable 

 
if variable == 'tas':
            #then it is TEMP in the data, find the column
    column = 'T2M'
    
elif variable == 'pr' :
    column = 'PRECTOTCORR'
            
elif variable == 'ps' :
    column = 'PS'
            
elif variable == 'sfcWind' :
    column = 'WS10M'
            
elif variable == 'sfcWindmax' :
    column = 'WS10M_MAX'
            
elif variable == 'tasmax' :
    column = 'T2M_MAX'
            
elif variable == 'tasmin' :
    column = 'T2M_MIN'

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
            dtTemp = str(observeData.at[i,'YEAR']) + "-" + str(observeData.at[i,'MO']) + "-" + str(observeData.at[i,'DY']) 
            if(str(observeData.at[i,'MO']) == '2' and str(observeData.at[i,'DY']) == '29'):
                print("skipped : " + dtTemp)
            else:
                dates.append(dtTemp)
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
        
#print(data_all)


# In[ ]:


data_all.to_csv('AutomatedSteps/'+variable+'_comparison.csv', index=None)


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


# In[ ]:


selections=pd.read_csv('AutomatedSteps/optionSelection.csv', header=[0])
for index, row in selections.iterrows():
    if selections.at[index,'option'] == 'variable':
        variable = selections.at[index,'selection']
        
data=pd.read_csv('AutomatedSteps/'+variable+'_comparison.csv')

biasData = data['Model'+variable] - data['Observed'+variable]

data["Bias"] = biasData
data.to_csv('AutomatedSteps/'+variable+'_comparison_bias.csv', index=None)

