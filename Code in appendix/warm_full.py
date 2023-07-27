#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# step6.dash_v1


# In[ ]:


import pandas as pd
import numpy as np
import csv
import calendar
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots
import base64

import io
from io import StringIO
from scipy import stats

import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import datetime as dt
import plotly.io as pio
import time

import os,sys,inspect
from dash.dependencies import Input, Output, State
from pandas import ExcelWriter
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
#parent_dir = os.paths.dirname(current_dir)
sys.path.insert(0, current_dir) 
from environmentVariables import environment_variables
import plotly
plotly.__version__


# In[ ]:


# sys.path.insert(0, 'calculation_folder') # Note: if this relavtive path doesn't work or produces errors try replacing it with an absolute path
# import calculation


app = dash.Dash(__name__)

#for external style sheets replace ___name__ with the below format
#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#df = pd.read_csv(user_key['extracted_loc_raw']+'/tas/tas_comparison_output_1991-1995.csv')


colors = {
    'background': '#E31837',
    'text': '#111111'
}



MIN_YR = 1986
MAX_YR = 2006
#This is the inital layout of the Website
app.layout = html.Div(style={'top-margin' : '0px'}, children=[
    dcc.Store(id='main_data'),
    dcc.Store(id='observed_normals'),
    dcc.Store(id='projected_normals'),
    dcc.Store(id='annual_data'),
    dcc.Store(id='observed_mean'),
    dcc.Store(id='projected_mean'),
    dcc.Store(id='observed_deviation'),
    dcc.Store(id='projected_deviation'),
    dcc.Store(id='observed_variance'),
    dcc.Store(id='projected_variance'),
    dcc.Store(id='bias_data'),
    dcc.Store(id='observed_monthBox'),
    dcc.Store(id='projected_monthBox'),
    dcc.Store(id='observed_yearBox'),
    dcc.Store(id='projected_yearBox'),
    dcc.Store(id='mainFig'),
    dcc.Store(id='projected_median'),
    dcc.Store(id='observed_median'),
    
    
    dcc.Store(id='main_data_auto'),
    dcc.Store(id='observed_normals_auto'),
    dcc.Store(id='projected_normals_auto'),
    dcc.Store(id='annual_data_auto'),
    dcc.Store(id='observed_mean_auto'),
    dcc.Store(id='projected_mean_auto'),
    dcc.Store(id='observed_deviation_auto'),
    dcc.Store(id='projected_deviation_auto'),
    dcc.Store(id='observed_variance_auto'),
    dcc.Store(id='projected_variance_auto'),
    dcc.Store(id='bias_data_auto'),
    dcc.Store(id='observed_monthBox_auto'),
    dcc.Store(id='projected_monthBox_auto'),
    dcc.Store(id='observed_yearBox_auto'),
    dcc.Store(id='projected_yearBox_auto'),
    dcc.Store(id='mainFig_auto'),
    dcc.Store(id='projected_median_auto'),
    dcc.Store(id='observed_median_auto'),
    
    
    html.Div([
        html.Img(src='https://github.com/eshtab/york_thesisrepo_public/blob/main/WarmLogo3.jpeg?raw=true',style={'width': '220px','height' : '70px','float' : 'left','margin-left':'0px','padding':'0px'}),
        html.Img(src='https://github.com/eshtab/york_thesisrepo_public/blob/main/york logo2.png?raw=true',style={'height' : '70px','float' : 'right','margin-right':'0px'})
    ],style = {'backgroundColor' : colors['background'], 'height' : '70px'} ),
    
    html.Div([
        dcc.Tabs(id='navbar', vertical=True, value='home',  children=[
        dcc.Tab(id="home",label='Home', value='home'),
        dcc.Tab(id="porj",label='Hosted: Regional Climate Model Validation', value='projVobs'),      
        dcc.Tab(id="automate",label='User-Data: Regional Climate Model Validation', value='auto'),
        dcc.Tab(id="docs",label='Documentation', value='howto'),
        ],parent_style={'float': 'left', 'height' : '90vh', 'width': '220px', 'backgroundColor': '#383838'}, style = {'height' : '600px','color' : 'white','font-family': 'Verdana'},
        colors={
        "border": "white",
        "primary": "white",
        "background": "#383838"
    })
        
        
    ]),
    html.Div(id='nav-content')

])

#This is for the vertical tabs, like Home, Docs, etc.

@app.callback(Output('nav-content', 'children'),
              Input('navbar', 'value'))
def render_content(tab):
    if tab == 'home':
        return html.Div([
            html.Img(id='image',src = 'https://github.com/eshtab/york_thesisrepo_public/blob/main/WarmLogoFull.jpeg?raw=true',style={'height' : '50%','width' : '55%','margin' :'auto','display' : 'block'} ),
            html.P('The Weather Analysis Regional Model (WARM) is a visualization tool developed for climatic analysis. It provides the ability to upload your own observed climate datasets or use the web-hosted datasets to perform comparative analysis with a regional climate model, CanRCM4. Additionally, WARM provides visualizations, data tables, and the ability to download the underlying data models, and exploratory data analysis outputs.',style= {'float' : 'left','margin': '15px','color' : 'black','width' : '50%','height' : '260px','background-color': '#D3D3D3','border-style' : 'solid','border-radius': '25px','font-family': 'Verdana','font-size': '25px','padding':'20px','text-align':'center','vertical-align': 'middle'})
        ],style = {'background': 'url(https://github.com/eshtab/york_thesisrepo_public/blob/main/FPBackground.png?raw=true)', 'background-size': 'contain','height': '88vh','background-position' : 'right','background-repeat' : 'no-repeat'})
    
    
    
    elif tab == 'projVobs':
        return html.Div([
            dcc.Tabs(id='tabs', value='tabs-1', children=[
            dcc.Tab(id="load",label='Load', value='Load'),
            dcc.Tab(id="analyze",label='Analyze', value='Analyze',disabled=True)
            ],style = {'font-family': 'Verdana'}),
            html.Div(id='tabs-content')
            ])
    
    elif tab == 'auto':
        return html.Div([
            dcc.Tabs(id='tabs-auto', value='tabs-3', children=[
            dcc.Tab(id="load",label='Load', value='Load'),
            dcc.Tab(id="analyze-auto",label='Analyze', value='Analyze-auto',disabled=True)
            ],style = {'font-family': 'Verdana'}),
            html.Div(id='tabs-content-auto')
            ])
   
    elif tab == 'howto':
        return html.Div([
             html.Iframe(src = "https://docs.google.com/viewer?embedded=true&url=https://github.com/eshtab/york_thesisrepo_public/raw/main/documentationDASH.pdf",
                        style={'height' : '100vh','width' : '80%'}) 
        ])
        
        
        
        
#THIS is for Proj v Obsv the horizontal tabs such as Load,Analyze
@app.callback(Output('tabs-content', 'children'),
              Input('tabs', 'value'))
def render_content(tab):
    if tab == 'Load':
        return html.Div([
            html.Form([
                html.H2('Please fill out the options below',style = {'text-align' : 'Center','font-family': 'Tahoma'}),
                html.Br([]),
                html.H3('Select a region:'),
                 dcc.Dropdown(
                    id='region',
                    options=[
                            {'label': 'Toronto, Canada', 'value': 'TOR'}                       
                ]),
                html.Br([]),
                html.H3('Select a variable:'),
                dcc.Dropdown(
                        id='variable',
                        options=[
                            {'label': 'Precipitation', 'value': 'pr'},
                            {'label': 'Pressure', 'value': 'ps'},
                            {'label': 'Surface Downwelling Longwave Radiation', 'value': 'rlds'},
                            {'label': 'Surface Temperature', 'value': 'tas'},
                            {'label': 'Maximum Surface Temperature', 'value': 'tasmax'},
                            {'label': 'Minimum Surface Temperature', 'value': 'tasmin'},
                            {'label': 'Surface Wind Speed', 'value': 'sfcWind'},
                            {'label': 'Maximum Surface Wind Speed', 'value': 'sfcWindmax'}
                ]),
                html.Br([]),
                html.H3('Select a date range:'),
                dcc.RangeSlider(
                    id="date_slider",
                    min=MIN_YR,
                    max=MAX_YR,
                    count=1,
                    step=1,
                    value=[MIN_YR, MAX_YR],
                    marks={yr: str(yr) for yr in range(MIN_YR, MAX_YR + 1)},
                ),
                dcc.DatePickerRange(
                    id='date-picker-range',
                    min_date_allowed=dt.datetime(1986, 1, 1),
                    max_date_allowed=dt.datetime(2006, 1, 1),
                    display_format="MMM D, YYYY",
                    style={'width' : '100%'}
                    #observed vs projected #daterange should be diff based on variable

                ),
                html.P(id = "displayDate"),
                html.Br([]),
                html.Br([]),
                html.Button('Submit', id='submit-val', type = 'button', n_clicks=0,style={'background-color': '#4CAF50','border': 'none','color': 'white','padding': '15px 32px','text-align': 'center','text-decoration': 'none','display': 'inline-block','font-size': '16px','margin': '4px 2px'})    

                
        ],id = 'LoadForm'),

        html.Form([ html.H3('Instructions',style={'font-family': 'Verdana'}),
                html.P('1. Enter selection for region.',style = {'text-align' : 'Left'}),
                html.P('2. Enter selection for variable.',style = {'text-align' : 'Left'}),
                html.P('3. Enter a start and end year using the slider. Use the calendar to choose specific dates or enter the dates by typing.',style = {'text-align' : 'Left'}),                      
                html.P('4. Click on submit to view graphs. Note that clicking submit will automatically redirect to the Analyze tab.',style = {'text-align' : 'Left'})                      
                                           
                  ],id = 'LoadInstruction')
        ],id = 'LoadDiv' )


#this is for the automation tab
@app.callback(Output('tabs-content-auto', 'children'),
              Input('tabs-auto', 'value'))
def render_content(tab):
    if tab == 'Load':
        return html.Div([
            html.Form([
                html.H2('Please fill out the options below',style = {'text-align' : 'Center','font-family': 'Tahoma'}),
                html.Br([]),
                html.H3('Select a CORDEX region:'),
                dcc.Dropdown(
                    id='region-auto',
                    options=[
                            {'label': 'North America', 'value': 'NA'}                       
                ]),
                html.Br([]),
                html.H3('Enter Grid Coordinates:'),
                html.Br([]),
                dcc.Input(
                    id = 'lat',
                    type="number",
                    step = 1,
                    placeholder="Latitude",
                    style = {'height' : '30px'}),
                dcc.Input(
                    id = 'long',
                    type="number",
                    step = 1,
                    placeholder="Longitude",
                    style = {'margin-left' : '20px','height' : '30px'}),
      
                html.Br([]),
                html.H3('Name your Data:'),
                dcc.Input(
                    id='nameData-auto',
                    type="text",
                    style = {'height' : '30px'}
                ),
                html.Br([]),
                html.H3('Upload Dataset:'),
                dcc.Upload(
                    id='upload-data-auto',
                    children=html.Div([
                        'Drag and Drop or ',
                        html.A('Select Files')
                    ]),
                    style={
                        'width': '100%',
                        'height': '60px',
                        'lineHeight': '60px',
                        'borderWidth': '1px',
                        'borderStyle': 'dashed',
                        'borderRadius': '5px',
                        'textAlign': 'center',
                        'margin': '10px'
                    },
                    # Allow multiple files to be uploaded
                    multiple=False
                ),
                html.Div(id='upload-Output'),
                html.H3('Select a date range:'),
                dcc.RangeSlider(
                    id="date_slider-auto",
                    min=MIN_YR,
                    max=MAX_YR,
                    count=1,
                    step=1,
                    value=[MIN_YR, MAX_YR],
                    marks={yr: str(yr) for yr in range(MIN_YR, MAX_YR + 1)},
                ),
                dcc.DatePickerRange(
                    id='date-picker-range-auto',
                    min_date_allowed=dt.datetime(1986, 1, 1),
                    max_date_allowed=dt.datetime(2006, 1, 1),
                    display_format="MMM D, YYYY",
                    style={'width' : '100%'}
                    #observed vs projected #daterange should be diff based on variable

                ),
                html.P(id = "displayDate-auto"),
                html.Br([]),
                html.Br([]),
                #after the submit button is hit
                #the code will execute the steps  to extract the rlat and rlong and everything else using the variable chosen and provided rlat and rlong
                #they will then provide the proper excel output to be displayed
                html.Button('Submit', id='submit-val-auto', type = 'button', n_clicks=0,style = {'background-color': '#4CAF50','font-size' : '20px'})    

                
        ],id = 'LoadForm',style = {'font-family': 'Tahoma'}),

        html.Form([ html.H3('Instructions',style={'font-family': 'Verdana'}),
                html.P('1. Enter selection for climate model region.',style = {'text-align' : 'Left'}),
                html.P('2. Enter selection for climate model latitude and longitude in grid format. For details on how to calculate the grid location values for a region, please visit the documentation tab.',style = {'text-align' : 'Left'}),
                html.P('3. Enter text to name the csv file that is available for download after submitting selections.',style = {'text-align' : 'Left'}),
                html.P('4. Upload the observed climate dataset by clicking on the field or by using drag-and-drop. For details on how to format your dataset, please visit the documentation tab.',style = {'text-align' : 'Left'}),
                html.P('5. Enter selection for variable (these are populated based on the dataset provided).',style = {'text-align' : 'Left'}),
                html.P('6. Enter a start and end year using the slider. Use the calendar to choose specific dates or enter the dates by typing.',style = {'text-align' : 'Left'}),                      
                html.P('7. Click on submit to view graphs. Note that clicking submit will automatically redirect to the Analyze tab.',style = {'text-align' : 'Left'})                      
                                           
                  ],id = 'LoadInstruction')
        ],id = 'LoadDiv' )




@app.callback(Output('upload-Output', 'children'),
              Input('upload-data-auto', 'contents'),
              State('upload-data-auto', 'filename'),
              State('upload-data-auto', 'last_modified'))
def update_output(list_of_contents, filename, list_of_dates):
    #print(1)
    if list_of_contents is not None:
        #print(2)
        content_type, content_string = list_of_contents.split(',')
        decoded = base64.b64decode(content_string)
        try:
            
            if 'csv' in filename:
                
                 #Delete all csv files in the Automatedsteps folder
                dir_name = "AutomatedSteps/"
                files = os.listdir(dir_name)

                for file in files:
                    if file.endswith(".csv"):
                        os.remove(os.path.join(dir_name, file))
                
                #IF user uploads a csv then we continue with steps
                #next step is to save the uploaded file
                #the steps will run and create the needed csvs
                #then there will be a printed out csv with results from the upload which we can display below
                #os.remove("AutomatedSteps/userInput.csv")
                #first save the user upload to file
                df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
                #print(df)
                df.to_csv('AutomatedSteps/userInput.csv', index=None)
                
                #this step will run and extract columns
                get_ipython().run_line_magic('run', './AutomatedSteps/Step0.ipynb')

                display = pd.read_csv('AutomatedSteps/variableList.csv')
                display2 = pd.read_csv('AutomatedSteps/outputFeedback.csv')
                
                #finally display the output
                return html.Div([
                html.H3('Select a variable:'),
                #this variable selection is made by the user input csv
                dcc.Dropdown(
                        id='variable-auto',
                        options = [{'label': row_value, 'value': row_value} for i,row_value in display['Variable'].iteritems()]
                ),
                html.H3('Data Quality of Input:'),
                dash_table.DataTable(
                id='tableFeedback',
                columns=[{"name": i, "id": i} for i in display2.columns],
                data=display2.to_dict('records')
            )
                ])
            else:
                
                return html.Div([
                'The file is not a csv, please upload a csv file'
            ])
        except Exception as e:
            print(e)
            return html.Div([
                'There was an error processing this file: '+ filename 
            ])


        
        
        
        
        
        
        
        
