#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 12:21:20 2019

@author: deborahkhider
"""

import pandas as pd

from bokeh.layouts import row, column, widgetbox, gridplot
from bokeh.models import Slider, LabelSet, Legend
from bokeh.plotting import figure, output_file, show, ColumnDataSource, curdoc
from bokeh.palettes import Spectral6
from bokeh.transform import factor_cmap 
from bokeh.models.glyphs import VBar, Wedge
from math import pi
from bokeh.transform import cumsum
from bokeh.models.widgets import Div, Paragraph
import subprocess
import os
import csv

import configparser

config = configparser.ConfigParser()
config.read('config.ini')

code_path = config['economic_live']['code_path']
gams_path = config['economic_live']['gams_path']
simulation_output_file =config['economic_live']['simulation_output_file']
mint_v6_file = config['economic_live']['mint_v6_file']
price_v6_file = config['economic_live']['price_v6']
productioncost_v6_file = config['economic_live']['productioncost_v6']
simprice_file = config['economic_live']['simprice_file']
simproductioncost_file = config['economic_live']['simproductioncost_file']


def update_data(attr, old, new):
    #Get the data
    data = source.data
    data1 = source1.data
    data2 = source2.data
    data3 = source3.data
    data4 = source4.data
    
    # Sliders
    cassava_c1_dynamic = cassava_c1_slider.value
    cassava_c2_dynamic = cassava_c2_slider.value
    cassava_p_dynamic = cassava_p_slider.value
    
    groundnuts_c1_dynamic = groundnuts_c1_slider.value
    groundnuts_c2_dynamic = groundnuts_c2_slider.value
    groundnuts_p_dynamic = groundnuts_p_slider.value
    
    maize_c1_dynamic = maize_c1_slider.value
    maize_c2_dynamic = maize_c2_slider.value
    maize_p_dynamic = maize_p_slider.value
    
    sesame_c1_dynamic = sesame_c1_slider.value
    sesame_c2_dynamic = sesame_c2_slider.value
    sesame_p_dynamic = sesame_p_slider.value
    
    sorghum_c1_dynamic = sorghum_c1_slider.value
    sorghum_c2_dynamic = sorghum_c2_slider.value
    sorghum_p_dynamic = sorghum_p_slider.value
    
    # organize in a dataframe for iteration
    slider_values = pd.DataFrame({'crop':x,
                                  'c1_adj':[cassava_c1_dynamic,groundnuts_c1_dynamic,maize_c1_dynamic,sesame_c1_dynamic,sorghum_c1_dynamic],
                                  'c2_adj':[cassava_c2_dynamic,groundnuts_c2_dynamic,maize_c2_dynamic,sesame_c2_dynamic,sorghum_c2_dynamic],
                                  'p_adj':[cassava_p_dynamic,groundnuts_p_dynamic,maize_p_dynamic,sesame_p_dynamic,sorghum_p_dynamic]
                                })
    
    #Run the econ model
    # Prepare the sim files
    csv_file = simproductioncost_file
    with open(csv_file,'w',newline='') as csvfile:
        yieldwriter = csv.writer(csvfile, delimiter=',')
        yieldwriter.writerow(['','c1','c2'])
        for idx, item in enumerate(x):
            yieldwriter.writerow([item,\
                c1_read[idx]*(1+float(slider_values[slider_values['crop']==item]['c1_adj'])/100),\
                c2_read[idx]*(1+float(slider_values[slider_values['crop']==item]['c2_adj'])/100)])
    csv_file2 = simprice_file
    with open(csv_file2,'w',newline='') as csvfile2:
        pricewriter = csv.writer(csvfile2, delimiter=',')
        pricewriter.writerow(['','p'])
        for idx, item in enumerate(x):
            pricewriter.writerow([item,\
                p_read[idx]*(1+float(slider_values[slider_values['crop']==item]['p_adj'])/100)])

    #Run the econ model
    subprocess.run([gams_path,mint_v6_file])
    
    #Get the results
    econ_data = pd.read_csv(simulation_output_file,index_col=False)  
    # Update the data
    data['y'] = econ_data['yield (kg/ha)']
    data1['y'] = econ_data['Nfert (kg/ha)']
    data2['y'] = econ_data['production (kg)']
    data3['y']= econ_data['Nuse (kg)']
    data4['y'] = econ_data['land area (ha)']/econ_data['land area (ha)'].sum() * 2*pi
    #pie_data.loc['value']= econ_data_f['land area (ha)']
    #pie_data['angle']= pie_data['value']/pie_data['value'].sum() * 2*pi
    print(data1, data2, data3, data4)

# Get the base data from calibration
default = pd.read_csv(productioncost_v6_file)   
default_p = pd.read_csv(price_v6_file)

#Read in global variables
global c1_read
c1_read = list(default['c1']) #Land cost for each crop
global c2_read
c2_read = list(default['c2']) #Fertilizer cost for each crop
global p_read
p_read = list(default_p['p'])
global x
x = list(default["Unnamed: 0"])
plot_size = 300

## Run the base
# Prepare the sim files
csv_file = simproductioncost_file
with open(csv_file,'w',newline='') as csvfile:
    yieldwriter = csv.writer(csvfile, delimiter=',')
    yieldwriter.writerow(['','c1','c2'])
    for idx, item in enumerate(x):
        yieldwriter.writerow([item,\
                c1_read[idx],\
                c2_read[idx]])
csv_file2 = simprice_file
with open(csv_file2,'w',newline='') as csvfile2:
    pricewriter = csv.writer(csvfile2, delimiter=',')
    pricewriter.writerow(['','p'])
    for idx, item in enumerate(x):
        pricewriter.writerow([item,\
                p_read[idx]])

#Run the econ model
#Run the econ model
wd = os.getcwd()
os.chdir(code_path)
subprocess.run([gams_path,mint_v6_file])
os.chdir(wd)

# Source data for the bar charts 
base = pd.read_csv(simulation_output_file,index_col=False)       
source = ColumnDataSource(data=dict(x=x, y=list(base['yield (kg/ha)'])))
source1 = ColumnDataSource(data=dict(x=x, y=list(base['Nfert (kg/ha)'])))
source2 = ColumnDataSource(data=dict(x=x, y=list(base['production (kg)'])))
source3 = ColumnDataSource(data=dict(x=x, y=list(base['Nuse (kg)'])))


y4 = {'cassava': int(base[(base["crop"]=='cassava')]['land area (ha)']),
    'groundnuts': int(base[(base["crop"]=='groundnuts')]['land area (ha)']), 
    'maize': int(base[(base["crop"]=='maize')]['land area (ha)']), 
    'sesame': int(base[(base["crop"]=='sesame')]['land area (ha)']),
    'sorghum': int(base[(base["crop"]=='sorghum')]['land area (ha)'])}
pie_data = pd.Series(y4).reset_index(name='value').rename(columns={'index':'crop'})
pie_data['angle'] = pie_data['value']/pie_data['value'].sum() * 2*pi
pie_data['color'] = Spectral6[0:5]
source4 = ColumnDataSource(data=dict(x=x, y=list(pie_data['angle']),v=list(pie_data['value'])))

# Make the histogram and pie
#yield
plot = figure(x_range =source.data['x'], y_range=(0, 20000),
              plot_width=plot_size, plot_height=plot_size,
              title = 'Yield (kg/ha)', toolbar_location=None,
              tools="hover",tooltips="@x: @y") 
                        
glyph = VBar(x="x", top="y", width=0.9,
          fill_color=factor_cmap('x', palette=Spectral6, factors=x))
plot.xaxis.major_label_orientation = pi/4
plot.add_glyph(source, glyph)

#Nitrogen fertilizer rate
plot1 = figure(x_range =source1.data['x'], y_range=(0, 1000),
               plot_width=plot_size, plot_height=plot_size,
              title = 'Nitrogen fertilizer use (kg/ha)', toolbar_location=None,
              tools="hover",tooltips="@x: @y")

glyph1 = VBar(x="x", top="y", width=0.9,
          fill_color=factor_cmap('x', palette=Spectral6, factors=x))
plot1.xaxis.major_label_orientation = pi/4
plot1.add_glyph(source1, glyph1)

#Production
plot2 = figure(x_range =source2.data['x'], y_range=(0, 1000000000),
               plot_width=plot_size, plot_height=plot_size,
              title = 'Production (kg)', toolbar_location=None,
              tools="hover",tooltips="@x: @y")
glyph2 = VBar(x="x", top="y", width=0.9,
          fill_color=factor_cmap('x', palette=Spectral6, factors=x))
plot2.xaxis.major_label_orientation = pi/4
plot2.add_glyph(source2, glyph2)

# Total nitrogen use
plot3 = figure(x_range =source3.data['x'], y_range=(0, 100000000),
               plot_width=plot_size, plot_height=plot_size,
               title = 'Total Nitrogen Fertilizer Use (kg)', toolbar_location=None,
               tools="hover",tooltips="@x: @y")

glyph3 = VBar(x="x", top="y", width=0.9,
          fill_color=factor_cmap('x', palette=Spectral6, factors=x))
plot3.xaxis.major_label_orientation = pi/4
plot3.add_glyph(source3, glyph3)


#land
plot4  = figure(plot_height = plot_size, plot_width = 2*plot_size,
                #x_range = (-0.6,0.6),
                #y_range =(0.5,1.5),
                title='Land Area (ha)', toolbar_location=None,
                tools="hover",tooltips="@x: @v")

plot4.wedge(x=0, y=1, radius=0.4,
        start_angle=cumsum('y', include_zero=True), 
        end_angle=cumsum('y'),
        line_color="white", fill_color=factor_cmap('x', palette=Spectral6, factors=x), 
        legend='x', source=source4) 
plot4.axis.visible = False
plot4.xgrid.visible = False
plot4.ygrid.visible = False


# Prepare the sliders
# Cassava
cassava_c1_slider = Slider(start=-50, end=40, value=0,
                           step=10, title="Land Cost Adjustment")
cassava_c2_slider = Slider(start=-50, end=40, value=0, step=10,
                   title="Nitrogen Fertilizer Cost Adjustment")
cassava_p_slider = Slider(start=-50, end=40, value=0, step=10,
                  title="Crop Price Adjustment")

# Groundnuts
groundnuts_c1_slider = Slider(start=-50, end=40, value=0,
                           step=10, title="Land Cost Adjustment")
groundnuts_c2_slider = Slider(start=-50, end=40, value=0, step=10,
                   title="Nitrogen Fertilizer Cost Adjustment")
groundnuts_p_slider = Slider(start=-50, end=40, value=0, step=10,
                  title="Crop Price Adjustment")

# Maize
maize_c1_slider = Slider(start=-50, end=40, value=0,
                           step=10, title="Land Cost Adjustment")
maize_c2_slider = Slider(start=-50, end=40, value=0, step=10,
                   title="Nitrogen Fertilizer Cost Adjustment")
maize_p_slider = Slider(start=-50, end=40, value=0, step=10,
                  title="Crop Price Adjustment")

# Sesame
sesame_c1_slider = Slider(start=-50, end=40, value=0,
                           step=10, title="Land Cost Adjustment")
sesame_c2_slider = Slider(start=-50, end=40, value=0, step=10,
                   title="Nitrogen Fertilizer Cost Adjustment")
sesame_p_slider = Slider(start=-50, end=40, value=0, step=10,
                  title="Crop Price Adjustment")

# Sorghum
sorghum_c1_slider = Slider(start=-50, end=40, value=0,
                           step=10, title="Land Cost Adjustment")
sorghum_c2_slider = Slider(start=-50, end=40, value=0, step=10,
                   title="Nitrogen Fertilizer Cost Adjustment")
sorghum_p_slider = Slider(start=-50, end=40, value=0, step=10,
                  title="Crop Price Adjustment")

# Get the values from the sliders
cassava_c1_slider.on_change('value', update_data)
cassava_c2_slider.on_change('value', update_data)
cassava_p_slider.on_change('value', update_data)

groundnuts_c1_slider.on_change('value', update_data)
groundnuts_c2_slider.on_change('value', update_data)
groundnuts_p_slider.on_change('value', update_data)

maize_c1_slider.on_change('value', update_data)
maize_c2_slider.on_change('value', update_data)
maize_p_slider.on_change('value', update_data)

sesame_c1_slider.on_change('value', update_data)
sesame_c2_slider.on_change('value', update_data)
sesame_p_slider.on_change('value', update_data)

sorghum_c1_slider.on_change('value', update_data)
sorghum_c2_slider.on_change('value', update_data)
sorghum_p_slider.on_change('value', update_data)

# Text for the widgetbox
p1 = Div(text="<b>Cassava:</b>")
p2 = Div(text="<b>Groundnuts:</b>")
p3 = Div(text="<b>Maize:</b>")
p4 = Div(text="<b>Sesame:</b>")
p5 = Div(text="<b>Sorghum:</b>")

#Text for the instruction box
p0 = Div(text="Change one parameter at a time for sensitivity analysis")

wb1 = widgetbox(p0,p1,cassava_c1_slider, 
               cassava_c2_slider, 
               cassava_p_slider) 
wb2 = widgetbox(p2,
               groundnuts_c1_slider, 
               groundnuts_c2_slider, 
               groundnuts_p_slider)
wb3 = widgetbox(p3,
               maize_c1_slider, 
               maize_c2_slider, 
               maize_p_slider)
wb4 = widgetbox(p4,
               sesame_c1_slider, 
               sesame_c2_slider, 
               sesame_p_slider)
wb5 = widgetbox(p5,
                sorghum_c1_slider, 
               sorghum_c2_slider, 
               sorghum_p_slider)

layout = gridplot([
        [wb1, wb2],
        [wb3,wb5],
        [plot,plot1],
        [plot2,plot3],
        [plot4]
        ])

curdoc().add_root(layout)
