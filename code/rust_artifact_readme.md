# Rust implementation README

For the most time-consuming tasks in pathleak (namely *generating sniffer data*, *intra-protocol mapping* and *inter-protocol mapping*), we offer a rust implementation accompanying the original, proof-of-concept Python one. This allows for much faster prototyping and experiments.

We explain how to set up the environment and run these tasks using the rust implementation.

## Overview

These tasks are implemented in pure rust, using standard toolchain version 1.92. We tested them on both Windows and Linux x64 targets, and they behave as expected.

The code are organized in a flat manner under `code/rust/src/tasks`, where each task inhabit one source file (e.g., `generate_sniffer_data.rs`). The main executable as defined in [`main.rs`](http://main.rs) accepts 2 command-line arguments: the first is the filename of the *run config* file, the second is the task name, which can be one of: `generate_sniffer_data`, `intra_map` or `inter_map`.

Once the config is loaded, the main executable then passes the control to the selected task implementation, which parses the config and runs the task.

The *run config* is a small YAML file specific to the rust implementation that defines, among other things, where to find the actual *task config* files (i.e., the ones used by the original implementation). It must contain a key-value pair named `root_dir` which points to the root folder of the original implementation (e.g., `code`). Task configs are loaded then from `code/configs`.

## Running the tasks

Make sure the correct rust toolchain is installed, and the correct run config is composed pointing to the right directory. Then, in the root directory of the rust implementation (e.g. `code/rust`), simply run. Results will be stored in the same format and in the same location as the original implementation.

```bash
$ cargo run --release -- /path/to/config.yaml task_name
```

## Quirks

There are a few quirks and/or optimizations that are specific to the rust implementation. We briefly go through them below.

### Trimming

Trimming is applied for both intra- and inter-protocol mapping. This means: when assessing the ultimate plausibility of two traces belonging to the end device, we no longer evaluate the plausibility of all pairs of locations in the traces, we only consider the pairs during their overlapping window (temporal) and during a small *grace period* immediately before and after this window.

We introduce this optimization based on the observation that if two traces are not close enough during their overlapping window, they will only be farther away outside this window. The reverse is also true: if they are close enough during this window, then they will always be considered as a potential match. In either case, there is no need to evaluate pairs outside this window (and the grace period around it).

Our tests suggest that there is virtually no impact from trimming on TPR.

Trimming can be fully disabled by enabling the `intra_map_disable_trim` and `inter_map_disable_trim` feature, respectively. It is configurable with a few additional options in the task config file, whose names are pretty self-explanatory:

```yaml
accel_settings:
  intra_map:
    trim_threshold: 5
    trim_grace_period: 60
    time_delta_threshold: 60
  inter_map:
    trim_grace_period: 60
```

`trim_threshold` controls the minimum number of samples in both traces needed to trigger trimming. `trim_trace_period` controls the length of grace period on both ends of the overlapping window, in simulation time step. `time_delta_threshold` controls the length of the overlapping window.

### Reversed compatibility matrix evaluation

After trimming, pairs of samples are grouped pair-wise into a *compatibility matrix* in which the *compatibility* of each pair is evaluated. If any pair is deemed incompatible, the entire matrix fails and the two traces are considered not compatible (i.e., impossible to have come from the same device). 

We accelerate this process by reversing the evaluation order for the right-hand samples (for convenience, the principle stands the same for left-hand samples): for LHS samples L1, L2, …, Ln and RHS samples R1, R2, …, Rn ordered by ascendingly by simulation time step, we evaluate pairs in the order of: [L1, Rn], [L1, Rn-1], …, [L1, R1], [L2, Rn], …, [Ln, R1]. The intuition here is that the farther away two samples are temporally, the farther away they may be spatially. This means we can filter out incompatible pairs and short circuit early on without having to evaluate the entire matrix.

The following table gives a quick impression on the effect of the optimization.

| Task | Baseline | Rust | Rust with trimming+reverse_order |
| --- | --- | --- | --- |
| intramap | 4866.67 | 7.15 (680.65x) | 2.99 (1627.45x) |
| intermap | 9499.16 | 18.35 (517.66x) | 5.73 (1657.79x) |