#This is the AUtomation BUTTON
#This is here for calculating the Model vs Observed graph and outputting it to the DIV
@app.callback(
    Output("tabs-auto", "value"),
    Output("analyze-auto", "children"),
    Output('main_data_auto','data'),
    Output('observed_normals_auto','data'),
    Output('projected_normals_auto','data'),
    Output('annual_data_auto','data'),
    Output('observed_mean_auto','data'),
    Output('projected_mean_auto','data'),
    Output('observed_deviation_auto','data'),
    Output('projected_deviation_auto','data'),
    Output('observed_variance_auto','data'),
    Output('projected_variance_auto','data'),
    Output('bias_data_auto','data'),
    Output('observed_monthBox_auto','data'),
    Output('projected_monthBox_auto','data'),
    Output('observed_yearBox_auto','data'),
    Output('projected_yearBox_auto','data'),
    Output('mainFig_auto','data'),
    [Input("submit-val-auto", "n_clicks")],
    state=[State(component_id='region-auto', component_property='value'),State('variable-auto', 'value'), State('date-picker-range-auto', 'start_date'),State('date-picker-range-auto', 'end_date'),State('lat', 'value'),State('long', 'value')])
def tab_resources(click,region,variable,startDatePicked,endDatePicked,rlat,rlong):
    #print("testing1234")
    if click:
        startDate = dt.datetime.strptime(startDatePicked,'%Y-%m-%d')
 
        endDate = dt.datetime.strptime(endDatePicked,'%Y-%m-%d') - dt.timedelta(days=1)
    
    
        #HERE WE RUN THE STEPS
        #we need to use rlat rlong and all other variables provided
        #in order to run the steps
        #lets save a csv file with the variables
        selections = pd.DataFrame(columns=['option','selection'])
        selections = selections.append({'option':'rlat','selection':rlat}, ignore_index=True)
        selections = selections.append({'option':'rlong','selection':rlong}, ignore_index=True)
        selections = selections.append({'option':'variable','selection':variable}, ignore_index=True)
        selections = selections.append({'option':'startDate','selection':startDate}, ignore_index=True)
        selections = selections.append({'option':'endDate','selection':endDate}, ignore_index=True)
        selections = selections.append({'option':'currYear','selection':0}, ignore_index=True)
        
        #loop 4 times and create the files
        for i in range(1986,2005,5):
            #create the csv with variables
            #selections.loc[selections['option'] = 'currYear', ['selection']] = i
            selections.at[5,'selection']=i
            #print(selections)
            selections.to_csv('AutomatedSteps/optionSelection.csv', index=None)
            get_ipython().run_line_magic('run', './AutomatedSteps/step1.csv_data_extraction_CRCM.ipynb')
  
        
        
        

        
        #run step 2- merge files
        get_ipython().run_line_magic('run', './AutomatedSteps/step2.combine_years_into_one_var_file.ipynb')
        
        #run step 3 unit conversion
        get_ipython().run_line_magic('run', './AutomatedSteps/step3.Unit_Conversion.ipynb')
        
        #run step 4 model mapped to observed
        get_ipython().run_line_magic('run', './AutomatedSteps/step4.mapping_model_to_observed.ipynb')
        
        #step 5 add bias
        get_ipython().run_line_magic('run', './AutomatedSteps/Step5.biascalc.ipynb')
        
        #variable (change to read user input)
        variable = variable
  

        if variable == 'tas':
                    
            column = 'T2M'
            columnName = 'Surface Temperature'
            measurement = '(C)'
            
        elif variable == 'pr' :
            column = 'PRECTOTCORR'
            columnName = 'Precipitation'
            measurement = '(mm)'

        elif variable == 'ps' :
            column = 'PS'
            columnName = 'Surface Pressure'
            measurement = '(kPa)'

        elif variable == 'sfcWind' :
            column = 'WS10M'
            columnName = 'Surface Wind Speed'
            measurement = '(km/h)'

        elif variable == 'sfcWindmax' :
            column = 'WS10M_MAX'
            columnName = 'Maximum Surface Wind Speed'
            measurement = '(km/h)'
        elif variable == 'tasmax' :
            column = 'T2M_MAX'
            columnName = 'Maximum Surface Temperature'
            measurement = '(C)'
        elif variable == 'tasmin' :
            column = 'T2M_MIN'
            columnName = 'Minimum Surface Temperature '
            measurement = '(C)'
        elif variable == 'rlds':
            column = 'ALLSKY_SFC_LW_DWN'
            columnName = 'Surface Downwelling Longwave Radiation'
            measurement = '(W m-2)'



        #THIS IS WHERE WE AUTOMATE IT, use the automated generated file
        data = pd.read_csv('AutomatedSteps/'+variable+'_comparison_bias.csv')

#         mask = (data['Date'] >= str(startDate.date())) & (data['Date'] <= str(endDate.date()))
#         #only use the data in between the user given range
#         data_all = data.loc[mask]
#        mask = (data['Date'] >= str(startDate.date())) & (data['Date'] <= str(endDate.date()))

#        data_all = data.loc[mask]
        data['Date'] = pd.to_datetime(data.Date)
        data['Date'] = data['Date'].dt.strftime('%Y-%m-%d')
        print(data)
        
        data_all = data[data['Date'].between(str(startDate.date()), str(endDate.date()),inclusive='both')]
        print(data_all)
        #create the plot figures
        fig = make_subplots(rows=2, cols=1, shared_xaxes=False)
        
        fig.add_trace(go.Scatter(x=data_all['Date'], y=data_all['Model'+variable],mode = 'lines+markers', name = "Predicted",xhoverformat="%d %b, %Y" ,yhoverformat = ".2f"))
        fig.add_trace(go.Scatter(x=data_all['Date'], y=data_all['Observed'+variable],mode = 'lines+markers',name = "Observed",xhoverformat="%d %b, %Y" ,yhoverformat = ".2f"))

        #Update the plot layot with titles
        fig.update_layout(
            title_text="Comparison of Predicted and Observed Climate",
            title_x=0.5,
            xaxis_title="Date",
            yaxis_title=columnName + ' ' + measurement,
            showlegend=True,
            autosize=False,
            width=1300,
            height=700,
            
#             margin=dict(l=5,r=5,b=0,t=5,pad=5)
            margin=go.layout.Margin(
                l=0, 
                r=0, 
                b=25, 
                t=25, 
                pad = 0
                )
            )
        

        #Create the Analysis to be placed under the graph
        #observed frequency
        stats1 = pd.DataFrame(columns=['Month'])
        
        #projected frequency
        stats2 = pd.DataFrame(columns=['Month'])
        
        #observed tendency
        stats3 = pd.DataFrame(columns=['Month'])
        
        #projected tendency
        stats4 = pd.DataFrame(columns=['Month'])
        
        
        #seasonal observed
        seasonalDF = pd.DataFrame(columns=['Month'])
        
        #seasonal project
        seasonalDF2 = pd.DataFrame(columns=['Month'])
        
        #standardDeviation Observed
        stats5 = pd.DataFrame(columns=['Month'])
        
        #standard deviation Projected
        stats6 = pd.DataFrame(columns=['Month'])
        
        
        #variance observed
        stats7 = pd.DataFrame(columns=['Month'])
        
        #variance projected
        stats8 = pd.DataFrame(columns=['Month'])
        
        
        #Bias
        biasDF = pd.DataFrame(columns=['Month'])
        
       #monthly median stats observed
        medianMonthlyObs = pd.DataFrame(columns=['Month'])
        
        #monthly median stats predicted
        medianMonthlyProj = pd.DataFrame(columns=['Month'])
       
    
        #get number of years in the date range and create them as columns  
        for i in range(startDate.year,(endDate.year+1)):
            stats1[i] = ""
            stats2[i] = ""
            stats3[i] = ""
            stats4[i] = ""
            stats5[i] = ""
            stats6[i] = ""
            stats7[i] = ""
            stats8[i] = ""
            medianMonthlyObs[i] = ""
            medianMonthlyProj[i] = ""
            biasDF[i] = ""
            seasonalDF[i] = ""
            seasonalDF2[i] = ""
            
        #fill in the months Column
        months = ['January','February','March','April','May','June','July','August','September','October','November','December']
        for i in months:
            stats1 = stats1.append({'Month': i}, ignore_index=True)
            stats2 = stats2.append({'Month': i}, ignore_index=True)
            stats3 = stats3.append({'Month': i}, ignore_index=True)
            stats4 = stats4.append({'Month': i}, ignore_index=True)
            stats5 = stats5.append({'Month': i}, ignore_index=True)
            stats6 = stats6.append({'Month': i}, ignore_index=True)
            stats7 = stats7.append({'Month': i}, ignore_index=True)
            stats8 = stats8.append({'Month': i}, ignore_index=True)
            medianMonthlyObs = medianMonthlyObs.append({'Month': i}, ignore_index=True)
            medianMonthlyProj = medianMonthlyProj.append({'Month': i}, ignore_index=True)
            biasDF = biasDF.append({'Month': i}, ignore_index=True)
            seasonalDF = seasonalDF.append({'Month': i}, ignore_index=True)
            seasonalDF2 = seasonalDF2.append({'Month': i}, ignore_index=True)
        
        #fill in the rows with 0/0
        
        stats1.fillna("0/0", inplace=True)
        stats2.fillna("0/0", inplace=True)
        stats3.fillna("0", inplace=True)
        stats4.fillna("0", inplace=True)
        stats5.fillna("0", inplace=True)
        stats6.fillna("0", inplace=True)
        stats7.fillna("0", inplace=True)
        stats8.fillna("0", inplace=True)
        medianMonthlyObs.fillna("0", inplace=True)
        medianMonthlyProj.fillna("0", inplace=True)
        biasDF.fillna("0/0", inplace=True)
        seasonalDF.fillna("0", inplace=True)
        seasonalDF2.fillna("0", inplace=True)
        

        #now loop through each row in data_all, and 
        #THIS IS FOR FREQUENCY for Stats 1 and 2
        rowit = data_all.iterrows()
        
        for i, row in rowit:
            
            #now for each row we check the month
            #then we declare our normal based on the month
            #then we compare with the normal to determine which count it goes in
            currDate = dt.datetime.strptime(data_all.at[i,'Date'], '%Y-%m-%d')  
            
            currMonth = currDate.month - 1
            
            currYear = currDate.year
           
            newValObs = data_all.at[i,'Observed'+variable]
            newValProj = data_all.at[i,'Model'+variable]
            
            newBias = data_all.at[i,'Bias']
            
                  
            if(currMonth == 0):
                normal = 48.67    
            elif(currMonth == 1):
                normal = 47.7
            elif(currMonth == 2):
                normal = 49.8
            elif(currMonth == 3):
                normal = 68.5
            elif(currMonth == 4):
                normal = 74.3
            elif(currMonth == 5):
                normal = 71.5
            elif(currMonth == 6):
                normal = 75.7
            elif(currMonth == 7):
                normal = 78.1
            elif(currMonth == 8):
                normal = 74.5
            elif(currMonth == 9):
                normal = 61.1
            elif(currMonth == 10):
                normal = 75.1
            elif(currMonth == 11):
                normal = 57.9
            
            
            currValObs = stats1.at[(currMonth),currYear]
            
            overObs = currValObs.split("/",1)[0]
            underObs = currValObs.split("/",1)[1]
            
            currValProj = stats2.at[(currMonth),currYear]
            
            overProj = currValProj.split("/",1)[0]
            underProj = currValProj.split("/",1)[1]
              
                
            currentBias = biasDF.at[(currMonth),currYear]
            posBias = currentBias.split("/",1)[0]
            negBias = currentBias.split("/",1)[1]
           
            #the bias threshold is based on variable
            biasThreshold = 0
            
            if variable == 'tas':                  
                biasThreshold = 1
            elif variable == 'pr' :
                biasThreshold = 1

            elif variable == 'ps' :
                biasThreshold = 0.5

            elif variable == 'sfcWind' :
                biasThreshold = 5

            elif variable == 'sfcWindmax' :
                biasThreshold = 5

            elif variable == 'tasmax' :
                biasThreshold = 1

            elif variable == 'tasmin' :
                biasThreshold = 1

        
            
            
            
            if newBias > biasThreshold:
                posBias = int(posBias) + 1
            elif newBias < (biasThreshold * -1):
                negBias = int(negBias) + 1
            else:
                posBias = int(posBias)
                negBias = int(negBias)
            
                
            if newValObs > normal:
                overObs = int(overObs) + 1     
            else:
                underObs = int(underObs) + 1
                
            if newValProj > normal:
                overProj = int(overProj) + 1     
            else:
                underProj = int(underProj) + 1
                 
                
            #overwrite the value
            stats1.at[(currMonth),currYear] = str(overObs) + "/" + str(underObs)
            stats2.at[(currMonth ),currYear] = str(overProj) + "/" + str(underProj)
            
            
            #seasonal data
            seasonalDF.at[(currMonth ),currYear] = newValObs
            seasonalDF2.at[(currMonth ),currYear] = newValProj
           
            #bias
            biasDF.at[(currMonth ),currYear] = str(posBias) + "/" + str(negBias)
                  
        
        #CENTRAL TENDENCY 
        
        temp_monthly = data_all
        temp_monthly['Date'] = pd.to_datetime(temp_monthly['Date'])
        temp_monthly = (temp_monthly.set_index('Date').resample('M').mean())
        
        temp_monthly_median = data_all
        temp_monthly_median['Date'] = pd.to_datetime(temp_monthly_median['Date'])
        temp_monthly_median = (temp_monthly_median.set_index('Date').resample('M').median())
        
       
        temp_yearly = data_all
        temp_yearly['Date'] = pd.to_datetime(temp_yearly['Date'])
        temp_yearly = (temp_yearly.set_index('Date').resample('Y').mean())
        
        temp_yearly_median = data_all
        temp_yearly_median['Date'] = pd.to_datetime(temp_yearly_median['Date'])
        temp_yearly_median = (temp_yearly_median.set_index('Date').resample('Y').median())
       
        #now that we have monthly and yearly resampled, place them in matrix
        stats3 = stats3.append({'Month': 'Annual'}, ignore_index=True)
        stats4 = stats4.append({'Month': 'Annual'}, ignore_index=True)
        
        #monthly median in dataframe
        medianMonthlyObs = medianMonthlyObs.append({'Month': 'Annual'}, ignore_index=True)
        medianMonthlyProj = medianMonthlyProj.append({'Month': 'Annual'}, ignore_index=True)
        
        rowit = temp_monthly.iterrows()  
        
        row_median = temp_monthly_median.iterrows()
        
        temp_monthly['Date'] = temp_monthly.index
        temp_monthly_median['Date'] = temp_monthly_median.index
         
        temp_monthly = temp_monthly.round({'Observed'+variable: 2, 'Model'+variable: 2})
        temp_monthly_median = temp_monthly_median.round({'Observed'+variable: 2, 'Model'+variable: 2})  
        temp_yearly = temp_yearly.round({'Observed'+variable: 2, 'Model'+variable: 2})
        temp_yearly_median = temp_yearly_median.round({'Observed'+variable: 2, 'Model'+variable: 2})
           
        
        #add monthly means
        for i, row in rowit:
            currDate = temp_monthly.at[i,'Date']
            
            currMonth = currDate.month
            
            currYear = currDate.year
            
            
            stats3.at[(currMonth),currYear] = temp_monthly.at[i,'Observed'+variable]
            stats4.at[(currMonth),currYear] = temp_monthly.at[i,'Model'+variable]
        
            
      
         #add monthly median
        for i, row in row_median:
            currDate = temp_monthly_median.at[i,'Date']
            
            currMonth = currDate.month
            
            currYear = currDate.year
            
            
            medianMonthlyObs.at[(currMonth ),currYear] = temp_monthly_median.at[i,'Observed'+variable]
            medianMonthlyProj.at[(currMonth),currYear] = temp_monthly_median.at[i,'Model'+variable]
        
            
        temp_yearly['Date'] = temp_yearly.index
        rowitYear = temp_yearly.iterrows()
        
        
        
        #add monthly means
        for i, row in rowitYear:
            currDate = temp_yearly.at[i,'Date']
            
            currMonth = currDate.month
            
            currYear = currDate.year
            
            
            stats3.at[12,currYear] = temp_yearly.at[i,'Observed'+variable]
            stats4.at[12,currYear] = temp_yearly.at[i,'Model'+variable]
        
           
        
        
        
        
        
        temp_yearly_median['Date'] = temp_yearly_median.index
        rowitYear_median = temp_yearly_median.iterrows()
         #add yearly medians
        for i, row in rowitYear_median:
            currDate = temp_yearly_median.at[i,'Date']
            
            currMonth = currDate.month
            
            currYear = currDate.year
            
            
            medianMonthlyObs.at[12,currYear] = temp_yearly_median.at[i,'Observed'+variable]
            medianMonthlyProj.at[12,currYear] = temp_yearly_median.at[i,'Model'+variable]
        
           
        
        
        
        
        
        
        
        #STANDARD DEVIATION
        
        stats5 = stats5.append({'Month': 'Annual'}, ignore_index=True)
        stats6 = stats6.append({'Month': 'Annual'}, ignore_index=True)
        
        temp_monthly_std = data_all
        temp_monthly_std['Date'] = pd.to_datetime(temp_monthly_std['Date'])
        temp_monthly_std = (temp_monthly_std.set_index('Date').resample('M').std())
        
       
        
        temp_yearly_std = data_all
        temp_yearly_std['Date'] = pd.to_datetime(temp_yearly_std['Date'])
        temp_yearly_std = (temp_yearly_std.set_index('Date').resample('Y').std())
        
        
        
         
        rowit = temp_monthly_std.iterrows()  
        
        temp_monthly_std['Date'] = temp_monthly_std.index
         
        temp_monthly_std = temp_monthly_std.round({'Observed'+variable: 2, 'Model'+variable: 2})    
        temp_yearly_std = temp_yearly_std.round({'Observed'+variable: 2, 'Model'+variable: 2})
           
        
        #add monthly means
        for i, row in rowit:
            currDate = temp_monthly_std.at[i,'Date']
            
            currMonth = currDate.month
            
            currYear = currDate.year
            
            
            stats5.at[(currMonth),currYear] = temp_monthly_std.at[i,'Observed'+variable]
            stats6.at[(currMonth),currYear] = temp_monthly_std.at[i,'Model'+variable]
        
            
      
        temp_yearly_std['Date'] = temp_yearly_std.index
        rowitYear = temp_yearly_std.iterrows()
        #add monthly means
        for i, row in rowitYear:
            currDate = temp_yearly_std.at[i,'Date']
            
            currMonth = currDate.month
            
            currYear = currDate.year
            
            
            stats5.at[12,currYear] = temp_yearly_std.at[i,'Observed'+variable]
            stats6.at[12,currYear] = temp_yearly_std.at[i,'Model'+variable]
        
           
        
        
        
        
        
        
        #add monthly means
        for i, row in rowit:
            currDate = temp_monthly_var.at[i,'Date']
            
            currMonth = currDate.month
            
            currYear = currDate.year
            
            
            stats7.at[(currMonth),currYear] = temp_monthly_var.at[i,'Observed'+variable]
        
        
        #Anual Precip
        temp_yearly_precip = data_all
        temp_yearly_precip['Date'] = pd.to_datetime(temp_yearly_precip['Date'])
        temp_yearly_precip = (temp_yearly_precip.set_index('Date').resample('Y').sum())
       
        temp_yearly_precip['Date'] = temp_yearly_precip.index
        
        #anual precip observed
        anualPrecip = pd.DataFrame()

        anualPrecip['Year'] = temp_yearly_precip['Date'].dt.year
        anualPrecip['Observed'] =  temp_yearly_precip['Observed'+variable]
        anualPrecip['Projected'] =  temp_yearly_precip['Model'+variable]
        
        anualPrecip = anualPrecip.round({'Observed': 2, 'Projected': 2})
        
        
        #box plots
        #create a df for both positive and negative
        
        #firstly pull the data
        bias=pd.read_csv(user_key['projectedvsobservedbias_mapped']+ variable+'_comparison_bias_output.csv')
        
        bias['Date'] = pd.to_datetime(bias['Date'])
        bias.reset_index(inplace=True)

        
        
        # do bias data
        bias['year'] = [dt.datetime.year for d in bias.Date]
        bias['month'] = [dt.datetime.month for d in bias.Date]
        years = bias['year'].unique()

        
        
        
        # Draw box plots
        
        #to do this we must create a new column listing month and year
        
        #this is the monthly breakdown
        temp_box = data_all
        
        
        
        temp_box['month_year'] = temp_box['Date'].dt.strftime('%Y-%m')

        boxfig1 = px.box(temp_box,x = "month_year", y = "Observed" +variable)
      
        boxfig2 = px.box(temp_box,x = "month_year", y = "Model" +variable)
          
           
        
        
        
        #this is for the year
            
        temp_box_year = data_all
        
        
        
        temp_box_year['year'] = temp_box_year['Date'].dt.strftime('%Y')

        boxfig3 = px.box(temp_box_year,x = "year", y = "Observed" +variable)
      
        boxfig4 = px.box(temp_box_year,x = "year", y = "Model" +variable)
          

            
        #print(boxfig4.hoverinfo)
        
        boxfig1.update_xaxes(
            title = "Month, Year"
        )
        boxfig1.update_yaxes(
            title = columnName + " " +   measurement
        )
        
        
        boxfig2.update_xaxes(
            title = "Month, Year"
        )
        boxfig2.update_yaxes(
            title = columnName + " " +   measurement
        )
        
        
        
        boxfig3.update_xaxes(
            title = "Year"
        )
        boxfig3.update_yaxes(
            title = columnName + " " +   measurement
        )
        
        
        
        boxfig4.update_xaxes(
            title = "Year"
        )
        boxfig4.update_yaxes(
            title = columnName + " " +   measurement
        )
        
        #print(boxfig3.hover_data())
            
            
        tempdataMonth = data_all
        tempdataMonth['Date'] = pd.to_datetime(tempdataMonth['Date'])
        tempdataMonth = (tempdataMonth.set_index('Date').resample('M').var())
        tempdataMonth['Date'] = tempdataMonth.index
        #create the data for the box figures
        
        
        #use temp_box for monthwise
        temp_monthly_box = pd.DataFrame()
        
        temp_box = data_all
        temp_box['Date'] = pd.to_datetime(temp_box['Date'])
        temp_box = (temp_box.set_index('Date'))
        temp_box['Date'] = temp_box.index
        
        date_monthly_obs = tempdataMonth['Date']
        
        
        
        
        median_monthly = temp_box["Observed" +variable].groupby(pd.Grouper(freq="M")).median()
        first_monthly = temp_box["Observed" +variable].groupby(pd.Grouper(freq="M")).quantile(0.25)
        third_monthly = temp_box["Observed" +variable].groupby(pd.Grouper(freq="M")).quantile(0.75)
        tempOBSBOX = temp_box["Observed" +variable].groupby(pd.Grouper(freq="M"))
        
        median_monthly_proj = temp_box["Model" +variable].groupby(pd.Grouper(freq="M")).median()
        first_monthly_proj = temp_box["Model" +variable].groupby(pd.Grouper(freq="M")).quantile(0.25)
        third_monthly_proj = temp_box["Model" +variable].groupby(pd.Grouper(freq="M")).quantile(0.75)
        
        
        median_yearly = temp_box["Observed" +variable].groupby(pd.Grouper(freq="Y")).median()
        first_yearly = temp_box["Observed" +variable].groupby(pd.Grouper(freq="Y")).quantile(0.25)
        third_yearly = temp_box["Observed" +variable].groupby(pd.Grouper(freq="Y")).quantile(0.75)
        
        median_yearly_proj = temp_box["Model" +variable].groupby(pd.Grouper(freq="Y")).median()
        first_yearly_proj = temp_box["Model" +variable].groupby(pd.Grouper(freq="Y")).quantile(0.25)
        third_yearly_proj = temp_box["Model" +variable].groupby(pd.Grouper(freq="Y")).quantile(0.75)
      
        
        iqr = third_monthly - first_monthly

        fence_low  = first_monthly - (1.5*iqr)
        fence_high = third_monthly + (1.5*iqr)
        
        fence_low = fence_low.to_frame()
        
        fence_high = fence_high.to_frame()
        
        #print(fence_high)
        currMonth = 0
        prevMonth = 0
        tempx = 0 #this will count the fence_low and fence_high, incrementing when month changed
            
        newDf = temp_box
        #pd.set_option("display.max_rows", None, "display.max_columns", None)
        #print(newDf)
        
        for index, row  in newDf.iterrows():
            #go over each row
            #check which month and year and based on that grab the proper fences
            #once you have them 
            currDate = newDf.at[index,'Date']
            
            #now grab the year and month of the date
            #currDate = dt.datetime.strptime(currDate,'%Y-%m-%d')
            
            #now get current month
            currMonth = currDate.month
            
            
            #if curr Month and previous month are not same then we increase tempx 
            #and make previous month into current
            if prevMonth != currMonth:
                if (prevMonth != 0):
                    tempx = tempx + 1
                
                prevMonth = currMonth
               
            
            
            currLow = fence_low.iat[tempx,0]
            currHigh = fence_high.iat[tempx,0]
            #print ("tempx : " + str(tempx) + " currHigh : " + str(currHigh) )    
            #now we remove rows from newDf based on low and high
            if (newDf.at[index,"Observed" +variable] > currHigh) or (newDf.at[index,"Observed" +variable] < currLow ):
                #drop if the value is outside the range
                #print( "current newDf var: " + str(newDf.at[index,"Observed" +variable]) +  " current high : " + str(currHigh) + " current Date:" + str(currDate))
                newDf.drop(index, inplace=True)   
            
            
            
            
            
            
            
            
            
        #df_out = temp_box.query('(@first_monthly - 1.5 * @iqr) <= ' + "Observed" +variable + ' <= (@third_monthly + 1.5 * @iqr)')
        
        
        #df_out = (temp_box["Observed" +variable] >= fence_low) & (temp_box["Observed" +variable] <= fence_high)
        #return df.loc[filter]
        
        #df_out = temp_box.loc[(temp_box["Observed" +variable].groupby(pd.Grouper(freq="M")).min() > fence_low) & (temp_box["Observed" +variable].groupby(pd.Grouper(freq="M")).min() < fence_high)]
        
         #df_out = temp_box[(np.abs(stats.zscore(temp_box[1])) < 3)]
        max_monthly = newDf["Observed" +variable].groupby(pd.Grouper(freq="M")).max()
        min_monthly = newDf["Observed" +variable].groupby(pd.Grouper(freq="M")).min()
        
        
        
        
        
        
        temp_monthly_box.insert(0,'Date',date_monthly_obs)                                
        temp_monthly_box.insert(1, 'Minimum', min_monthly)
        temp_monthly_box.insert(2, 'First Quartile', first_monthly) 
        temp_monthly_box.insert(3, 'Median', median_monthly)
        temp_monthly_box.insert(4, 'Third Quartile', third_monthly)
        temp_monthly_box.insert(5, 'Maximum', max_monthly)                                            
            
            
        temp_monthly_box['Date'] = temp_monthly_box['Date'].dt.strftime('%b, %Y')
        #projected                                            
        temp_monthly_proj = pd.DataFrame()
                                                  
        date_monthly_proj = tempdataMonth['Date']                                             
        #max_monthly_proj = temp_box["Model" +variable].groupby(pd.Grouper(freq="M")).max()
        #min_monthly_proj = temp_box["Model" +variable].groupby(pd.Grouper(freq="M")).min()
