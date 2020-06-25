# FIO-runner
...is a flexible IO tester runner.

This repo contains a small set of tests and a few scripts to run the benchmarks and plot results.

### What for?
It was basically written to benchmark virtual machine's network disks.

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

Now graphs are plotted using both results!

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
* `libaio` is used, because it's one of the most popular library. At least, most drive-latency-sensitive application uses libaio.
* `O_SYNC` is used for synchronized IO. It is possible to use `fsync()`/`fdatasync()`, but if we use `O_SYNC`, it's easier to parse results - every `clat` includes flush request.
* Every test runs twice. This is especially important for the first test in suite, first run will be (sometimes much) slower, than the second run.
* Every test runs with iodepth=1. We don't measure concurrent access here, only one-thread latency. As these tests were written for benchmarking cloud environment, we may assume that every one parallel IO or parallel thread will add the same performance as one-threaded fio, until we hit the limit.

There're different types of workloads:
1. synchronized random writes
2. synchronized sequential writes
3. random writes
4. sequential writes
5. random reads
6. sequential reads

And all the kinds of random workloads with pareto distribution.

#### Synchronized writes with small block size

Databases on the network disks are often limited by one-threaded latency of the database journaling thread. Most of them write to the journal with 8K blocks. So, for simplicity these benchmarks might tell something about database performance on the test drive. Do not interpret it as-is, do the comparison!

#### Random and sequiential reads

These tests might show difference if the storage provides readahead logic. Sequential reads could be faster.

#### Pareto distribution

Pareto distribution test benchmarks the cache if it is enabled for a virtual machine. If cache is used, the `rr`(random read) test will show performance growth. It will also show performance growth (but less!) without cache, because most backends use their own caching (e.g. on the server with the part of a disk).
If it is a writeback caching, it might show performance degradation for synchronized writes.

## TODO
1. Add test suite to benchmark with different level of parallelism.
