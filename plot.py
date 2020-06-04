#!/usr/bin/env python3
import argparse
import sys
import os
import csv
import matplotlib.pyplot as plt
import numpy as np

def get_time_value(filename):
    f = open(filename,"r+")
    for line in f.readlines():
        if line:
            linelist = line.split(",")
            yield int(linelist[0].strip()), int(linelist[1].strip())

def get_output(args):
    if args.output:
        return open(args.output, "w+")
    else:
        return sys.stdout

def work(args):
    figure, axes = plt.subplots(nrows=1,ncols=1,figsize=(9,4))
    values_plot = list()
    labels = list()
    for input_file in args.input:
        bound = args.interval
        sum_bound = args.sum
        values = list()
        labels = list()
        for k, v in get_time_value(input_file):
            if (k > bound):
                labels.append(bound)
                values_plot.append(np.array(values).astype(np.float))
                values.clear()
                bound = bound + args.interval
                sum_bound = args.sum
                values.append(v)
            elif (sum_bound):
                if (k <= bound - args.interval + sum_bound): # |--s-----i <- we are between '|' and 's'
                    try:
                        values[-1] += v
                    except IndexError: # The only reason is empty list
                        values.append(v)
                else:
                    sum_bound += sum_bound
                    if (sum_bound > bound):
                        sum_bound = bound
                    values.append(v)
            else:
                values.append(v)

    axes.boxplot(
        values_plot,
        vert=True,
        patch_artist=True,
        labels=labels, # Plot name as filename
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
    parser.add_argument('--sum',type=int,help="Summarize by this interval to plot boxplot",default=0)
    parser.add_argument('--median',action='store_true',help="Plot medians without boxplot")
    args = parser.parse_args()
    work(args)

if __name__=='__main__':
    sys.exit(main())