#         median_monthly_proj = temp_box["Model" +variable].groupby(pd.Grouper(freq="M")).median()
#         first_monthly_proj = temp_box["Model" +variable].groupby(pd.Grouper(freq="M")).quantile(0.25)
#         third_monthly_proj = temp_box["Model" +variable].groupby(pd.Grouper(freq="M")).quantile(0.75)
        
        iqr2 = third_monthly_proj - first_monthly_proj
        fence_low2  = first_monthly_proj - (1.5*iqr2)
        fence_high2 = third_monthly_proj + (1.5*iqr2)
        
        
        
        fence_low2 = fence_low2.to_frame()
        
        fence_high2 = fence_high2.to_frame()
        
        #print(fence_high)
        currMonth = 0
        prevMonth = 0
        tempx = 0 #this will count the fence_low and fence_high, incrementing when month changed
        currLow = 0
        currHigh = 0
        newDf2 = temp_box
        #pd.set_option("display.max_rows", None, "display.max_columns", None)
        #print(newDf)
        
        for index, row  in newDf2.iterrows():
            #go over each row
            #check which month and year and based on that grab the proper fences
            #once you have them 
            currDate = newDf2.at[index,'Date']
            
            #now grab the year and month of the date
            #currDate = dt.datetime.strptime(currDate,'%Y-%m-%d')
            
            #now get current month
            currMonth = currDate.month
            
            
            #if curr Month and previous month are not same then we increase tempx 
            #and make previous month into current
            if prevMonth != currMonth:
                if (prevMonth != 0):
                    tempx = tempx + 1
                
                prevMonth = currMonth
               
            
            
            currLow = fence_low2.iat[tempx,0]
            currHigh = fence_high2.iat[tempx,0]
            #print ("tempx : " + str(tempx) + " currHigh : " + str(currHigh) )    
            #now we remove rows from newDf based on low and high
            if (newDf2.at[index,"Model" +variable] > currHigh) or (newDf2.at[index,"Model" +variable] < currLow ):
                #drop if the value is outside the range
                #print( "current newDf var: " + str(newDf.at[index,"Observed" +variable]) +  " current high : " + str(currHigh) + " current Date:" + str(currDate))
                newDf2.drop(index, inplace=True)   
            
            
        
        pd.set_option("display.max_rows", None, "display.max_columns", None)
        #print(newDf2)
        max_monthly_proj = newDf2["Model" +variable].groupby(pd.Grouper(freq="M")).max()
        min_monthly_proj = newDf2["Model" +variable].groupby(pd.Grouper(freq="M")).min()
        
        
        
        
        
        
        temp_monthly_proj.insert(0,'Date',date_monthly_proj)                                
        temp_monthly_proj.insert(1, 'Minimum', min_monthly_proj)
        temp_monthly_proj.insert(2, 'First Quartile', first_monthly_proj)
        temp_monthly_proj.insert(3, 'Median', median_monthly_proj)
        temp_monthly_proj.insert(4, 'Third Quartile', third_monthly_proj)
        temp_monthly_proj.insert(5, 'Maximum', max_monthly_proj)                                    
       
        temp_monthly_proj['Date'] = temp_monthly_proj['Date'].dt.strftime('%b, %Y')
        
        
        tempdataYear = data_all
        tempdataYear['Date'] = pd.to_datetime(tempdataYear['Date'])
        tempdataYear = (tempdataYear.set_index('Date').resample('Y').var())
        tempdataYear['Date'] = tempdataYear.index
        
        temp_yearly_box = pd.DataFrame()
        
        #temp_yearly_box['Date'] = temp_yearly_box.index
        
        date_yearly = tempdataYear['Date']             
        #max_yearly = temp_box["Observed" +variable].groupby(pd.Grouper(freq="Y")).max()
        #min_yearly = temp_box["Observed" +variable].groupby(pd.Grouper(freq="Y")).min()
        
        iqr3 = third_yearly - first_yearly
        fence_low3  = first_yearly - (1.5*iqr3)
        fence_high3 = third_yearly + (1.5*iqr3)
        
        fence_low3 = fence_low3.to_frame()
        
        fence_high3 = fence_high3.to_frame()
        
        #print(fence_high)
        currYear = 0
        prevYear = 0
        tempx = 0 #this will count the fence_low and fence_high, incrementing when month changed
            
        newDf3 = temp_box
        #pd.set_option("display.max_rows", None, "display.max_columns", None)
        #print(newDf)
        
        for index, row  in newDf3.iterrows():
            #go over each row
            #check which month and year and based on that grab the proper fences
            #once you have them 
            currDate = newDf3.at[index,'Date']
            
            #now grab the year and month of the date
            #currDate = dt.datetime.strptime(currDate,'%Y-%m-%d')
            
            #now get current year
            currYear = currDate.year
            
            
            #if curr Month and previous month are not same then we increase tempx 
            #and make previous month into current
            if prevYear != currYear:
                if (prevYear != 0):
                    tempx = tempx + 1
                
                prevYear = currYear
               
            
            
            currLow = fence_low3.iat[tempx,0]
            currHigh = fence_high3.iat[tempx,0]
            #print ("tempx : " + str(tempx) + " currHigh : " + str(currHigh) )    
            #now we remove rows from newDf based on low and high
            if (newDf3.at[index,"Observed" +variable] > currHigh) or (newDf3.at[index,"Observed" +variable] < currLow ):
                #drop if the value is outside the range
                #print( "current newDf var: " + str(newDf.at[index,"Observed" +variable]) +  " current high : " + str(currHigh) + " current Date:" + str(currDate))
                newDf3.drop(index, inplace=True)   
            
            
        
        max_yearly = newDf3["Observed" +variable].groupby(pd.Grouper(freq="Y")).max()
        min_yearly = newDf3["Observed" +variable].groupby(pd.Grouper(freq="Y")).min()
        
        
        
        
        
        
        
        
        
        
        
        
        temp_yearly_box.insert(0,'Date',date_yearly)    
        temp_yearly_box.insert(1, 'Minimum', min_yearly)
        temp_yearly_box.insert(2, 'First Quartile', first_yearly)
        temp_yearly_box.insert(3, 'Median', median_yearly)
        temp_yearly_box.insert(4, 'Third Quartile', third_yearly)
        temp_yearly_box.insert(5, 'Maximum', max_yearly)     
        
        temp_yearly_box['Date'] = temp_yearly_box['Date'].dt.strftime('%Y')
        
        temp_yearly_proj = pd.DataFrame()
                                                  
        date_yearly_proj = tempdataYear['Date']                                                
  
         
        iqr4 = third_yearly_proj - first_yearly_proj
        fence_low4  = first_yearly_proj - (1.5*iqr4)
        fence_high4 = third_yearly_proj + (1.5*iqr4)
        
        fence_low4 = fence_low4.to_frame()
        
        fence_high4 = fence_high4.to_frame()
        
        #print(fence_high)
        currYear = 0
        prevYear = 0
        tempx = 0 #this will count the fence_low and fence_high, incrementing when month changed
            
        newDf4 = temp_box
        #pd.set_option("display.max_rows", None, "display.max_columns", None)
        #print(newDf)
        
        for index, row  in newDf4.iterrows():
            #go over each row
            #check which month and year and based on that grab the proper fences
            #once you have them 
            currDate = newDf4.at[index,'Date']
            
            #now grab the year and month of the date
            #currDate = dt.datetime.strptime(currDate,'%Y-%m-%d')
            
            #now get current month
            currMonth = currDate.year
            
            
            #if curr Month and previous month are not same then we increase tempx 
            #and make previous month into current
            if prevYear != currYear:
                if (prevYear != 0):
                    tempx = tempx + 1
                
                prevYear = currYear
               
            
            
            currLow = fence_low4.iat[tempx,0]
            currHigh = fence_high4.iat[tempx,0]
            #print ("tempx : " + str(tempx) + " currHigh : " + str(currHigh) )    
            #now we remove rows from newDf based on low and high
            if (newDf4.at[index,"Model" +variable] > currHigh) or (newDf4.at[index,"Model" +variable] < currLow ):
                #drop if the value is outside the range
                #print( "current newDf var: " + str(newDf.at[index,"Observed" +variable]) +  " current high : " + str(currHigh) + " current Date:" + str(currDate))
                newDf4.drop(index, inplace=True)   
            
            
        pd.set_option("display.max_rows", None, "display.max_columns", None)
        print(newDf4["Model" +variable].groupby(pd.Grouper(freq="Y")))
        print("AHHHHHHHHH NEW UHSAUDUH UISHAUI DH")
        
        max_yearly_proj = newDf4["Model" +variable].groupby(pd.Grouper(freq="Y")).max()
        min_yearly_proj = newDf4["Model" +variable].groupby(pd.Grouper(freq="Y")).min()
        
        
        pd.set_option("display.max_rows", None, "display.max_columns", None)
        print(min_yearly_proj)
        
        
        
        
        
        temp_yearly_proj.insert(0,'Date',date_yearly_proj)                                
        temp_yearly_proj.insert(1, 'Minimum', min_yearly_proj)
        temp_yearly_proj.insert(2, 'First Quartile', first_yearly_proj)
        temp_yearly_proj.insert(3, 'Median', median_yearly_proj)
        temp_yearly_proj.insert(4, 'Third Quartile', third_yearly_proj)
        temp_yearly_proj.insert(5, 'Maximum', max_yearly_proj)                                    
        
        temp_yearly_proj['Date'] = temp_yearly_proj['Date'].dt.strftime('%Y')
        
        
        #use temp_box_year for year wise 
            
        
        #seasonal plot here
        #have to creat a DF where each year is a column and one column is the month
        #under the month column is simply months, and under the year column is the values
        
        
        temp_yearly_proj = temp_yearly_proj.round(2)
        temp_yearly_box = temp_yearly_box.round(2)
        
        temp_monthly_proj = temp_monthly_proj.round(2)
        temp_monthly_box = temp_monthly_box.round(2)
        
        
        seasonalfig = px.line(seasonalDF, x="Month", y=seasonalDF.columns)
        
 
        seasonalfig.update_yaxes(
            title = columnName + " " +   measurement
        )
        seasonalfig.update_layout(title = "Observed "+ columnName+ " Seasonality Plots",legend_title=dict(text = "Year"))
        
        seasonalfig2 = px.line(seasonalDF2, x="Month", y=seasonalDF.columns)
        
        boxfig3.update_layout(title = 'Observed ' + columnName + ': Year-wise Box Plots')
        
        boxfig4.update_layout(title = 'Predicted ' + columnName + ': Year-wise Box Plots')
        
        boxfig1.update_layout(title = 'Observed ' + columnName + ': Month-wise Box Plots')
        
        boxfig2.update_layout(title = 'Predicted ' + columnName + ': Month-wise Box Plots')

        seasonalfig2.update_yaxes(
            title = columnName + " " +   measurement
        )
        seasonalfig2.update_layout(title = "Predicted "+ columnName+ " Seasonality Plots",legend_title=dict(text = "Year"))
        
        
        tempfig = make_subplots(specs=[[{"secondary_y": True}]])
        
      
        
        tempfig.add_trace(go.Scatter(x=data_all['Date'], y=data_all['Bias'], fill='tozeroy', name = "Bias"),secondary_y=True) # fill to trace0 y
        tempfig.add_trace(go.Scatter(x=data_all['Date'], y=data_all["Observed" +variable], name = "Observed"),secondary_y=False) # fill down to xaxis
        tempfig.update_layout(
            title_x=0.5,
            xaxis_title="Date",
            yaxis_title=columnName + ' ' + measurement,
            showlegend=True,
            yaxis_range=[-75,150],
#             margin=dict(l=5,r=5,b=0,t=5,(specs=[[{“secondary_y”: True}]])pad=5)
            )
        tempfig.update_yaxes(title = "Bias", range = [-75,150],secondary_y = True)
        tempfig.update_layout(title = 'Bias Graph')
        
        
        
        
