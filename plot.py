#!/usr/bin/env python3
import argparse
import sys
import os
import csv
import matplotlib.pyplot as plt
import numpy as np

# This is just a list for boxplot colors. Why not?
bplot_colors = ['red', 'blue', 'green', 'lightblue', 'lightgreen', 'pink', 'burlywood', 'chartreuse']

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
    figure, axes = plt.subplots(nrows=1,ncols=1,figsize=(9,4))
    if not args.median: # Do we need better solution?
        bplot_color_choice = 0

    bplot_boxes = list()
    bplot_legends = list()

    for input_file in args.input:
        bound = args.interval
        sum_bound = args.sum_bucket
        values_plot = list() # Values of Y to plot
        labels_plot = list() # Labels for X to plot on
        values = list() # Raw values from file
        lines_count = count_lines(input_file)
        for timestamp, v, line_num in get_time_value(input_file):
            v = v / args.value_divider
            if (timestamp > bound): # |---s-----bt <- t is after the bound. Cleanup and prepare for plot
                if not args.msec:
                    labels_plot.append(bound/1e3)
                else:
                    labels_plot.append(bound)
                if args.median: # Count median here if needed
                    values_plot.append(np.percentile(values,50))
                else:
                    values_plot.append(np.array(values).astype(np.float))
                values.clear()
                bound = bound + args.interval
                sum_bound = args.sum_bucket
                values.append(v)
            elif (sum_bound):
                if (timestamp <= bound - args.interval + sum_bound): # |-t-s-----b <- we are between '|' and 's'
                    try:
                        values[-1] += v
                    except IndexError: # The only reason is empty list
                        values.append(v)
                else: # If we're out of bucket, then create set new sum_bound
                    sum_bound += args.sum_bucket
                    if (sum_bound > bound):
                        sum_bound = bound
                    values.append(v) # And append value to new bucket
            else: # We are not summing and not over the bound. Just add new value
                values.append(v)

            if (line_num == lines_count): # We done. This was the last iteration
                if not args.msec:
                    labels_plot.append(timestamp/1e3)
                else:
                    labels_plot.append(timestamp)
                if args.median:
                    values_plot.append(np.percentile(values, 50))
                else:
                    values_plot.append(np.array(values).astype(np.float))

        if args.median:
            axes.plot(labels_plot,np.array(values_plot),'o-',label=input_file)
        else:
            locs, ticks = plt.xticks()
            manage_ticks = False
            if len(locs) < len(labels_plot):
                manage_ticks = True
            bp = axes.boxplot(
                values_plot,
                vert=True,
                manage_ticks=manage_ticks,
                patch_artist=True,
                labels=labels_plot, # Plot name as filename
                whis=[1,99],
                boxprops=dict(
                    facecolor=bplot_colors[bplot_color_choice])
                )
            bplot_boxes.append(bp["boxes"][0])
            bplot_legends.append(input_file)
            bplot_color_choice += 1

    axes.set_title(args.title)
    if not args.median:
        axes.legend(bplot_boxes,bplot_legends)
    else:
        plt.legend()
    plt.ylabel(args.ylabel)
    plt.xlabel(args.xlabel)
    if (args.top_limit):
        plt.ylim(bottom=0,top=args.top_limit)
    else:
        plt.ylim(bottom=0)
    plt.grid(True)
    plt.show()

def main():
    parser = argparse.ArgumentParser(description="Plot stuff")
    parser.add_argument('--input','-i',type=str,nargs='*',help="Input files")
    parser.add_argument('--output','-o',type=str,help="Output file")
    parser.add_argument('--interval',type=int,help="Plot boxplot on interval (msec)",default=30000)
    parser.add_argument('--title','-t',type=str,help="Plot title",default="FIO results")
    parser.add_argument('--sum-bucket',type=int,help="Summarize values on this interval and treat it as a value to plot",default=0)
    parser.add_argument('--median',action='store_true',help="Plot medians without boxplot")
    parser.add_argument('--msec',action='store_true',help="Show time in milliseconds instead of seconds")
    parser.add_argument('--ylabel',type=str,help="Set this Y-label",default="latency (msec)")
    parser.add_argument('--xlabel',type=str,help="Set this X-label",default="time (s)")
    parser.add_argument('--value-divider',type=int,help="Divide values on this value. Default is for nsec->msec convertion",default=1e6)
    parser.add_argument('--top-limit',type=float,help="Set Y axis top limit")
    args = parser.parse_args()
    work(args)

if __name__=='__main__':
    sys.exit(main())
