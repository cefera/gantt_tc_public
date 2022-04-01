# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 10:23:34 2022

@author: cesar
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


jpac_blue   = "#1F77B4"; jpac_red    = "#D61D28";
jpac_green  = "#2CA02C"; jpac_orange = "#FF7F0E";
jpac_purple = "#9467BD"; jpac_brown  = "#8C564B";
jpac_pink   = "#E377C2"; jpac_gold   = "#BCBD22";
jpac_aqua   = "#17BECF"; jpac_grey   = "#7F7F7F";

jpac_color = [jpac_blue, jpac_red, jpac_green, 
              jpac_orange, jpac_purple, jpac_brown,
              jpac_pink, jpac_gold, jpac_aqua, jpac_grey ];


#%%

calibrate = pd.read_excel('Calibrate.xlsx')

calibrate_start = calibrate.Start.min()

calibrate['start_num'] = (calibrate.Start-calibrate_start).dt.days
# number of days from project start to end of tasks
calibrate['end_num'] = (calibrate.End-calibrate_start).dt.days
# days between start and end of each task
calibrate['days_start_to_end'] = calibrate.end_num - calibrate.start_num


calibrate1 = pd.read_excel('Calibrate1.xlsx')

calibrate_smonth = calibrate1.Smonth.min()

calibrate1['start_num_month'] = (calibrate1.Smonth-calibrate_smonth).dt.days
# number of days from project start to end of tasks
calibrate1['end_num_month'] = (calibrate1.Emonth-calibrate_smonth).dt.days
# days between start and end of each task
calibrate1['days_start_to_end_month'] = calibrate1.end_num_month - calibrate1.start_num_month

     
#%%

df = pd.read_excel('Plan.xlsx')

# project start date
proj_start = df.Start.min()
# number of days from project start to task start
df['start_num'] = (df.Start-proj_start).dt.days
# number of days from project start to end of tasks
df['end_num'] = (df.End-proj_start).dt.days
# days between start and end of each task
df['days_start_to_end'] = df.end_num - df.start_num

'''
fig, ax = plt.subplots(1, figsize=(16,6))
ax.barh(df.Task, df.days_start_to_end, left=df.start_num)
plt.show()
'''
# create a column with the color for each department
def color(row):
    c_dict = {'TG-1':jpac_color[0], 'TG-2':jpac_color[1], 'TG-3':jpac_color[2]}
    return c_dict[row['Department']]
df['color'] = df.apply(color, axis=1)

#%%

from matplotlib.patches import Patch
fig, ax = plt.subplots(1, figsize=(16,6))
ax.barh(df.Task, df.days_start_to_end, left=df.start_num, color=df.color)
##### LEGENDS #####
c_dict = {'TG-1':jpac_color[0], 'TG-2':jpac_color[1], 'TG-3':jpac_color[2]}
legend_elements = [Patch(facecolor=c_dict[i], label=i)  for i in c_dict]
plt.legend(handles=legend_elements)
##### TICKS #####
xticks = np.arange(0, df.end_num.max()+1, 3)
xticks_labels = pd.date_range(proj_start, end=df.End.max()).strftime("%m/%d")
xticks_minor = np.arange(0, df.end_num.max()+1, 1)
ax.set_xticks(xticks)
ax.set_xticks(xticks_minor, minor=True)
ax.set_xticklabels(xticks_labels[::3])
plt.show()

# days between start and current progression of each task
df['current_num'] = (df.days_start_to_end * df.Completion)

from matplotlib.patches import Patch
fig, ax = plt.subplots(1, figsize=(16,6))
# bars
ax.barh(df.Task, df.current_num, left=df.start_num, color=df.color)
ax.barh(df.Task, df.days_start_to_end, left=df.start_num, color=df.color, alpha=0.5)
# texts
for idx, row in df.iterrows():
    ax.text(row.end_num+5, idx, 
            f"{row.Name}", 
            va='center', alpha=0.8)