#        pio.kaleido.scope.mathjax = None
        #print out all figs
#         fig.write_image("Images/MainGraph.png",engine='orca')
#         tempfig.write_image("Images/Biasfig.png",engine='orca')
#         boxfig1.write_image("Images/Boxfig1.png",engine='orca')
#         boxfig2.write_image("Images/Boxfig2.png",engine='orca')
#         boxfig3.write_image("Images/Boxfig3.png",engine='orca')
#         boxfig4.write_image("Images/Boxfig4.png",engine='orca')
#         seasonalfig.write_image("Images/Seasonalfig1.png",engine='orca')
#         seasonalfig2.write_image("Images/Seasonalfig2.png",engine='orca')

        print(temp_yearly_proj)
        print(boxfig4)
        if variable == 'pr':         
            percipValue ={'float' : 'left','margin' : '10px','width': '800px', 'display': 'inline-block'}
            percipValueRight ={'float' : 'right','margin' : '10px','width': '800px', 'display': 'inline-block'}
        else:
            percipValue ={'float' : 'left','margin' : '10px','width': '800px', 'display': 'none'}
            percipValueRight ={'float' : 'right','margin' : '10px','width': '800px', 'display': 'none'}
            
        if variable == 'rlds':        
            biasShow ={'float' : 'right','margin' : '10px','width': '800px', 'display': 'none'}
        else:
            biasShow ={'float' : 'right','margin' : '10px','width': '800px', 'display': 'inline-block'}
        
   #     print(str(percipValue)) 
#         biasfig = go.Figure(data=go.Scatter(
#                     x=data_all['Date'],
#                     y=data_all["Observed" +variable],
#                     xhoverformat="%d %b, %Y",
#                     yhoverformat = ".2f",
#                     error_y=dict(
#                         type='data',
#                         array=data_all['Bias']
#                     )))

#         biasfig.update_yaxes(title_text="Observed Value of " + columnName, secondary_y=False)
#         biasfig.update_yaxes(title_text="Error Bar Value", secondary_y=True)

        #create the output that will go on the page
        
        graph = html.Div([
            html.Div(id = 'graphDIV', children =[
                html.Button("Download Data Model", id="btn_csv_auto",style={'background-color': '#4CAF50','border': 'none','color': 'white','padding': '15px 32px','text-align': 'center','text-decoration': 'none','display': 'inline-block','font-size': '16px','margin': '4px 2px'}),
                dcc.Download(id="download-dataframe-csv-auto"),
                (dcc.Graph(
                   id='Graph1',
                   figure=fig,
                    style={
                        'height' : '300px', 
                        'margin' : '50px'
                    }
               ))
            ],style = {'display': 'inline-block'}),
            
            
            html.Div(id = 'frequencyObs', children=[
            html.Div([
                html.Button("Download Analysis", id="btn_analysis_auto",style={'background-color': '#4CAF50','border': 'none','color': 'white','padding': '15px 32px','text-align': 'center','text-decoration': 'none','display': 'inline-block','font-size': '16px','margin': '4px 2px'}),
                dcc.Download(id="download-analysis-auto"),
                    ],style={'float' : 'left','margin' : '10px','margin-top': '350px','width': '100%', 'display': 'inline-block'}),
            
            html.Div([
            html.H3('Number of days where observed ' + columnName + ' is >/< than  ECCC 30 year normals', style={'width': '800px','margin' : '10px','font-size': '12px', 'float': 'left', 'font-family': 'Verdana'}),
            dash_table.DataTable(
                id='table',
                columns=[{"name": i, "id": i} for i in stats1.columns],
                data=stats1.to_dict('records'),
            )
            ],style=percipValue),
                
             html.Div([
                 html.H3('Number of days where Predicted ' + columnName + ' is >/< than  ECCC 30 year normal', style={'width': '800px','margin' : '10px','font-size': '12px', 'float': 'left', 'font-family': 'Verdana'}),
                 dash_table.DataTable(
                id='table',
                columns=[{"name": i, "id": i} for i in stats2.columns],
                data=stats2.to_dict('records'),
            )
             ],style=percipValueRight),
                
            html.Div([
                html.H3('Annual ' + columnName + '', style={'width': '800px','font-size': '12px','margin' : '10px', 'font-family': 'Verdana'}),
                dash_table.DataTable(
                id='table',
                columns=[{"name": i, "id": i} for i in anualPrecip.columns],
                data=anualPrecip.to_dict('records'),
                style_cell={
                    'minWidth': '10px', 'width': '10px', 'maxWidth': '10px'
                }
            ),
            ],style=percipValue),
                
            html.Div([],style={'float' : 'left','margin' : '10px','width': '100%', 'display': 'inline-block'}),
            html.Div([
                html.H3('Observed ' + columnName + ': Monthly Means', style={'width': '800px','margin' : '10px', 'font-size': '12px', 'float': 'left', 'font-family': 'Verdana'}),
                dash_table.DataTable(
                id='table',
                columns=[{"name": i, "id": i} for i in stats3.columns],
                data=stats3.to_dict('records')
            ),
            ],style={'float' : 'left','margin' : '10px','width': '800px', 'display': 'inline-block'}),
            html.Div([
                html.H3('Predicted ' + columnName + ': Monthly Means', style={'width': '800px','margin' : '10px','font-size': '12px', 'float': 'left', 'font-family': 'Verdana'}),
                dash_table.DataTable(
                id='table',
                columns=[{"name": i, "id": i} for i in stats4.columns],
                data=stats4.to_dict('records')
               
            ),
            ],style={'float' : 'right','margin' : '10px','width': '800px', 'display': 'inline-block'}),
             html.Div([
                html.H3('Observed ' + columnName + ': Monthly Medians', style={'width': '800px','margin' : '10px', 'font-size': '12px', 'float': 'left', 'font-family': 'Verdana'}),
                dash_table.DataTable(
                id='table',
                columns=[{"name": i, "id": i} for i in medianMonthlyObs.columns],
                data=medianMonthlyObs.to_dict('records')
            ),
            ],style={'float' : 'left','margin' : '10px','width': '800px', 'display': 'inline-block'}),
            html.Div([
                html.H3('Predicted ' + columnName + ': Monthly Medians', style={'width': '800px','margin' : '10px', 'font-size': '12px', 'float': 'left', 'font-family': 'Verdana'}),
                dash_table.DataTable(
                id='table',
                columns=[{"name": i, "id": i} for i in medianMonthlyProj.columns],
                data=medianMonthlyProj.to_dict('records')
            ),
            ],style={'float' : 'right','margin' : '10px','width': '800px', 'display': 'inline-block'}),
            html.Div([
                
                html.H3('Observed ' + columnName + ': Monthly Standard Deviation', style={'width': '800px','margin' : '10px','font-size': '12px', 'float': 'left', 'font-family': 'Verdana'}),
                dash_table.DataTable(
                id='table',
                columns=[{"name": i, "id": i} for i in stats5.columns],
                data=stats5.to_dict('records')
            ),
            ],style={'float' : 'left','margin' : '10px','width': '800px', 'display': 'inline-block'}),
                
            html.Div([
                html.H3('Predicted ' + columnName + ': Monthly Standard Deviation', style={'width': '800px','margin' : '10px','font-size': '12px', 'float': 'left', 'font-family': 'Verdana'}),
                dash_table.DataTable(
                id='table',
                columns=[{"name": i, "id": i} for i in stats6.columns],
                data=stats6.to_dict('records')
            )
                
            ],style={'float' : 'right','margin' : '10px','width': '800px', 'display': 'inline-block'}),
                
            
              
            html.Div([],style={'float' : 'left','margin' : '10px','width': '100%', 'display': 'inline-block'}),
             
            html.Div([
               
                #html.H3('Bias Graph                                        ', style={'width': 'auto','margin' : '10px','font-size': '12px', 'float': 'left', 'font-family': 'Verdana'}),
                (dcc.Graph(
                   id='Graph1',
                   figure=tempfig
                   ))
                
            ],style={'float' : 'left','margin' : '10px','width': '800px', 'display': 'inline-block'}),
                   
              html.Div([
                html.H3('Bias between Predicted and Observed' + columnName + ' ', style={ 'width': '800px','margin' : '10px','font-size': '12px', 'float': 'left', 'font-family': 'Verdana'}),
                dash_table.DataTable(
                id='table',
                columns=[{"name": i, "id": i} for i in biasDF.columns],
                data=biasDF.to_dict('records'))
        
                
            ],style=biasShow),
                
               html.Div([],style={'float' : 'left','margin' : '10px','width': '100%', 'display': 'inline-block'}),
               
               html.Div([
         #       html.H3('Observed ' + columnName + ': Month-wise Box Plots', style={'width': '800px','margin' : '10px','font-size': '12px', 'float': 'left', 'font-family': 'Verdana'}),
                (dcc.Graph(
               id='Graph1',
               figure=boxfig1
                )),
                
            ],style={'float' : 'left','margin' : '10px','width': '800px', 'display': 'inline-block'}),
                   
            html.Div([
                  
       #    html.H3('Projected ' + columnName + ': Month-wise Box Plots', style={ 'width': '800px','margin' : '10px','font-size': '12px', 'float': 'left', 'font-family': 'Verdana'}),        
            (dcc.Graph(
               id='Graph1',
               figure=boxfig2
           )),
                
            ],style={'float' : 'right','margin' : '10px','width': '800px', 'display': 'inline-block'}),
                   

            html.Div([
                dash_table.DataTable(
                id='table',
                columns=[{"name": i, "id": i} for i in temp_monthly_box.columns],
                data=temp_monthly_box.to_dict('records')
            ), 
                
            ],style={'float' : 'left','margin' : '10px','width': '800px', 'display': 'inline-block'}),
                   
            html.Div([
                 dash_table.DataTable(
                id='table',
                columns=[{"name": i, "id": i} for i in temp_monthly_proj.columns],
                data=temp_monthly_proj.to_dict('records')
            ),  
            ],style={'float' : 'right','margin' : '10px','width': '800px', 'display': 'inline-block'}),
                   

            html.Div([
#               html.H3('Observed ' + columnName + ': Year-wise Box Plots', style={'width': '800px','margin' : '10px','font-size': '12px', 'float': 'left', 'font-family': 'Verdana'}),
                (dcc.Graph(
                   id='Graph1',
                   figure=boxfig3
               )),
                
            ],style={'float' : 'left','width': '800px', 'display': 'inline-block'}),
                   
              html.Div([
            #html.H3('Projected ' + columnName + ': Year-wise Box Plots', style={'font-size': '12px', 'float': 'right', 'font-family': 'Verdana'}),
         

            (dcc.Graph(
               id='Graph1',
               figure=boxfig4
           )),
                
            ],style={'float' : 'right','width': '800px', 'display': 'inline-block'}),
                   
                
            html.Div([
               dash_table.DataTable(
                id='table',
                columns=[{"name": i, "id": i} for i in temp_yearly_box.columns],
                data=temp_yearly_box.to_dict('records')
            ),
                
            ],style={'float' : 'left','margin' : '10px','width': '800px', 'display': 'inline-block'}),
                   
              html.Div([
                  
            dash_table.DataTable(
                id='table',
                columns=[{"name": i, "id": i} for i in temp_yearly_proj.columns],
                data=temp_yearly_proj.to_dict('records')
            ),
                
            ],style={'float' : 'right','margin' : '10px','width': '800px', 'display': 'inline-block'}),
                   
                
            html.Div([
#           html.H3('Observed and Projected Precipitation Seasonality Plots', style={'font-size': '12px', 'font-family': 'Verdana'}),
                 (dcc.Graph(
               id='Graph1',
               figure=seasonalfig
           )),
                
            ],style={'float' : 'left','width': '800px', 'display': 'inline-block'}),
                   
              html.Div([
                (dcc.Graph(
                   id='Graph1',
                   figure=seasonalfig2,

               ))
                
            ],style={'float' : 'right','width': '800px', 'display': 'inline-block'}),
                   
        

                
            ],style = {'display':'inline-block','width' : '2000px'})
           
             
              
              
        ])

        return 'Analyze-auto',graph,data_all.to_json(date_format='iso', orient='split'),stats1.to_json(date_format='iso', orient='split'),stats2.to_json(date_format='iso', orient='split'),anualPrecip.to_json(date_format='iso', orient='split'),stats3.to_json(date_format='iso', orient='split'),stats4.to_json(date_format='iso', orient='split'),stats5.to_json(date_format='iso', orient='split'),stats6.to_json(date_format='iso', orient='split'),stats7.to_json(date_format='iso', orient='split'),stats8.to_json(date_format='iso', orient='split'),biasDF.to_json(date_format='iso', orient='split'),temp_monthly_box.to_json(date_format='iso', orient='split'),temp_monthly_proj.to_json(date_format='iso', orient='split'),temp_yearly_box.to_json(date_format='iso', orient='split'),temp_yearly_proj.to_json(date_format='iso', orient='split'),fig
    
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        


