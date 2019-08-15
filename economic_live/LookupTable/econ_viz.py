#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 11:07:52 2019

@author: deborahkhider

Slide visualization econ
"""

#import numpy as np
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
    
    #Query
    df = econ_data.loc[(econ_data['crop']=='cassava') & (econ_data['p'] == cassava_p_dynamic) & (econ_data['c1'] == cassava_c1_dynamic) & (econ_data['c2'] == cassava_c2_dynamic)]
    econ_data_c = econ_data[econ_data['run_ID'].isin(df['run_ID'])]

    df1 = econ_data_c[(econ_data_c['crop']=='groundnuts') & (econ_data_c['p'] == groundnuts_p_dynamic) & (econ_data_c['c1'] == groundnuts_c1_dynamic) & (econ_data_c['c2'] == groundnuts_c2_dynamic)]
    econ_data_g = econ_data_c[econ_data_c['run_ID'].isin(df1['run_ID'])]

    df2 = econ_data_g[(econ_data_g['crop']=='maize') & (econ_data_g['p'] == maize_p_dynamic) & (econ_data_g['c1'] == maize_c1_dynamic) & (econ_data_g['c2'] == maize_c2_dynamic)]
    econ_data_m = econ_data_g[econ_data_g['run_ID'].isin(df2['run_ID'])]

    df3 = econ_data_m[(econ_data_g['crop']=='sesame') & (econ_data_m['p'] == sesame_p_dynamic) & (econ_data_m['c1'] == sesame_c1_dynamic) & (econ_data_m['c2'] == sesame_c2_dynamic)]
    econ_data_s = econ_data_m[econ_data_m['run_ID'].isin(df3['run_ID'])]

    df4 = econ_data_s[(econ_data_s['crop']=='sorghum') & (econ_data_s['p'] == sorghum_p_dynamic) & (econ_data_s['c1'] == sorghum_c1_dynamic) & (econ_data_s['c2'] == sorghum_c2_dynamic)]
    econ_data_s2 = econ_data_s[econ_data_s['run_ID'].isin(df4['run_ID'])]

    econ_data_f = econ_data_s2.iloc[0:5,:] #This takes care of the fact that the base run is run 5 times
    
    # Update the data
    data['y'] = econ_data_f['yield (kg/ha)']
    data1['y'] = econ_data_f['Nfert (kg/ha)']
    data2['y'] = econ_data_f['production (kg)']
    data3['y']= econ_data_f['Nuse (kg)']
    data4['y'] = econ_data_f['land area (ha)']/econ_data_f['land area (ha)'].sum() * 2*pi
    #pie_data.loc['value']= econ_data_f['land area (ha)']
    #pie_data['angle']= pie_data['value']/pie_data['value'].sum() * 2*pi
    print(data1, data2, data3, data4)
    
econ_data = pd.read_csv("results_summary_bycrop.csv")
x = list(econ_data["crop"].unique())
runID = list(econ_data["run_ID"].unique())
plot_size = 300

# Find a baserun to get the bar graph started
base = None
for ID in runID:
    if base is None and any(list(econ_data[(econ_data["run_ID"]==ID)][['c1','c2','p']].any())) is False:
        base = econ_data[(econ_data["run_ID"]==ID)]
        total_area = round(sum(base['land area (ha)']))    

# Source data for the bar charts        
source = ColumnDataSource(data=dict(x=x, y=list(base['yield (kg/ha)'])))
source1 = ColumnDataSource(data=dict(x=x, y=list(base['Nfert (kg/ha)'])))
source2 = ColumnDataSource(data=dict(x=x, y=list(base['production (kg)'])))
source3 = ColumnDataSource(data=dict(x=x, y=list(base['Nuse (kg)'])))

# Data for the pie charts
# if land is unallocated use this
#y3 = {'cassava': int(base[(base["crop"]=='cassava')]['land area (ha)']),
    #'groundnuts': int(base[(base["crop"]=='groundnuts')]['land area (ha)']), 
    #'maize': int(base[(base["crop"]=='maize')]['land area (ha)']), 
    #'sesame': int(base[(base["crop"]=='sesame')]['land area (ha)']),
    #'sorghum': int(base[(base["crop"]=='sorghum')]['land area (ha)']), 
    #'not allocated': int(int(sum(base['land area (ha)']))-total_area)}

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
