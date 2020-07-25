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
    fig = go.Figure()
    header = ["time","value","op","bs"]

    for input_file in args.input:
        df = pd.read_csv(input_file,names=header)
        df['time_round'] = round(df['time']/args.interval)*args.interval+args.interval
        df['value'] /= args.value_divider

        if not args.msec:
            df['time_round'] /= 1e3

        if args.median:
            if args.per_second:
                df = df.groupby('time_round').sum().reset_index()
                df['value'] /= args.interval/1e3
            else:
                df = df.groupby('time_round').median().reset_index()
            fig.add_trace(go.Scatter(x=df['time_round'], y=df['value'],
                                mode="lines",name=input_file))
        else:
            fig.add_trace(go.Box(x=df['time_round'], y=df['value'],
                                name=input_file))

    fig.update_layout(title=args.title,
                    xaxis_title=args.xlabel,
                    yaxis_title=args.ylabel,
                    legend=dict(
                        font=dict(
                            size=24
                        )))
    if (args.top_limit):
        fig.update_yaxes(range=[0,args.top_limit])
    fig.update_yaxes(rangemode="tozero")

    if args.output:
        fig.write_image(args.output,width="1920",height="1080")
    else:
        fig.show()

def main():
    parser = argparse.ArgumentParser(description="Plot stuff")
    parser.add_argument('--input','-i',type=str,nargs='*',help="Input files")
    parser.add_argument('--output','-o',type=str,help="Write char to this output file")
    parser.add_argument('--interval',type=int,help="Plot boxplot on interval (msec)",default=30000)
    parser.add_argument('--title','-t',type=str,help="Plot title",default="FIO results")
    parser.add_argument('--per-second',action='store_true',help="Count per-second average value for the given interval (eg IO/s graph)")
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