#This is here for calculating the Model vs Observed graph and outputting it to the DIV
@app.callback(
    Output("tabs", "value"),
    Output("analyze", "children"),
    Output('main_data','data'),
    Output('observed_normals','data'),
    Output('projected_normals','data'),
    Output('annual_data','data'),
    Output('observed_mean','data'),
    Output('projected_mean','data'),
    Output('observed_deviation','data'),
    Output('projected_deviation','data'),
    Output('observed_variance','data'),
    Output('projected_variance','data'),
    Output('bias_data','data'),
    Output('observed_monthBox','data'),
    Output('projected_monthBox','data'),
    Output('observed_yearBox','data'),
    Output('projected_yearBox','data'),
    Output('mainFig','data'),
    [Input("submit-val", "n_clicks")],
    state=[State(component_id='region', component_property='value'), State('variable', 'value'),State('date-picker-range', 'start_date'),State('date-picker-range', 'end_date')])
def tab_resources(click,region,variable,startDatePicked,endDatePicked):
    #print("testing1234")
    if click:
        
        #this is where we calculate stuff
        #Insert Inputs HERE

        #lat and long are currently not relevant

        #date range (change to read user input)
        #print(startDatePicked)
        startDate = dt.datetime.strptime(startDatePicked,'%Y-%m-%d')
 
        endDate = dt.datetime.strptime(endDatePicked,'%Y-%m-%d') - dt.timedelta(days=1)

        print (startDate)
        print(endDate)
        #variable (change to read user input)
        variable = variable

        
# use this to determine full variable name and measurement unit  
        if variable == 'tas':
                    #then it is TEMP in the data, find the column
            column = 'avg_hourly_temperature'
            columnName = 'Surface Temperature'
            measurement = '(C)'
        elif variable == 'pr' :
            column = 'precipitation'
            columnName = 'Precipitation'
            measurement = '(mm)'

        elif variable == 'ps' :
            column = 'avg_hourly_pressure_station'
            columnName = 'Surface Pressure'
            measurement = '(kPa)'

        elif variable == 'sfcWind' :
            column = 'avg_hourly_wind_speed'
            columnName = 'Surface Wind Speed'
            measurement = '(km/h)'

        elif variable == 'sfcWindmax' :
            column = 'max_wind_speed'
            columnName = 'Maximum Surface Wind Speed'
            measurement = '(km/h)'

        elif variable == 'tasmax' :
            column = 'max_temperature'
            columnName = 'Maximum Surface Temperature'
            measurement = '(C)'

        elif variable == 'tasmin' :
            column = 'min_temperature'
            columnName = 'Minimum Surface Temperature '
            measurement = '(C)'

        elif variable == 'rlds':
            column = 'ALLSKY_SFC_LW_DWN'
            columnName = 'Surface Downwelling Longwave Radiation'
            measurement = '(W m-2)'



        #now we call the mapped csv for this variable
        data = pd.read_csv(user_key['projectedvsobservedbias_mapped']+variable+'_comparison_bias_output.csv')

