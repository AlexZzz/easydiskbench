# EasyDiskBench
...is a flexible IO tester runner.

This repo contains a small set of tests and a few scripts to run the benchmarks and plotting results.

It uses plotly and plotly-orca to build and save plots.

### What for?
It was basically written to benchmark virtual machine's network disks.

## Prerequisites
You must have `plotly` and [plotly-orca](https://github.com/plotly/orca) packages installed to plot the graphs.

## How to

Create a VM.

Run tests:

`./run-basic.sh root yourserver.com /root/fio`

Plot graphs:

`./plot-all.sh`

Create another VM.

Run tests:

`./run-basic.sh root yourserver.com /root/fio`

Plot graphs:

`./plot-all.sh`

Now graphs are plotted using both data sets!

## Interpreting results

### Tests and results naming

Every test adhere to the naming scheme:
```
rr - random read
r - read
rw - random write
w - write
```
Block size - 4k for 4 kibibyte, 4m for 4 mebibyte.

`sync` suffix is set when writes are synchronized.

### Workloads

* `O_DIRECT` flag is used to bypass the page cache.
* `libaio` is used, because it's the most popular library. At least, most drive-latency-sensitive application use libaio.
* `O_SYNC` is used for synchronized IO. It is possible to use `fsync()`/`fdatasync()`, but if we use `O_SYNC`, it's easier to parse results - every `clat` includes flush request.
* Every test runs twice. This is especially important for the first test in suite, first run will be (sometimes much) slower, than the second run.
* Every test runs with iodepth=1. We don't measure concurrent access latency/bandwidth here, only one-thread latency. As these tests were written for benchmarking cloud environment, we may assume that every one parallel IO or parallel thread will add the same performance as one-threaded fio, until we hit the limit.

There're different types of workloads:
1. synchronized random writes
2. synchronized sequential writes
3. random writes
4. sequential writes
5. random reads
6. sequential reads

And all the kinds of random workloads with pareto distribution.

## run-basic.sh

`run-basic.sh` accepts four arguments:
1. `remote_user` - remote user name, will be used for ssh/scp.
2. `host` - hostname of the remote virtual machine (or IP-address).
3. `path` - path to the directory which will be created, used for the tests and cleaned up.
4. `filename` - name of the file, which will be used with a `--filename` argument for the FIO. You may use it to specify disk name, e.g. `/dev/sdb`.

## plot-all.sh

Runs `plot.py` to plot graphs from `./results/*` directories. You may pass any other directories as arguments:
`./plot-all.sh ./results/first ./results/second`

## plot.py

Plots graphs from FIO log passed with `-i` argument. `--interval (msec)` is used to count median or distribution for the time interval in milliseconds.

If one wants to see a distribution instead of median value, just drop `--median` flag. So, plotting latency results is easy:
```
./plot.py -i lat_results.1.log --interval 10000 -o lat_results.png
```

To plot from FIO IOPS log which is collected without summarization, it is useful to summarize values and count per-second IO rate. Use `--per-second` for it. Set `--value-divider` to 1, to print raw values (number of IOs). All the values are divided by the value represented by this option. Default value is 1000000, which is used to convert latency results from nanoseconds to milliseconds.
```
./plot.py -i iops_results.1.log --interval 1000 --ylabel IO/s --value-divider 1 --median --per-second -o iops_results.png
```

To plot bandwidth log it may be useful to set `--value-divider` to 1024, so one can see MiB/s. Use `--interval 1000` to really make it per second.
```
./plot.py -i bw_results.1.log --interval 1000 --ylabel MiB/s --value-divider 1024 --median -o bw_results.png
```

Use `plot.py --help` to find out more about options.

## TODO
1. Fix boxplot plotting on many data sets. Boxplots must be placed side by side within interval region.
2. Add test suite to benchmark with different level of parallelism.
