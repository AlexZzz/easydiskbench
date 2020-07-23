#!/usr/bin/env python3
import argparse
import sys
import os
import csv
import plotly.graph_objects as go
import numpy as np
import pandas as pd

def get_time_value(filename):
    f = open(filename,"r+")
    count = 0
    for line in f.readlines():
        if line:
            linelist = line.split(",")
            count += 1
            yield int(linelist[0].strip()), int(linelist[1].strip()), int(count)

def count_lines(filename):
    count = 0
    f = open(filename, "r+")
    for line in f.readlines():
        count += 1
    return count

def work(args):
    if not args.median: # Do we need better solution?
        bplot_color_choice = 0
    fig = go.Figure()

    bplot_boxes = list()
    bplot_legends = list()

    header = ["time","value","op","bs"]
    for input_file in args.input:
        df = pd.read_csv(input_file,names=header)
        fig.add_trace(go.Scatter(df, x="time", y="value",mode="lines",name=input_file))
        print(df)

    fig.show()
#
#        if args.median:
#            fig.add_trace(go.Scatter(x=labels_plot,
#                                    y=np.array(values_plot),mode="lines",
#                                    name=input_file))
#        else:
#            fig.add_trace(go.Box(y=values_plot,
#                                    x=labels_plot,
#                                    name=input_file))
#
#    fig.update_layout(title=args.title,
#                    xaxis_title=args.xlabel,
#                    yaxis_title=args.ylabel)
#    fig.update_yaxes(rangemode="tozero")
#    if (args.top_limit):
#        fig.update_yaxes(range=[0,args.top_limit])
#    if args.output:
#        fig.write_image(args.output)
#    else:
#        fig.show()

def main():
    parser = argparse.ArgumentParser(description="Plot stuff")
    parser.add_argument('--input','-i',type=str,nargs='*',help="Input files")
    parser.add_argument('--output','-o',type=str,help="Write char to this output file")
    parser.add_argument('--interval',type=int,help="Plot boxplot on interval (msec)",default=30000)
    parser.add_argument('--title','-t',type=str,help="Plot title",default="FIO results")
    parser.add_argument('--sum-bucket',type=int,help="Summarize values on this interval and treat it as a value to plot",default=0)
    parser.add_argument('--median',action='store_true',help="Plot medians without boxplot")
    parser.add_argument('--msec',action='store_true',help="Show time in milliseconds instead of seconds")
    parser.add_argument('--ylabel',type=str,help="Set this Y-label",default="latency (msec)")
    parser.add_argument('--xlabel',type=str,help="Set this X-label",default="time (s)")
    parser.add_argument('--value-divider',type=int,help="Divide values on this value. Default is for nsec->msec convertion. Set to 1 for IOPS plot",default=1e6)
    parser.add_argument('--top-limit',type=float,help="Set Y axis top limit")
    args = parser.parse_args()
    work(args)

if __name__=='__main__':
    sys.exit(main())