#         mask = (data['Date'] >= str(startDate.date())) & (data['Date'] <= str(endDate.date()))
#         #only use the data in between the user given range
#         data_all = data.loc[mask]
        data_all = data[data['Date'].between(str(startDate.date()), str(endDate.date()),inclusive='both')]

        #create the plot figures
        fig = make_subplots(rows=2, cols=1, shared_xaxes=False)
        
        fig.add_trace(go.Scatter(x=data_all['Date'], y=data_all['Model'+variable],mode = 'lines+markers', name = "Predicted",xhoverformat="%d %b, %Y" ,yhoverformat = ".2f"))
        fig.add_trace(go.Scatter(x=data_all['Date'], y=data_all['Observed'+variable],mode = 'lines+markers',name = "Observed",xhoverformat="%d %b, %Y" ,yhoverformat = ".2f"))

        #Update the plot layot with titles
        fig.update_layout(
            title_text="Comparison of Predicted and Observed Climate",
            title_x=0.5,
            xaxis_title="Date",
            yaxis_title=columnName + ' ' + measurement,
            showlegend=True,
            autosize=False,
            width=1300,
            height=700,
            
#             margin=dict(l=5,r=5,b=0,t=5,pad=5)
            margin=go.layout.Margin(
                l=0, 
                r=0, 
                b=25, 
                t=25, 
                pad = 0
                )
            )
        

        #Create the Analysis to be placed under the graph
        #observed frequency
        stats1 = pd.DataFrame(columns=['Month'])
        
        #projected frequency
        stats2 = pd.DataFrame(columns=['Month'])
        
        #observed tendency
        stats3 = pd.DataFrame(columns=['Month'])
        
        #projected tendency
        stats4 = pd.DataFrame(columns=['Month'])
        
        
        #seasonal observed
        seasonalDF = pd.DataFrame(columns=['Month'])
        
        #seasonal project
        seasonalDF2 = pd.DataFrame(columns=['Month'])
        
        #standardDeviation Observed
        stats5 = pd.DataFrame(columns=['Month'])
        
        #standard deviation Projected
        stats6 = pd.DataFrame(columns=['Month'])
        
        
        #variance observed
        stats7 = pd.DataFrame(columns=['Month'])
        
        #variance projected
        stats8 = pd.DataFrame(columns=['Month'])
        
        
        #Bias
        biasDF = pd.DataFrame(columns=['Month'])
        
       #monthly median stats observed
        medianMonthlyObs = pd.DataFrame(columns=['Month'])
        
        #monthly median stats predicted
        medianMonthlyProj = pd.DataFrame(columns=['Month'])
       
    
        #get number of years in the date range and create them as columns  
        for i in range(startDate.year,(endDate.year+1)):
            stats1[i] = ""
            stats2[i] = ""
            stats3[i] = ""
            stats4[i] = ""
            stats5[i] = ""
            stats6[i] = ""
            stats7[i] = ""
            stats8[i] = ""
            medianMonthlyObs[i] = ""
            medianMonthlyProj[i] = ""
            biasDF[i] = ""
            seasonalDF[i] = ""
            seasonalDF2[i] = ""
            
        #fill in the months Column
        months = ['January','February','March','April','May','June','July','August','September','October','November','December']
        for i in months:
            stats1 = stats1.append({'Month': i}, ignore_index=True)
            stats2 = stats2.append({'Month': i}, ignore_index=True)
            stats3 = stats3.append({'Month': i}, ignore_index=True)
            stats4 = stats4.append({'Month': i}, ignore_index=True)
            stats5 = stats5.append({'Month': i}, ignore_index=True)
            stats6 = stats6.append({'Month': i}, ignore_index=True)
            stats7 = stats7.append({'Month': i}, ignore_index=True)
            stats8 = stats8.append({'Month': i}, ignore_index=True)
            medianMonthlyObs = medianMonthlyObs.append({'Month': i}, ignore_index=True)
            medianMonthlyProj = medianMonthlyProj.append({'Month': i}, ignore_index=True)
            biasDF = biasDF.append({'Month': i}, ignore_index=True)
            seasonalDF = seasonalDF.append({'Month': i}, ignore_index=True)
            seasonalDF2 = seasonalDF2.append({'Month': i}, ignore_index=True)
        
        #fill in the rows with 0/0
        
        stats1.fillna("0/0", inplace=True)
        stats2.fillna("0/0", inplace=True)
        stats3.fillna("0", inplace=True)
        stats4.fillna("0", inplace=True)
        stats5.fillna("0", inplace=True)
        stats6.fillna("0", inplace=True)
        stats7.fillna("0", inplace=True)
        stats8.fillna("0", inplace=True)
        medianMonthlyObs.fillna("0", inplace=True)
        medianMonthlyProj.fillna("0", inplace=True)
        biasDF.fillna("0/0", inplace=True)
        seasonalDF.fillna("0", inplace=True)
        seasonalDF2.fillna("0", inplace=True)
        
        
        print(data_all)
        #now loop through each row in data_all, and 
        #THIS IS FOR FREQUENCY for Stats 1 and 2
        rowit = data_all.iterrows()
        
        for i, row in rowit:
            
            #now for each row we check the month
            #then we declare our normal based on the month
            #then we compare with the normal to determine which count it goes in
            currDate = dt.datetime.strptime(data_all.at[i,'Date'], '%Y-%m-%d')  
            
            currMonth = currDate.month - 1
            
            currYear = currDate.year
           
            newValObs = data_all.at[i,'Observed'+variable]
            newValProj = data_all.at[i,'Model'+variable]
            
            newBias = data_all.at[i,'Bias']
            
                  
            if(currMonth == 0):
                normal = 48.67    
            elif(currMonth == 1):
                normal = 47.7
            elif(currMonth == 2):
                normal = 49.8
            elif(currMonth == 3):
                normal = 68.5
            elif(currMonth == 4):
                normal = 74.3
            elif(currMonth == 5):
                normal = 71.5
            elif(currMonth == 6):
                normal = 75.7
            elif(currMonth == 7):
                normal = 78.1
            elif(currMonth == 8):
                normal = 74.5
            elif(currMonth == 9):
                normal = 61.1
            elif(currMonth == 10):
                normal = 75.1
            elif(currMonth == 11):
                normal = 57.9
            
            
            currValObs = stats1.at[(currMonth),currYear]
            
            overObs = currValObs.split("/",1)[0]
            underObs = currValObs.split("/",1)[1]
            
            currValProj = stats2.at[(currMonth),currYear]
            
            overProj = currValProj.split("/",1)[0]
            underProj = currValProj.split("/",1)[1]
              
                
            currentBias = biasDF.at[(currMonth),currYear]
            posBias = currentBias.split("/",1)[0]
            negBias = currentBias.split("/",1)[1]
           
            #the bias threshold is based on variable
            biasThreshold = 0
            
            if variable == 'tas':                  
                biasThreshold = 1
            elif variable == 'pr' :
                biasThreshold = 1

            elif variable == 'ps' :
                biasThreshold = 0.5

            elif variable == 'sfcWind' :
                biasThreshold = 5

            elif variable == 'sfcWindmax' :
                biasThreshold = 5

            elif variable == 'tasmax' :
                biasThreshold = 1

            elif variable == 'tasmin' :
                biasThreshold = 1

        
            
            
            
            if newBias > biasThreshold:
                posBias = int(posBias) + 1
            elif newBias < (biasThreshold * -1):
                negBias = int(negBias) + 1
            else:
                posBias = int(posBias)
                negBias = int(negBias)
            
                
            if newValObs > normal:
                overObs = int(overObs) + 1     
            else:
                underObs = int(underObs) + 1
                
            if newValProj > normal:
                overProj = int(overProj) + 1     
            else:
                underProj = int(underProj) + 1
                 
                
            #overwrite the value
            stats1.at[(currMonth),currYear] = str(overObs) + "/" + str(underObs)
            stats2.at[(currMonth ),currYear] = str(overProj) + "/" + str(underProj)
            
            
            #seasonal data
            seasonalDF.at[(currMonth ),currYear] = newValObs
            seasonalDF2.at[(currMonth ),currYear] = newValProj
           
            #bias
            biasDF.at[(currMonth ),currYear] = str(posBias) + "/" + str(negBias)
                  
        
        #CENTRAL TENDENCY 
        
        temp_monthly = data_all
        temp_monthly['Date'] = pd.to_datetime(temp_monthly['Date'])
        temp_monthly = (temp_monthly.set_index('Date').resample('M').mean())
        
        temp_monthly_median = data_all
        temp_monthly_median['Date'] = pd.to_datetime(temp_monthly_median['Date'])
        temp_monthly_median = (temp_monthly_median.set_index('Date').resample('M').median())
        
       
        temp_yearly = data_all
        temp_yearly['Date'] = pd.to_datetime(temp_yearly['Date'])
        temp_yearly = (temp_yearly.set_index('Date').resample('Y').mean())
        
        temp_yearly_median = data_all
        temp_yearly_median['Date'] = pd.to_datetime(temp_yearly_median['Date'])
        temp_yearly_median = (temp_yearly_median.set_index('Date').resample('Y').median())
       
        #now that we have monthly and yearly resampled, place them in matrix
        stats3 = stats3.append({'Month': 'Annual'}, ignore_index=True)
        stats4 = stats4.append({'Month': 'Annual'}, ignore_index=True)
        
        #monthly median in dataframe
        medianMonthlyObs = medianMonthlyObs.append({'Month': 'Annual'}, ignore_index=True)
        medianMonthlyProj = medianMonthlyProj.append({'Month': 'Annual'}, ignore_index=True)
        
        rowit = temp_monthly.iterrows()  
        
        row_median = temp_monthly_median.iterrows()
        
        temp_monthly['Date'] = temp_monthly.index
        temp_monthly_median['Date'] = temp_monthly_median.index
         
        temp_monthly = temp_monthly.round({'Observed'+variable: 2, 'Model'+variable: 2})
        temp_monthly_median = temp_monthly_median.round({'Observed'+variable: 2, 'Model'+variable: 2})  
        temp_yearly = temp_yearly.round({'Observed'+variable: 2, 'Model'+variable: 2})
        temp_yearly_median = temp_yearly_median.round({'Observed'+variable: 2, 'Model'+variable: 2})
           
        
        #add monthly means
        for i, row in rowit:
            currDate = temp_monthly.at[i,'Date']
            
            currMonth = currDate.month
            
            currYear = currDate.year
            
            
            stats3.at[(currMonth),currYear] = temp_monthly.at[i,'Observed'+variable]
            stats4.at[(currMonth),currYear] = temp_monthly.at[i,'Model'+variable]
        
            
      
         #add monthly median
        for i, row in row_median:
            currDate = temp_monthly_median.at[i,'Date']
            
            currMonth = currDate.month
            
            currYear = currDate.year
            
            
            medianMonthlyObs.at[(currMonth ),currYear] = temp_monthly_median.at[i,'Observed'+variable]
            medianMonthlyProj.at[(currMonth),currYear] = temp_monthly_median.at[i,'Model'+variable]
        
            
        temp_yearly['Date'] = temp_yearly.index
        rowitYear = temp_yearly.iterrows()
        
        
        
        #add monthly means
        for i, row in rowitYear:
            currDate = temp_yearly.at[i,'Date']
            
            currMonth = currDate.month
            
            currYear = currDate.year
            
            
            stats3.at[12,currYear] = temp_yearly.at[i,'Observed'+variable]
            stats4.at[12,currYear] = temp_yearly.at[i,'Model'+variable]
        
           
        
        
        
        
        
        temp_yearly_median['Date'] = temp_yearly_median.index
        rowitYear_median = temp_yearly_median.iterrows()
         #add yearly medians
        for i, row in rowitYear_median:
            currDate = temp_yearly_median.at[i,'Date']
            
            currMonth = currDate.month
            
            currYear = currDate.year
            
            
            medianMonthlyObs.at[12,currYear] = temp_yearly_median.at[i,'Observed'+variable]
            medianMonthlyProj.at[12,currYear] = temp_yearly_median.at[i,'Model'+variable]
        
           
        
        
        
        
        
        
        
        #STANDARD DEVIATION
        
        stats5 = stats5.append({'Month': 'Annual'}, ignore_index=True)
        stats6 = stats6.append({'Month': 'Annual'}, ignore_index=True)
        
        temp_monthly_std = data_all
        temp_monthly_std['Date'] = pd.to_datetime(temp_monthly_std['Date'])
        temp_monthly_std = (temp_monthly_std.set_index('Date').resample('M').std())
        
       
        
        temp_yearly_std = data_all
        temp_yearly_std['Date'] = pd.to_datetime(temp_yearly_std['Date'])
        temp_yearly_std = (temp_yearly_std.set_index('Date').resample('Y').std())
        
        
        
         
        rowit = temp_monthly_std.iterrows()  
        
        temp_monthly_std['Date'] = temp_monthly_std.index
         
        temp_monthly_std = temp_monthly_std.round({'Observed'+variable: 2, 'Model'+variable: 2})    
        temp_yearly_std = temp_yearly_std.round({'Observed'+variable: 2, 'Model'+variable: 2})
           
        
        #add monthly means
        for i, row in rowit:
            currDate = temp_monthly_std.at[i,'Date']
            
            currMonth = currDate.month
            
            currYear = currDate.year
            
            
            stats5.at[(currMonth),currYear] = temp_monthly_std.at[i,'Observed'+variable]
            stats6.at[(currMonth),currYear] = temp_monthly_std.at[i,'Model'+variable]
        
            
      
        temp_yearly_std['Date'] = temp_yearly_std.index
        rowitYear = temp_yearly_std.iterrows()
        #add monthly means
        for i, row in rowitYear:
            currDate = temp_yearly_std.at[i,'Date']
            
            currMonth = currDate.month
            
            currYear = currDate.year
            
            
            stats5.at[12,currYear] = temp_yearly_std.at[i,'Observed'+variable]
            stats6.at[12,currYear] = temp_yearly_std.at[i,'Model'+variable]
        
           
        
        
        
        
        
        
        #add monthly means
        for i, row in rowit:
            currDate = temp_monthly_var.at[i,'Date']
            
            currMonth = currDate.month
            
            currYear = currDate.year
            
            
            stats7.at[(currMonth),currYear] = temp_monthly_var.at[i,'Observed'+variable]
        
        
        #Anual Precip
        temp_yearly_precip = data_all
        temp_yearly_precip['Date'] = pd.to_datetime(temp_yearly_precip['Date'])
        temp_yearly_precip = (temp_yearly_precip.set_index('Date').resample('Y').sum())
       
        temp_yearly_precip['Date'] = temp_yearly_precip.index
        
        #anual precip observed
        anualPrecip = pd.DataFrame()

        anualPrecip['Year'] = temp_yearly_precip['Date'].dt.year
        anualPrecip['Observed'] =  temp_yearly_precip['Observed'+variable]
        anualPrecip['Projected'] =  temp_yearly_precip['Model'+variable]
        
        anualPrecip = anualPrecip.round({'Observed': 2, 'Projected': 2})
        
        
        #box plots
        #create a df for both positive and negative
        
        #firstly pull the data
        bias=pd.read_csv(user_key['projectedvsobservedbias_mapped']+ variable+'_comparison_bias_output.csv')
        
        bias['Date'] = pd.to_datetime(bias['Date'])
        bias.reset_index(inplace=True)

        
        
        # do bias data
        bias['year'] = [dt.datetime.year for d in bias.Date]
        bias['month'] = [dt.datetime.month for d in bias.Date]
        years = bias['year'].unique()

        
        
        
        # Draw box plots
        
        #to do this we must create a new column listing month and year
        
        #this is the monthly breakdown
        temp_box = data_all
        
        
        
        temp_box['month_year'] = temp_box['Date'].dt.strftime('%Y-%m')

        boxfig1 = px.box(temp_box,x = "month_year", y = "Observed" +variable)
      
        boxfig2 = px.box(temp_box,x = "month_year", y = "Model" +variable)
          
           
        
        
        
        #this is for the year
            
        temp_box_year = data_all
        
        
        
        temp_box_year['year'] = temp_box_year['Date'].dt.strftime('%Y')

        boxfig3 = px.box(temp_box_year,x = "year", y = "Observed" +variable)
      
        boxfig4 = px.box(temp_box_year,x = "year", y = "Model" +variable)
          

            
        #print(boxfig4.hoverinfo)
        
        boxfig1.update_xaxes(
            title = "Month, Year"
        )
        boxfig1.update_yaxes(
            title = columnName + " " +   measurement
        )
        
        
        boxfig2.update_xaxes(
            title = "Month, Year"
        )
        boxfig2.update_yaxes(
            title = columnName + " " +   measurement
        )
        
        
        
        boxfig3.update_xaxes(
            title = "Year"
        )
        boxfig3.update_yaxes(
            title = columnName + " " +   measurement
        )
        
        
        
        boxfig4.update_xaxes(
            title = "Year"
        )
        boxfig4.update_yaxes(
            title = columnName + " " +   measurement
        )
        
        #print(boxfig3.hover_data())
            
            
        tempdataMonth = data_all
        tempdataMonth['Date'] = pd.to_datetime(tempdataMonth['Date'])
        tempdataMonth = (tempdataMonth.set_index('Date').resample('M').var())
        tempdataMonth['Date'] = tempdataMonth.index
        #create the data for the box figures
        
        
        #use temp_box for monthwise
        temp_monthly_box = pd.DataFrame()
        
        temp_box = data_all
        temp_box['Date'] = pd.to_datetime(temp_box['Date'])
        temp_box = (temp_box.set_index('Date'))
        temp_box['Date'] = temp_box.index
        
        date_monthly_obs = tempdataMonth['Date']
        
        
        
        
        median_monthly = temp_box["Observed" +variable].groupby(pd.Grouper(freq="M")).median()
        first_monthly = temp_box["Observed" +variable].groupby(pd.Grouper(freq="M")).quantile(0.25)
        third_monthly = temp_box["Observed" +variable].groupby(pd.Grouper(freq="M")).quantile(0.75)
        tempOBSBOX = temp_box["Observed" +variable].groupby(pd.Grouper(freq="M"))
        
        median_monthly_proj = temp_box["Model" +variable].groupby(pd.Grouper(freq="M")).median()
        first_monthly_proj = temp_box["Model" +variable].groupby(pd.Grouper(freq="M")).quantile(0.25)
        third_monthly_proj = temp_box["Model" +variable].groupby(pd.Grouper(freq="M")).quantile(0.75)
        
        
        median_yearly = temp_box["Observed" +variable].groupby(pd.Grouper(freq="Y")).median()
        first_yearly = temp_box["Observed" +variable].groupby(pd.Grouper(freq="Y")).quantile(0.25)
        third_yearly = temp_box["Observed" +variable].groupby(pd.Grouper(freq="Y")).quantile(0.75)
        
        median_yearly_proj = temp_box["Model" +variable].groupby(pd.Grouper(freq="Y")).median()
        first_yearly_proj = temp_box["Model" +variable].groupby(pd.Grouper(freq="Y")).quantile(0.25)
        third_yearly_proj = temp_box["Model" +variable].groupby(pd.Grouper(freq="Y")).quantile(0.75)
      
        
        iqr = third_monthly - first_monthly

        fence_low  = first_monthly - (1.5*iqr)
        fence_high = third_monthly + (1.5*iqr)
        
        fence_low = fence_low.to_frame()
        
        fence_high = fence_high.to_frame()
        
        #print(fence_high)
        currMonth = 0
        prevMonth = 0
        tempx = 0 #this will count the fence_low and fence_high, incrementing when month changed
            
        newDf = temp_box
        #pd.set_option("display.max_rows", None, "display.max_columns", None)
        #print(newDf)
        
        for index, row  in newDf.iterrows():
            #go over each row
            #check which month and year and based on that grab the proper fences
            #once you have them 
            currDate = newDf.at[index,'Date']
            
            #now grab the year and month of the date
            #currDate = dt.datetime.strptime(currDate,'%Y-%m-%d')
            
            #now get current month
            currMonth = currDate.month
            
            
            #if curr Month and previous month are not same then we increase tempx 
            #and make previous month into current
            if prevMonth != currMonth:
                if (prevMonth != 0):
                    tempx = tempx + 1
                
                prevMonth = currMonth
               
            
            
            currLow = fence_low.iat[tempx,0]
            currHigh = fence_high.iat[tempx,0]
            #print ("tempx : " + str(tempx) + " currHigh : " + str(currHigh) )    
            #now we remove rows from newDf based on low and high
            if (newDf.at[index,"Observed" +variable] > currHigh) or (newDf.at[index,"Observed" +variable] < currLow ):
                #drop if the value is outside the range
                #print( "current newDf var: " + str(newDf.at[index,"Observed" +variable]) +  " current high : " + str(currHigh) + " current Date:" + str(currDate))
                newDf.drop(index, inplace=True)   
            
            
            
            
            
            
            
            
            
        #df_out = temp_box.query('(@first_monthly - 1.5 * @iqr) <= ' + "Observed" +variable + ' <= (@third_monthly + 1.5 * @iqr)')
        
        
        #df_out = (temp_box["Observed" +variable] >= fence_low) & (temp_box["Observed" +variable] <= fence_high)
        #return df.loc[filter]
        
        #df_out = temp_box.loc[(temp_box["Observed" +variable].groupby(pd.Grouper(freq="M")).min() > fence_low) & (temp_box["Observed" +variable].groupby(pd.Grouper(freq="M")).min() < fence_high)]
        
         #df_out = temp_box[(np.abs(stats.zscore(temp_box[1])) < 3)]
        max_monthly = newDf["Observed" +variable].groupby(pd.Grouper(freq="M")).max()
        min_monthly = newDf["Observed" +variable].groupby(pd.Grouper(freq="M")).min()
        
        
        
        
        
        
        temp_monthly_box.insert(0,'Date',date_monthly_obs)                                
        temp_monthly_box.insert(1, 'Minimum', min_monthly)
        temp_monthly_box.insert(2, 'First Quartile', first_monthly) 
        temp_monthly_box.insert(3, 'Median', median_monthly)
        temp_monthly_box.insert(4, 'Third Quartile', third_monthly)
        temp_monthly_box.insert(5, 'Maximum', max_monthly)                                            
            
            
        temp_monthly_box['Date'] = temp_monthly_box['Date'].dt.strftime('%b, %Y')
        #projected                                            
        temp_monthly_proj = pd.DataFrame()
                                                  
        date_monthly_proj = tempdataMonth['Date']                                             
        #max_monthly_proj = temp_box["Model" +variable].groupby(pd.Grouper(freq="M")).max()
        #min_monthly_proj = temp_box["Model" +variable].groupby(pd.Grouper(freq="M")).min()
