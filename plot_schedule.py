#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 10:28:39 2019

@author: joncosgrove

plot caltrain schedule in the style of Marey as seen in 
The Visual Display of Quantative Data, Tufte

example: https://github.com/bradtraversy/python_bokeh_chart
example: https://github.com/bokeh/bokeh/blob/master/examples/models/file/panels.py
"""

import bokeh.plotting as bk
import bokeh.models as bkm
from bokeh.colors import rgb
import pandas as pd
import re


path = '/Users/joncosgrove/Dropbox/Projects/Caltrain schedule/'
# files = ['Caltrain schedule/Weekday_Southbound-Table 1.csv']
# file = ['Caltrain schedule/Weekday_Southbound-Table 1.csv']
# files = ['Caltrain schedule/Weekday_Northbound-Table 1.csv']
files = ['Caltrain schedule/Weekday_Southbound-Table 1.csv',
            'Caltrain schedule/Weekday_Northbound-Table 1.csv']
# d = pd.read_csv(path + file, header=1)

# stops = ~d.isnull()

####################
# matplotlib version
####################
# from matplotlib import pyplot as plt

# file = 'Caltrain schedule/Weekday_Southbound-Table 1.csv'
# d = pd.read_csv(path + file, header=1)
# stops = ~d.isnull()

# fig = plt.figure()
# ax = fig.add_subplot(111)

# X = d.Train_366[stops.Train_366]
# Y = d.Milepost[stops.Train_366]
# S = d.Station[stops.Train_366]

# plt.plot(X, Y, '.-')
# #for xy in zip(X, Y):                                       # <--
# #    ax.annotate('(%s, %s)' % xy, xy=xy, textcoords='data') # <--
# ax.set_yticks(d.Milepost.values)
# ax.set_yticklabels(d.Station.values)
# ax.grid(True, which='major', axis='y', lw=0.25, c='gray')

# plt.show()


###############
# bokeh version
###############
def plot_setup(d):
    # title = file.split('/')[1].split('-')[0]
    title = 'Caltrain'
    p = bk.figure(title=title,
                  plot_width=1200,
                  plot_height=800,
                  x_axis_type='datetime',
                  x_axis_label='Departure Time',
                  y_axis_label='Station',
                  active_scroll='wheel_zoom')
    # style
    axis_line_color = (150,150,150) # rgb value for axis line color

    # grid and tools
    p.xgrid.grid_line_color = None
    p.toolbar.logo = None
    # p.legend.location = "top_left"
    # p.legend.click_policy="mute"

    # xaxis
    xformat = bkm.DatetimeTickFormatter(hours=["%H:%M"],
                                 minutes=["%H:%M"])
    p.xaxis.formatter = xformat
    p.xaxis.axis_line_color = axis_line_color
    # p.xaxis.major_label_orientation=math.radians(30)
    p.add_layout(bkm.axes.DatetimeAxis(axis_label=None,
                                       axis_line_color=axis_line_color,
                                       formatter=xformat), "above")

    n = pd.datetime.now().date()
    xstart = n + pd.DateOffset(hour=6)
    xend = n + pd.DateOffset(hour=10)
    p.x_range = bkm.ranges.Range1d(xstart, xend)#d.Milepost.values.max())

    #  yaxis
    p.y_range = bkm.ranges.Range1d(0,47.7)#d.Milepost.values.max())
    p.ygrid.ticker = d.Milepost.values
    p.yaxis.ticker = d.Milepost.values
    p.yaxis.axis_line_color = axis_line_color
    station_labels = dict(zip(d.Milepost.values, d.Station.values))
    p.yaxis.major_label_overrides = station_labels

    # station_labels = dict(zip(d.Milepost.values, d.Station.values))
    p.extra_y_ranges["y"] = bkm.ranges.Range1d(0,d.Milepost.values.max())


    # p.add_layout(bkm.axes.LinearAxis(axis_label="Station",
    #                                  major_label_overrides=station_labels,
    #                                  ticker=d.Milepost.values), "right")
    p.add_layout(bkm.axes.LinearAxis(axis_label="Milepost",
                                     axis_line_color=axis_line_color,
                                     ticker=d.Milepost.values), "right")
    print('Running plot setup')
    return p


def add_route(train_no, figure, stop_markers=True):

    train_no=str(train_no)
    train = "Train_" + train_no
    X = d[train][stops[train]]
    X = pd.to_datetime(X)
    if train == "Train_196":
        X[22] = X[22] + pd.Timedelta(days=1)
        print(X)
    elif train == "Train_199":
        X[28] = X[28] + pd.Timedelta(days=1)
        print(X)
    Y = d.Milepost[stops[train]]
    S = d.Station[stops[train]]
    data = pd.concat([X, Y, S], axis='columns')
    source = bk.ColumnDataSource(data)

# set line colors and weights
    # color = rgb(r(204),g(74),b(71))
    if len(data.index)<=10:
        c='darkslategray'
        w=2
    else:
        c='darkslategray'
        w=1

    p.line('Train_'+train_no,
            'Milepost',
            source=source,
            line_color=(91,91,91), #gray
            line_width=w,
            name='Train_'+train_no
            # legend='Train_'+train_no
            )
    if stop_markers==True:
        p.circle('Train_'+train_no,
            'Milepost',
            source=source,
            size=1.75,
            fill_color=None,
            color=c)
    return p #, X, Y, S, data, source



plot_setup_complete = False
for file in files:
    d = pd.read_csv(path + file, header=1)

    stops = ~d.isnull()

    if plot_setup_complete == False:
        print("setting up plot")
        p = plot_setup(d=d)
        plot_setup_complete = True

    for item in d.keys().values:
        m = re.search(r'\d{3}', item, re.I)
        if m:
            p = add_route(str(m.group()[0:3]), figure=p)
    
    # p, X, Y, S, data, source = add_route("314", figure=p)

hover = bkm.tools.HoverTool()
hover.tooltips = """
  <div>
    <h3>$name</h3>
    <div><strong>Station: </strong>@Station</div>
    <div><strong>Milepost: </strong>@Milepost{00.0}</div>
  </div>
"""
# <div><strong>Time: </strong>$x</div>
# <div><img src="@Image" alt="" width="200" /></div>
p.add_tools(hover)
bk.output_file('index.html')
bk.save(p)
# bk.show(p)