##### LEGENDS #####
c_dict = {'TG-1':jpac_color[0], 'TG-2':jpac_color[1], 'TG-3':jpac_color[2]}
legend_elements = [Patch(facecolor=c_dict[i], label=i)  for i in c_dict]
plt.legend(handles=legend_elements)
##### TICKS #####
xticks = np.arange(0, df.end_num.max()+1, 3)
xticks_labels = pd.date_range(proj_start, end=df.End.max()).strftime("%y/%m")
xticks_minor = np.arange(0, df.end_num.max()+1, 1)
ax.set_xticks(xticks)
ax.set_xticks(xticks_minor, minor=True)
ax.set_xticklabels(xticks_labels[::3])
plt.show()
fig.savefig('gantt_tc_colortest.pdf', bbox_inches='tight')

#%%

from matplotlib.patches import Patch

# Printing

yearfontsize = 15
yearheight = 0.3
correction_x = 20
years = ['2022','2023','2024','2025','2026','2027']
months = np.array(calibrate1.Month)

# Limits
nplots = 3; aesthetic_limits = (0.,1.)
xlimits = (np.array(calibrate['start_num']).min(), np.array(calibrate['end_num']).max())

fig, subfig = plt.subplots(nplots, figsize=(16,9))
for i in range(nplots):
    subfig[i].axis('off')

#   Year labels
left, width = 0.1, 0.9; bottom, height = 0.95, 0.05;
rect_histy = [left, bottom, width, height]
subfig[0] = plt.axes(rect_histy)
subfig[0].set_xlim(xlimits)
subfig[0].set_ylim(aesthetic_limits)
subfig[0].vlines(calibrate.end_num,aesthetic_limits[0],aesthetic_limits[1],color='k' )
subfig[0].tick_params(direction='in', top=False, right=False,left=False,bottom=False,size=0,labelright=False,labelleft=False,labelbottom=False,labelsize=20)
for i in range(len(calibrate.end_num)):
    a, b = calibrate.start_num[i], calibrate.end_num[i] ;
    if i==0:
        c = a +  (b - a)/2. - 1.5*correction_x;        
    else:
        c = a +  (b - a)/2. - correction_x;
    subfig[0].text(c,yearheight,years[i],fontsize=yearfontsize)

#   Month labels
left, width = 0.1, 0.9; bottom, height = 0.90, 0.05;
rect_histy = [left, bottom, width, height]
subfig[1] = plt.axes(rect_histy)
subfig[1].set_xlim(xlimits)
subfig[1].set_ylim(aesthetic_limits)
subfig[1].vlines(calibrate1.end_num_month,aesthetic_limits[0],aesthetic_limits[1],color='k' )
subfig[1].tick_params(direction='in', top=False, right=False,left=False,bottom=False,size=10,labelright=False,labelleft=False,labelbottom=False,labelsize=20)
for i in range(len(calibrate1.end_num_month)):
    a, b = calibrate1.start_num_month[i], calibrate1.end_num_month[i] ;
    if months[i]=='OND':
        c = a +  (b - a)/2. - 1.5*correction_x;        
    else:
        c = a +  (b - a)/2. - correction_x;
    subfig[1].text(c,yearheight,months[i],fontsize=yearfontsize)





#   Gantt chart
left, width = 0.1, 0.9; bottom, height = 0.05, 0.85;
rect_histy = [left, bottom, width, height]
subfig[2] = plt.axes(rect_histy)
ymin, ymax = df.Task.min()-1, df.Task.max()+1
subfig[2].set_xlim(xlimits)
subfig[2].set_ylim((ymin,ymax))
xticks = np.array(calibrate1.end_num_month)
subfig[2].set_xticks(xticks)
subfig[2].tick_params(direction='in', top=True, right=False,left=False,bottom=True,size=10,labelright=False,labelleft=False,labelbottom=False,labelsize=20)
subfig[2].vlines(calibrate1.end_num_month,ymin,ymax,ls='dashed',lw=1,color='k' ,zorder=0)
subfig[2].barh(df.Task, df.days_start_to_end, left=df.start_num, color=df.color,zorder=2)
c_dict = {'TG-1':jpac_color[0], 'TG-2':jpac_color[1], 'TG-3':jpac_color[2]}
legend_elements = [Patch(facecolor=c_dict[i], label=i)  for i in c_dict]
subfig[2].legend(handles=legend_elements,loc='upper left',fontsize=20)

# texts
for idx, row in df.iterrows():
    subfig[2].text(row.end_num+10, idx, 
            f"{row.Name}", 
            va='center', alpha=1.,fontsize=yearfontsize)


plt.show()
fig.savefig('gantt_tc.pdf', bbox_inches='tight')