#         median_monthly_proj = temp_box["Model" +variable].groupby(pd.Grouper(freq="M")).median()
#         first_monthly_proj = temp_box["Model" +variable].groupby(pd.Grouper(freq="M")).quantile(0.25)
#         third_monthly_proj = temp_box["Model" +variable].groupby(pd.Grouper(freq="M")).quantile(0.75)
        
        iqr2 = third_monthly_proj - first_monthly_proj
        fence_low2  = first_monthly_proj - (1.5*iqr2)
        fence_high2 = third_monthly_proj + (1.5*iqr2)
        
        
        
        fence_low2 = fence_low2.to_frame()
        
        fence_high2 = fence_high2.to_frame()
        
        #print(fence_high)
        currMonth = 0
        prevMonth = 0
        tempx = 0 #this will count the fence_low and fence_high, incrementing when month changed
        currLow = 0
        currHigh = 0
        newDf2 = temp_box
        #pd.set_option("display.max_rows", None, "display.max_columns", None)
        #print(newDf)
        
        for index, row  in newDf2.iterrows():
            #go over each row
            #check which month and year and based on that grab the proper fences
            #once you have them 
            currDate = newDf2.at[index,'Date']
            
            #now grab the year and month of the date
            #currDate = dt.datetime.strptime(currDate,'%Y-%m-%d')
            
            #now get current month
            currMonth = currDate.month
            
            
            #if curr Month and previous month are not same then we increase tempx 
            #and make previous month into current
            if prevMonth != currMonth:
                if (prevMonth != 0):
                    tempx = tempx + 1
                
                prevMonth = currMonth
               
            
            
            currLow = fence_low2.iat[tempx,0]
            currHigh = fence_high2.iat[tempx,0]
            #print ("tempx : " + str(tempx) + " currHigh : " + str(currHigh) )    
            #now we remove rows from newDf based on low and high
            if (newDf2.at[index,"Model" +variable] > currHigh) or (newDf2.at[index,"Model" +variable] < currLow ):
                #drop if the value is outside the range
                #print( "current newDf var: " + str(newDf.at[index,"Observed" +variable]) +  " current high : " + str(currHigh) + " current Date:" + str(currDate))
                newDf2.drop(index, inplace=True)   
            
            
        
        pd.set_option("display.max_rows", None, "display.max_columns", None)
        #print(newDf2)
        max_monthly_proj = newDf2["Model" +variable].groupby(pd.Grouper(freq="M")).max()
        min_monthly_proj = newDf2["Model" +variable].groupby(pd.Grouper(freq="M")).min()
        
        
        
        
        
        
        temp_monthly_proj.insert(0,'Date',date_monthly_proj)                                
        temp_monthly_proj.insert(1, 'Minimum', min_monthly_proj)
        temp_monthly_proj.insert(2, 'First Quartile', first_monthly_proj)
        temp_monthly_proj.insert(3, 'Median', median_monthly_proj)
        temp_monthly_proj.insert(4, 'Third Quartile', third_monthly_proj)
        temp_monthly_proj.insert(5, 'Maximum', max_monthly_proj)                                    
       
        temp_monthly_proj['Date'] = temp_monthly_proj['Date'].dt.strftime('%b, %Y')
        
        
        tempdataYear = data_all
        tempdataYear['Date'] = pd.to_datetime(tempdataYear['Date'])
        tempdataYear = (tempdataYear.set_index('Date').resample('Y').var())
        tempdataYear['Date'] = tempdataYear.index
        
        temp_yearly_box = pd.DataFrame()
        
        #temp_yearly_box['Date'] = temp_yearly_box.index
        
        date_yearly = tempdataYear['Date']             
        #max_yearly = temp_box["Observed" +variable].groupby(pd.Grouper(freq="Y")).max()
        #min_yearly = temp_box["Observed" +variable].groupby(pd.Grouper(freq="Y")).min()
        
        iqr3 = third_yearly - first_yearly
        fence_low3  = first_yearly - (1.5*iqr3)
        fence_high3 = third_yearly + (1.5*iqr3)
        
        fence_low3 = fence_low3.to_frame()
        
        fence_high3 = fence_high3.to_frame()
        
        #print(fence_high)
        currYear = 0
        prevYear = 0
        tempx = 0 #this will count the fence_low and fence_high, incrementing when month changed
            
        newDf3 = temp_box
        #pd.set_option("display.max_rows", None, "display.max_columns", None)
        #print(newDf)
        
        for index, row  in newDf3.iterrows():
            #go over each row
            #check which month and year and based on that grab the proper fences
            #once you have them 
            currDate = newDf3.at[index,'Date']
            
            #now grab the year and month of the date
            #currDate = dt.datetime.strptime(currDate,'%Y-%m-%d')
            
            #now get current year
            currYear = currDate.year
            
            
            #if curr Month and previous month are not same then we increase tempx 
            #and make previous month into current
            if prevYear != currYear:
                if (prevYear != 0):
                    tempx = tempx + 1
                
                prevYear = currYear
               
            
            
            currLow = fence_low3.iat[tempx,0]
            currHigh = fence_high3.iat[tempx,0]
            #print ("tempx : " + str(tempx) + " currHigh : " + str(currHigh) )    
            #now we remove rows from newDf based on low and high
            if (newDf3.at[index,"Observed" +variable] > currHigh) or (newDf3.at[index,"Observed" +variable] < currLow ):
                #drop if the value is outside the range
                #print( "current newDf var: " + str(newDf.at[index,"Observed" +variable]) +  " current high : " + str(currHigh) + " current Date:" + str(currDate))
                newDf3.drop(index, inplace=True)   
            
            
        
        max_yearly = newDf3["Observed" +variable].groupby(pd.Grouper(freq="Y")).max()
        min_yearly = newDf3["Observed" +variable].groupby(pd.Grouper(freq="Y")).min()
        
        
        
        
        
        
        
        
        
        
        
        
        temp_yearly_box.insert(0,'Date',date_yearly)    
        temp_yearly_box.insert(1, 'Minimum', min_yearly)
        temp_yearly_box.insert(2, 'First Quartile', first_yearly)
        temp_yearly_box.insert(3, 'Median', median_yearly)
        temp_yearly_box.insert(4, 'Third Quartile', third_yearly)
        temp_yearly_box.insert(5, 'Maximum', max_yearly)     
        
        temp_yearly_box['Date'] = temp_yearly_box['Date'].dt.strftime('%Y')
        
        temp_yearly_proj = pd.DataFrame()
                                                  
        date_yearly_proj = tempdataYear['Date']                                                
  
         
        iqr4 = third_yearly_proj - first_yearly_proj
        fence_low4  = first_yearly_proj - (1.5*iqr4)
        fence_high4 = third_yearly_proj + (1.5*iqr4)
        
        fence_low4 = fence_low4.to_frame()
        
        fence_high4 = fence_high4.to_frame()
        
        #print(fence_high)
        currYear = 0
        prevYear = 0
        tempx = 0 #this will count the fence_low and fence_high, incrementing when month changed
            
        newDf4 = temp_box
        #pd.set_option("display.max_rows", None, "display.max_columns", None)
        #print(newDf)
        
        for index, row  in newDf4.iterrows():
            #go over each row
            #check which month and year and based on that grab the proper fences
            #once you have them 
            currDate = newDf4.at[index,'Date']
            
            #now grab the year and month of the date
            #currDate = dt.datetime.strptime(currDate,'%Y-%m-%d')
            
            #now get current month
            currMonth = currDate.year
            
            
            #if curr Month and previous month are not same then we increase tempx 
            #and make previous month into current
            if prevYear != currYear:
                if (prevYear != 0):
                    tempx = tempx + 1
                
                prevYear = currYear
               
            
            
            currLow = fence_low4.iat[tempx,0]
            currHigh = fence_high4.iat[tempx,0]
            #print ("tempx : " + str(tempx) + " currHigh : " + str(currHigh) )    
            #now we remove rows from newDf based on low and high
            if (newDf4.at[index,"Model" +variable] > currHigh) or (newDf4.at[index,"Model" +variable] < currLow ):
                #drop if the value is outside the range
                #print( "current newDf var: " + str(newDf.at[index,"Observed" +variable]) +  " current high : " + str(currHigh) + " current Date:" + str(currDate))
                newDf4.drop(index, inplace=True)   
            
            
        pd.set_option("display.max_rows", None, "display.max_columns", None)
        print(newDf4["Model" +variable].groupby(pd.Grouper(freq="Y")))
        print("AHHHHHHHHH NEW UHSAUDUH UISHAUI DH")
        
        max_yearly_proj = newDf4["Model" +variable].groupby(pd.Grouper(freq="Y")).max()
        min_yearly_proj = newDf4["Model" +variable].groupby(pd.Grouper(freq="Y")).min()
        
        
        pd.set_option("display.max_rows", None, "display.max_columns", None)
        print(min_yearly_proj)
        
        
        
        
        
        temp_yearly_proj.insert(0,'Date',date_yearly_proj)                                
        temp_yearly_proj.insert(1, 'Minimum', min_yearly_proj)
        temp_yearly_proj.insert(2, 'First Quartile', first_yearly_proj)
        temp_yearly_proj.insert(3, 'Median', median_yearly_proj)
        temp_yearly_proj.insert(4, 'Third Quartile', third_yearly_proj)
        temp_yearly_proj.insert(5, 'Maximum', max_yearly_proj)                                    
        
        temp_yearly_proj['Date'] = temp_yearly_proj['Date'].dt.strftime('%Y')
        
        
        #use temp_box_year for year wise 
            
        
        #seasonal plot here
        #have to creat a DF where each year is a column and one column is the month
        #under the month column is simply months, and under the year column is the values
        
        
        temp_yearly_proj = temp_yearly_proj.round(2)
        temp_yearly_box = temp_yearly_box.round(2)
        
        temp_monthly_proj = temp_monthly_proj.round(2)
        temp_monthly_box = temp_monthly_box.round(2)
        
        
        seasonalfig = px.line(seasonalDF, x="Month", y=seasonalDF.columns)
        
 
        seasonalfig.update_yaxes(
            title = columnName + " " +   measurement
        )
        seasonalfig.update_layout(title = "Observed "+ columnName+ " Seasonality Plots",legend_title=dict(text = "Year"))
        
        seasonalfig2 = px.line(seasonalDF2, x="Month", y=seasonalDF.columns)
        
        boxfig3.update_layout(title = 'Observed ' + columnName + ': Year-wise Box Plots')
        
        boxfig4.update_layout(title = 'Predicted ' + columnName + ': Year-wise Box Plots')
        
        boxfig1.update_layout(title = 'Observed ' + columnName + ': Month-wise Box Plots')
        
        boxfig2.update_layout(title = 'Predicted ' + columnName + ': Month-wise Box Plots')

        seasonalfig2.update_yaxes(
            title = columnName + " " +   measurement
        )
        seasonalfig2.update_layout(title = "Predicted "+ columnName+ " Seasonality Plots",legend_title=dict(text = "Year"))
        
        
        tempfig = make_subplots(specs=[[{"secondary_y": True}]])
        
      
        
        tempfig.add_trace(go.Scatter(x=data_all['Date'], y=data_all['Bias'], fill='tozeroy', name = "Bias"),secondary_y=True) # fill to trace0 y
        tempfig.add_trace(go.Scatter(x=data_all['Date'], y=data_all["Observed" +variable], name = "Observed"),secondary_y=False) # fill down to xaxis
        tempfig.update_layout(
            title_x=0.5,
            xaxis_title="Date",
            yaxis_title=columnName + ' ' + measurement,
            showlegend=True,
            yaxis_range=[-75,150],
#             margin=dict(l=5,r=5,b=0,t=5,(specs=[[{“secondary_y”: True}]])pad=5)
            )
        tempfig.update_yaxes(title = "Bias", range = [-75,150],secondary_y = True)
        tempfig.update_layout(title = 'Bias Graph')
        
        
        
        
#        pio.kaleido.scope.mathjax = None
        #print out all figs
#         fig.write_image("Images/MainGraph.png",engine='orca')
#         tempfig.write_image("Images/Biasfig.png",engine='orca')
#         boxfig1.write_image("Images/Boxfig1.png",engine='orca')
#         boxfig2.write_image("Images/Boxfig2.png",engine='orca')
#         boxfig3.write_image("Images/Boxfig3.png",engine='orca')
#         boxfig4.write_image("Images/Boxfig4.png",engine='orca')
#         seasonalfig.write_image("Images/Seasonalfig1.png",engine='orca')
#         seasonalfig2.write_image("Images/Seasonalfig2.png",engine='orca')

        print(temp_yearly_proj)
        print(boxfig4)
        if variable == 'pr':         
            percipValue ={'float' : 'left','margin' : '10px','width': '800px', 'display': 'inline-block'}
            percipValueRight ={'float' : 'right','margin' : '10px','width': '800px', 'display': 'inline-block'}
        else:
            percipValue ={'float' : 'left','margin' : '10px','width': '800px', 'display': 'none'}
            percipValueRight ={'float' : 'right','margin' : '10px','width': '800px', 'display': 'none'}
            
        if variable == 'rlds':        
            biasShow ={'float' : 'right','margin' : '10px','width': '800px', 'display': 'none'}
        else:
            biasShow ={'float' : 'right','margin' : '10px','width': '800px', 'display': 'inline-block'}
        
        #print(str(percipValue)) 
#         biasfig = go.Figure(data=go.Scatter(
#                     x=data_all['Date'],
#                     y=data_all["Observed" +variable],
#                     xhoverformat="%d %b, %Y",
#                     yhoverformat = ".2f",
#                     error_y=dict(
#                         type='data',
#                         array=data_all['Bias']
#                     )))

