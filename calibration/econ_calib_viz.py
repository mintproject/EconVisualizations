#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 11 07:26:28 2019

@author: deborahkhider

Econ model calib output
"""

import pandas as pd
#from bokeh.io import show
from bokeh.models.widgets import Div, Dropdown
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import DataTable, TableColumn
from bokeh.layouts import widgetbox, gridplot
from bokeh.plotting import curdoc


def update(attr,old,new):
    if dd_crop.value == 'maize':
        dffilt = data[data['crop']=='maize']
    elif dd_crop.value == 'cassava':
        dffilt = data[data['crop']=='cassava']
    elif dd_crop.value == 'groundnuts':
        dffilt = data[data['crop']=='groundnuts']
    elif dd_crop.value == 'sesame':
        dffilt = data[data['crop']=='sesame']
    elif dd_crop.value == 'sorghum':
        dffilt = data[data['crop']=='sorghum']
    else:
        print("Dropdown value is incorrect")
    
    # update the source:
    source.data['land']=[dffilt[headers[5]],dffilt[headers[6]],dffilt[headers[5]]-dffilt[headers[6]]]
    source.data['Nuse']=[dffilt[headers[7]],dffilt[headers[8]],dffilt[headers[7]]-dffilt[headers[8]]]
    source.data['prod']=[dffilt[headers[9]],dffilt[headers[10]],dffilt[headers[9]]-dffilt[headers[10]]]
    
    #update div
    if (dffilt['cc1']>0).any():
        cc1_crop = 'Myopic elasticity calibration criteria met'
    else:
        cc1_crop = 'Myopic elasticity calibration criteria not met'
    
    if (dffilt['cc2']<0).any():
        cc2_crop = 'No dominant response criteria met'
    else:
        cc2_crop = 'No dominant response criteria not met'
    
    div2.text = '<p>'+dd_crop.value.capitalize()+'</p><p>'+ cc1_crop+'</p><p>'+ cc2_crop+'</p><p>'

#Get the calib data 
global data
data = pd.read_csv('MINT_v6_calibration_output.txt')

# put a disclaimer at the top if everything worked as planned 
if (data['cc1']<0).any():
    cc1_str = 'Myopic elasticity calibration criteria not met'
else:
    cc1_str = 'Myopic elasticity calibration criteria met'

if (data['cc2']>0).any():
    cc2_str = 'No dominant response criteria not met'
else:
    cc2_str = 'No dominant response criteria met'

#Take the difference for each crop
headers = list(data)
land = data[headers[5]]-data[headers[6]]
Nuse = data[headers[7]]-data[headers[8]]
prod = data[headers[9]]-data[headers[10]]

#Write the rest of the strings out
if land.any()>20:
    land_str = 'Check discrepancy between simulated and observed land area'
else:
    land_str = 'Discrepancy between simulated land and observed land area within tolerance'
    
if Nuse.any()>20:
    Nuse_str = 'Check discrepancy between simulated and observed N use'
else:
    Nuse_str = 'Discrepancy between simulated and observed N use within tolerance'

if prod.any()>20:
    prod_str = 'Check discrepancy between simulated and observed production'
else:
    prod_str = 'Discrepancy between simulated and observed production within tolerance'

# first widget
div1 = Div(text='<p>'+cc1_str+'</p><p>'+
           cc2_str+'</p><p>'+
           land_str+'</p><p>'+
           Nuse_str+'</p><p>'+
           prod_str+'</p><p>', width=600)

# Now work on the table 
#Step 1: filter by crop
dffilt = data[data['crop']=='maize']
source = ColumnDataSource({'criteria':['Simulated','Observed','Difference'],
        'land':[dffilt[headers[5]],dffilt[headers[6]],dffilt[headers[5]]-dffilt[headers[6]]],
        'Nuse':[dffilt[headers[7]],dffilt[headers[8]],dffilt[headers[7]]-dffilt[headers[8]]],
        'prod':[dffilt[headers[9]],dffilt[headers[10]],dffilt[headers[9]]-dffilt[headers[10]]]})
#Step 2: Make the columns
columns = [
        TableColumn(field="criteria", title=""),
        TableColumn(field="land", title="Land Area (ha)"),
        TableColumn(field="Nuse", title="N use (kg)"),
        TableColumn(field="prod", title="Production (kg)"), 
    ]

data_table = DataTable(source=source,columns=columns, width=500)

#Button to change crop
menu_crop = [("Sorghum", "sorghum"), ("Maize", "maize"),
             ("Cassava", "cassava"), ("Groundnuts", "groundnuts"),
             ("Sesame", "sesame")]
dd_crop = Dropdown(label="Crop", button_type="primary", menu=menu_crop,
                   value = 'maize')
dd_crop.on_change('value', update)

#Make another div for crop cc1/cc2 criteria
if (dffilt['cc1']>0).any():
    cc1_crop = 'Myopic elasticity calibration criteria met'
else:
    cc1_crop = 'Myopic elasticity calibration criteria not met'
    
if (dffilt['cc2']<0).any():
    cc2_crop = 'No dominant response criteria met'
else:
    cc2_crop = 'No dominant response criteria not met'
    
div2= Div(text='<p> Maize </p><p>'+
           cc1_crop+'</p><p>'+
           cc2_crop+'</p><p>')
div2.on_change('text',update)

wb1 = widgetbox(dd_crop,
               div2)

#put everything in a hopefully nice layout
layout = gridplot([
        [div1],
        [data_table,wb1]
        ])
curdoc().add_root(layout)
