#!/usr/bin/env python3
import argparse
import sys
import os
import csv
import matplotlib.pyplot as plt
import numpy as np

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
    for input_file in args.input:
        bound = args.interval
        sum_bound = args.sum
        values_plot = list() # Values of Y to plot
        labels_plot = list() # Labels for X to plot on
        values = list() # Raw values from file
        lines_count = count_lines(input_file)
        for k, v, c in get_time_value(input_file):
            if (k > bound): # |---s-----bk <- k is after the bound. Cleanup and prepare for plot
                labels_plot.append(bound)
                values_plot.append(np.array(values).astype(np.float))
                values.clear()
                bound = bound + args.interval
                sum_bound = args.sum
                values.append(v)
            elif (sum_bound):
                if (k <= bound - args.interval + sum_bound): # |-k-s-----b <- we are between '|' and 's'
                    try:
                        values[-1] += v
                    except IndexError: # The only reason is empty list
                        values.append(v)
                else: # summarize for this bucket
                    sum_bound += args.sum
                    if (sum_bound > bound):
                        sum_bound = bound
                    values.append(v)
            else: # We are not summing and not over the bound. Just add new value
                values.append(v)

            if (c == lines_count): # We done. This was the last iteration
                labels_plot.append(k)
                values_plot.append(np.array(values).astype(np.float))

        axes.boxplot(
            values_plot,
            vert=True,
            patch_artist=True,
            labels=labels_plot, # Plot name as filename
            whis=[1,99])

    axes.set_title(args.title)
    plt.ylim(ymin=0)
    plt.grid(True)
    plt.show()

def main():
    parser = argparse.ArgumentParser(description="Plot stuff")
    parser.add_argument('--input','-i',type=str,nargs='*',help="Input files")
    parser.add_argument('--output','-o',type=str,help="Output file")
    parser.add_argument('--interval',type=int,help="Plot boxplot on interval (msecs)",default=30000)
    parser.add_argument('--title','-t',type=str,help="Plot title",default="FIO results")
    parser.add_argument('--sum',type=int,help="Summarize values on this interval and treat it as a value to plot",default=0)
    parser.add_argument('--median',action='store_true',help="Plot medians without boxplot")
    args = parser.parse_args()
    work(args)

if __name__=='__main__':
    sys.exit(main())