#         biasfig.update_yaxes(title_text="Observed Value of " + columnName, secondary_y=False)
#         biasfig.update_yaxes(title_text="Error Bar Value", secondary_y=True)

        #create the output that will go on the page
        graph = html.Div([
            html.Div(id = 'graphDIV', children =[
                html.Button("Download Data Model", id="btn_csv",style={'background-color': '#4CAF50','border': 'none','color': 'white','padding': '15px 32px','text-align': 'center','text-decoration': 'none','display': 'inline-block','font-size': '16px','margin': '4px 2px'}),
                dcc.Download(id="download-dataframe-csv"),
                (dcc.Graph(
                   id='Graph1',
                   figure=fig,
                    style={
                        'height' : '300px', 
                        'margin' : '50px'
                    }
               ))
            ],style = {'display': 'inline-block'}),
            
            
            html.Div(id = 'frequencyObs', children=[
            html.Div([
                html.Button("Download Analysis", id="btn_analysis",style={'background-color': '#4CAF50','border': 'none','color': 'white','padding': '15px 32px','text-align': 'center','text-decoration': 'none','display': 'inline-block','font-size': '16px','margin': '4px 2px'}),
                dcc.Download(id="download-analysis"),
                    ],style={'float' : 'left','margin' : '10px','margin-top': '350px','width': '100%', 'display': 'inline-block'}),
            
            html.Div([
            html.H3('Number of days where observed ' + columnName + ' is >/< than  ECCC 30 year normals', style={'width': '800px','margin' : '10px','font-size': '12px', 'float': 'left', 'font-family': 'Verdana'}),
            dash_table.DataTable(
                id='table',
                columns=[{"name": i, "id": i} for i in stats1.columns],
                data=stats1.to_dict('records'),
            )
            ],style=percipValue),
                
             html.Div([
                 html.H3('Number of days where Predicted ' + columnName + ' is >/< than  ECCC 30 year normal', style={'width': '800px','margin' : '10px','font-size': '12px', 'float': 'left', 'font-family': 'Verdana'}),
                 dash_table.DataTable(
                id='table',
                columns=[{"name": i, "id": i} for i in stats2.columns],
                data=stats2.to_dict('records'),
            )
             ],style=percipValueRight),
                
            html.Div([
                html.H3('Annual ' + columnName + '', style={'width': '800px','font-size': '12px','margin' : '10px', 'font-family': 'Verdana'}),
                dash_table.DataTable(
                id='table',
                columns=[{"name": i, "id": i} for i in anualPrecip.columns],
                data=anualPrecip.to_dict('records'),
                style_cell={
                    'minWidth': '10px', 'width': '10px', 'maxWidth': '10px'
                }
            ),
            ],style=percipValue),
                
            html.Div([],style={'float' : 'left','margin' : '10px','width': '100%', 'display': 'inline-block'}),
            html.Div([
                html.H3('Observed ' + columnName + ': Monthly Means', style={'width': '800px','margin' : '10px', 'font-size': '12px', 'float': 'left', 'font-family': 'Verdana'}),
                dash_table.DataTable(
                id='table',
                columns=[{"name": i, "id": i} for i in stats3.columns],
                data=stats3.to_dict('records')
            ),
            ],style={'float' : 'left','margin' : '10px','width': '800px', 'display': 'inline-block'}),
            html.Div([
                html.H3('Predicted ' + columnName + ': Monthly Means', style={'width': '800px','margin' : '10px','font-size': '12px', 'float': 'left', 'font-family': 'Verdana'}),
                dash_table.DataTable(
                id='table',
                columns=[{"name": i, "id": i} for i in stats4.columns],
                data=stats4.to_dict('records')
               
            ),
            ],style={'float' : 'right','margin' : '10px','width': '800px', 'display': 'inline-block'}),
             html.Div([
                html.H3('Observed ' + columnName + ': Monthly Medians', style={'width': '800px','margin' : '10px', 'font-size': '12px', 'float': 'left', 'font-family': 'Verdana'}),
                dash_table.DataTable(
                id='table',
                columns=[{"name": i, "id": i} for i in medianMonthlyObs.columns],
                data=medianMonthlyObs.to_dict('records')
            ),
            ],style={'float' : 'left','margin' : '10px','width': '800px', 'display': 'inline-block'}),
            html.Div([
                html.H3('Predicted ' + columnName + ': Monthly Medians', style={'width': '800px','margin' : '10px', 'font-size': '12px', 'float': 'left', 'font-family': 'Verdana'}),
                dash_table.DataTable(
                id='table',
                columns=[{"name": i, "id": i} for i in medianMonthlyProj.columns],
                data=medianMonthlyProj.to_dict('records')
            ),
            ],style={'float' : 'right','margin' : '10px','width': '800px', 'display': 'inline-block'}),
            html.Div([
                
                html.H3('Observed ' + columnName + ': Monthly Standard Deviation', style={'width': '800px','margin' : '10px','font-size': '12px', 'float': 'left', 'font-family': 'Verdana'}),
                dash_table.DataTable(
                id='table',
                columns=[{"name": i, "id": i} for i in stats5.columns],
                data=stats5.to_dict('records')
            ),
            ],style={'float' : 'left','margin' : '10px','width': '800px', 'display': 'inline-block'}),
                
            html.Div([
                html.H3('Predicted ' + columnName + ': Monthly Standard Deviation', style={'width': '800px','margin' : '10px','font-size': '12px', 'float': 'left', 'font-family': 'Verdana'}),
                dash_table.DataTable(
                id='table',
                columns=[{"name": i, "id": i} for i in stats6.columns],
                data=stats6.to_dict('records')
            )
                
            ],style={'float' : 'right','margin' : '10px','width': '800px', 'display': 'inline-block'}),
                
            
              
            html.Div([],style={'float' : 'left','margin' : '10px','width': '100%', 'display': 'inline-block'}),
             
            html.Div([
               
                #html.H3('Bias Graph                                        ', style={'width': 'auto','margin' : '10px','font-size': '12px', 'float': 'left', 'font-family': 'Verdana'}),
                (dcc.Graph(
                   id='Graph1',
                   figure=tempfig
                   ))
                
            ],style={'float' : 'left','margin' : '10px','width': '800px', 'display': 'inline-block'}),
                   
              html.Div([
                html.H3('Bias between Observed and Projected ' + columnName + '', style={ 'width': '800px','margin' : '10px','font-size': '12px', 'float': 'left', 'font-family': 'Verdana'}),
                dash_table.DataTable(
                id='table',
                columns=[{"name": i, "id": i} for i in biasDF.columns],
                data=biasDF.to_dict('records'))
        
                
            ],style=biasShow),
                
               html.Div([],style={'float' : 'left','margin' : '10px','width': '100%', 'display': 'inline-block'}),
               
               html.Div([
         #       html.H3('Observed ' + columnName + ': Month-wise Box Plots', style={'width': '800px','margin' : '10px','font-size': '12px', 'float': 'left', 'font-family': 'Verdana'}),
                (dcc.Graph(
               id='Graph1',
               figure=boxfig1
                )),
                
            ],style={'float' : 'left','margin' : '10px','width': '800px', 'display': 'inline-block'}),
                   
            html.Div([
                  
       #    html.H3('Projected ' + columnName + ': Month-wise Box Plots', style={ 'width': '800px','margin' : '10px','font-size': '12px', 'float': 'left', 'font-family': 'Verdana'}),        
            (dcc.Graph(
               id='Graph1',
               figure=boxfig2
           )),
                
            ],style={'float' : 'right','margin' : '10px','width': '800px', 'display': 'inline-block'}),
                   

            html.Div([
                dash_table.DataTable(
                id='table',
                columns=[{"name": i, "id": i} for i in temp_monthly_box.columns],
                data=temp_monthly_box.to_dict('records')
            ), 
                
            ],style={'float' : 'left','margin' : '10px','width': '800px', 'display': 'inline-block'}),
                   
            html.Div([
                 dash_table.DataTable(
                id='table',
                columns=[{"name": i, "id": i} for i in temp_monthly_proj.columns],
                data=temp_monthly_proj.to_dict('records')
            ),  
            ],style={'float' : 'right','margin' : '10px','width': '800px', 'display': 'inline-block'}),
                   

            html.Div([
#               html.H3('Observed ' + columnName + ': Year-wise Box Plots', style={'width': '800px','margin' : '10px','font-size': '12px', 'float': 'left', 'font-family': 'Verdana'}),
                (dcc.Graph(
                   id='Graph1',
                   figure=boxfig3
               )),
                
            ],style={'float' : 'left','width': '800px', 'display': 'inline-block'}),
                   
              html.Div([
            #html.H3('Projected ' + columnName + ': Year-wise Box Plots', style={'font-size': '12px', 'float': 'right', 'font-family': 'Verdana'}),
         

            (dcc.Graph(
               id='Graph1',
               figure=boxfig4
           )),
                
            ],style={'float' : 'right','width': '800px', 'display': 'inline-block'}),
                   
                
            html.Div([
               dash_table.DataTable(
                id='table',
                columns=[{"name": i, "id": i} for i in temp_yearly_box.columns],
                data=temp_yearly_box.to_dict('records')
            ),
                
            ],style={'float' : 'left','margin' : '10px','width': '800px', 'display': 'inline-block'}),
                   
              html.Div([
                  
            dash_table.DataTable(
                id='table',
                columns=[{"name": i, "id": i} for i in temp_yearly_proj.columns],
                data=temp_yearly_proj.to_dict('records')
            ),
                
            ],style={'float' : 'right','margin' : '10px','width': '800px', 'display': 'inline-block'}),
                   
                
            html.Div([
#           html.H3('Observed and Projected Precipitation Seasonality Plots', style={'font-size': '12px', 'font-family': 'Verdana'}),
                 (dcc.Graph(
               id='Graph1',
               figure=seasonalfig
           )),
                
            ],style={'float' : 'left','width': '800px', 'display': 'inline-block'}),
                   
              html.Div([
                (dcc.Graph(
                   id='Graph1',
                   figure=seasonalfig2,

               ))
                
            ],style={'float' : 'right','width': '800px', 'display': 'inline-block'}),
                   
        

                
            ],style = {'display':'inline-block','width' : '2000px'})
           
             
              
        ])

        return 'Analyze',graph,data_all.to_json(date_format='iso', orient='split'),stats1.to_json(date_format='iso', orient='split'),stats2.to_json(date_format='iso', orient='split'),anualPrecip.to_json(date_format='iso', orient='split'),stats3.to_json(date_format='iso', orient='split'),stats4.to_json(date_format='iso', orient='split'),stats5.to_json(date_format='iso', orient='split'),stats6.to_json(date_format='iso', orient='split'),stats7.to_json(date_format='iso', orient='split'),stats8.to_json(date_format='iso', orient='split'),biasDF.to_json(date_format='iso', orient='split'),temp_monthly_box.to_json(date_format='iso', orient='split'),temp_monthly_proj.to_json(date_format='iso', orient='split'),temp_yearly_box.to_json(date_format='iso', orient='split'),temp_yearly_proj.to_json(date_format='iso', orient='split'),fig
    


@app.callback(
    Output("download-dataframe-csv", "data"),
    inputs = [Input("btn_csv", "n_clicks"), Input('main_data','data')],
    prevent_initial_call=True,
)
def func(n_clicks,data_all ):
    
    if n_clicks:   
        df = pd.read_json(data_all, orient='split')
        return dcc.send_data_frame(df.to_csv, "mydf.csv")

    
    
@app.callback(
    Output("download-analysis", "data"),
    inputs = [Input("btn_analysis", "n_clicks"), Input('observed_normals','data'),
              Input('projected_normals','data'),Input('annual_data','data'),Input('observed_mean','data'),
              Input('projected_mean','data'),Input('observed_deviation','data'),Input('projected_deviation','data'),
             Input('observed_variance','data'),Input('projected_variance','data'),Input('bias_data','data'),
             Input('observed_monthBox','data'),Input('projected_monthBox','data'),Input('observed_yearBox','data'),
             Input('projected_yearBox','data'),Input('mainFig','data')],
    prevent_initial_call=True,
)
def func(n_clicks,observedNormal,projectedNormal,annualData,observedMean,projectedMean,observedDeviation,projectedDeviation,observedVairance,projectedVariance,biasData,observedMonthBox,projectedMonthBox,observedYearBox,projectedYearBox,fig):
    
    if n_clicks: 

        df1 = pd.read_json(observedNormal, orient='split')
        df2 = pd.read_json(projectedNormal, orient='split')
        df3 = pd.read_json(annualData, orient='split')
        df4 = pd.read_json(observedMean, orient='split')
        df5 = pd.read_json(projectedMean, orient='split')
        df6 = pd.read_json(observedDeviation, orient='split')
        df7 = pd.read_json(projectedDeviation, orient='split')
        df8 = pd.read_json(observedVairance, orient='split')
        df9 = pd.read_json(projectedVariance, orient='split')
        df10 = pd.read_json(biasData, orient='split')
        df11 = pd.read_json(observedMonthBox, orient='split')
        df12 = pd.read_json(projectedMonthBox, orient='split')
        df13 = pd.read_json(observedYearBox, orient='split')
        df14 = pd.read_json(projectedYearBox, orient='split')


      
    
        df3.reset_index(drop=True, inplace=True)
        df11.reset_index(drop=True, inplace=True)
        df12.reset_index(drop=True, inplace=True)
        df13.reset_index(drop=True, inplace=True)
        df14.reset_index(drop=True, inplace=True)
        
        
    
        
        with pd.ExcelWriter('DataAnalysis.xlsx') as writer:
            
            workbook = writer.book
            writer.sheets={'Project vs Observed Graph':workbook.add_worksheet()}
            worksheet1 = writer.sheets['Project vs Observed Graph']
            worksheet1.insert_image('D3', 'Images/MainGraph.png')
            
            
            df1.to_excel(writer, sheet_name='Observed Normal',index=False)
            df2.to_excel(writer, sheet_name='Projected Normal',index=False)
            df3.to_excel(writer, sheet_name='Annual Data',index=False)
            df4.to_excel(writer, sheet_name='Observed Mean',index=False)
            df5.to_excel(writer, sheet_name='Projected Mean',index=False)            
            df6.to_excel(writer, sheet_name='Observed Deviation',index=False)
            df7.to_excel(writer, sheet_name='Projected Deviation',index=False)
            df8.to_excel(writer, sheet_name='Observed Variance',index=False)
            df9.to_excel(writer, sheet_name='Projected Variance',index=False)
            df10.to_excel(writer, sheet_name='Bias Data',index=False)
            df11.to_excel(writer, sheet_name='Observed Monthly Box Data',index=False)
            df12.to_excel(writer, sheet_name='Projected Monthly Box Data',index=False)
            df13.to_excel(writer, sheet_name='Observed Yearly Box Data',index=False)
            df14.to_excel(writer, sheet_name='Projected Yearly Box Data',index=False)
            
            
            writer.save()
        
        return dcc.send_file(writer)
            



        
        
        
        
        
#THIS IS TO DOWNLOAD THE AUTOMATED DATA to CSV !!!!   


@app.callback(
    Output("download-dataframe-csv-auto", "data"),
    inputs = [Input("btn_csv_auto", "n_clicks"), Input('main_data_auto','data')],
    prevent_initial_call=True,
)
def func(n_clicks,data_all ):
    
    if n_clicks:   
        df = pd.read_json(data_all, orient='split')
        return dcc.send_data_frame(df.to_csv, "mydf.csv")

@app.callback(
    Output("download-analysis-auto", "data"),
    inputs = [Input("btn_analysis_auto", "n_clicks"), Input('observed_normals_auto','data'),
              Input('projected_normals_auto','data'),Input('annual_data_auto','data'),Input('observed_mean_auto','data'),
              Input('projected_mean_auto','data'),Input('observed_deviation_auto','data'),Input('projected_deviation_auto','data'),
             Input('observed_variance_auto','data'),Input('projected_variance_auto','data'),Input('bias_data_auto','data'),
             Input('observed_monthBox_auto','data'),Input('projected_monthBox_auto','data'),Input('observed_yearBox_auto','data'),
             Input('projected_yearBox_auto','data'),Input('mainFig_auto','data')],
    prevent_initial_call=True,
)
def func(n_clicks,observedNormal,projectedNormal,annualData,observedMean,projectedMean,observedDeviation,projectedDeviation,observedVairance,projectedVariance,biasData,observedMonthBox,projectedMonthBox,observedYearBox,projectedYearBox,fig):
    
    if n_clicks: 

        df1 = pd.read_json(observedNormal, orient='split')
        df2 = pd.read_json(projectedNormal, orient='split')
        df3 = pd.read_json(annualData, orient='split')
        df4 = pd.read_json(observedMean, orient='split')
        df5 = pd.read_json(projectedMean, orient='split')
        df6 = pd.read_json(observedDeviation, orient='split')
        df7 = pd.read_json(projectedDeviation, orient='split')
        df8 = pd.read_json(observedVairance, orient='split')
        df9 = pd.read_json(projectedVariance, orient='split')
        df10 = pd.read_json(biasData, orient='split')
        df11 = pd.read_json(observedMonthBox, orient='split')
        df12 = pd.read_json(projectedMonthBox, orient='split')
        df13 = pd.read_json(observedYearBox, orient='split')
        df14 = pd.read_json(projectedYearBox, orient='split')


      
    
        df3.reset_index(drop=True, inplace=True)
        df11.reset_index(drop=True, inplace=True)
        df12.reset_index(drop=True, inplace=True)
        df13.reset_index(drop=True, inplace=True)
        df14.reset_index(drop=True, inplace=True)
        
        
    
        
        with pd.ExcelWriter('DataAnalysis.xlsx') as writer:
            
            workbook = writer.book
            writer.sheets={'Project vs Observed Graph':workbook.add_worksheet()}
            worksheet1 = writer.sheets['Project vs Observed Graph']
            worksheet1.insert_image('D3', 'Images/MainGraph.png')
            
            
            df1.to_excel(writer, sheet_name='Observed Normal',index=False)
            df2.to_excel(writer, sheet_name='Projected Normal',index=False)
            df3.to_excel(writer, sheet_name='Annual Data',index=False)
            df4.to_excel(writer, sheet_name='Observed Mean',index=False)
            df5.to_excel(writer, sheet_name='Projected Mean',index=False)            
            df6.to_excel(writer, sheet_name='Observed Deviation',index=False)
            df7.to_excel(writer, sheet_name='Projected Deviation',index=False)
            df8.to_excel(writer, sheet_name='Observed Variance',index=False)
            df9.to_excel(writer, sheet_name='Projected Variance',index=False)
            df10.to_excel(writer, sheet_name='Bias Data',index=False)
            df11.to_excel(writer, sheet_name='Observed Monthly Box Data',index=False)
            df12.to_excel(writer, sheet_name='Projected Monthly Box Data',index=False)
            df13.to_excel(writer, sheet_name='Observed Yearly Box Data',index=False)
            df14.to_excel(writer, sheet_name='Projected Yearly Box Data',index=False)
            
            
            writer.save()
        
        return dcc.send_file(writer)
            

    
@app.callback(
    [Output("date-picker-range", "start_date"), Output("date-picker-range", "end_date")],
    [Input("date_slider", "value")],
    [State("date-picker-range", "start_date"), State("date-picker-range", "end_date")],
)
def update_date_range(slider_dates, date_range_start, date_range_end):
    start_yr, end_yr = slider_dates[0], slider_dates[1]    

    if date_range_start is not None:
        date_range_start = str(start_yr) + date_range_start[4:]
    else:
        date_range_start = str(start_yr) + '-01-01'

    if date_range_end is not None:
        date_range_end = str(end_yr) + date_range_end[4:]
    else:
        date_range_end = str(end_yr) + '-01-01'

    return date_range_start, date_range_end


@app.callback(
    Output("displayDate", "children"),
    [Input("date-picker-range", "start_date"), Input("date-picker-range", "end_date")],
)
def update_date_range(date_range_start, date_range_end):
    return f"You have selected dates from {date_range_start} to {date_range_end}"



@app.callback(
    [Output("date-picker-range-auto", "start_date"), Output("date-picker-range-auto", "end_date")],
    [Input("date_slider-auto", "value")],
    [State("date-picker-range-auto", "start_date"), State("date-picker-range-auto", "end_date")],
)
def update_date_range(slider_dates, date_range_start, date_range_end):
    start_yr, end_yr = slider_dates[0], slider_dates[1]    

    if date_range_start is not None:
        date_range_start = str(start_yr) + date_range_start[4:]
    else:
        date_range_start = str(start_yr) + '-01-01'

    if date_range_end is not None:
        date_range_end = str(end_yr) + date_range_end[4:]
    else:
        date_range_end = str(end_yr) + '-01-01'

    return date_range_start, date_range_end


@app.callback(
    Output("displayDate-auto", "children"),
    [Input("date-picker-range-auto", "start_date"), Input("date-picker-range-auto", "end_date")],
)
def update_date_range(date_range_start, date_range_end):
    return f"You have selected dates from {date_range_start} to {date_range_end}"




# @app.callback(
#     dash.dependencies.Output('frequencyObs', 'style'),
#     [dash.dependencies.Input('frequencyBtn', 'n_clicks')],
#     )
# def button_toggle(n_clicks):
#     if n_clicks % 2 == 1:
#         return {'display': 'none'}
#     else:
#         return {'display': 'block'}
    

    

        
if __name__ == '__main__':
    app.run_server()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




