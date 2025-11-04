# Notes to the original README

## Setting up the environment

### Poetry vs venv

It might be easier altogether just to use venv to manage the dependencies especially given that there is currently no
plan to publish this project as a ready-to-use library. To produce the regular `requirements.txt` for pip, run the
following command. Note that the `export` command in poetry is provided by a dedicated plugin since version 2 and must
be installed separately.

```shell
poetry export --without-hashes -o requirements.txt
```

### SUMO on Windows

Despite official support of SUMO for Windows, there still seems to be some dependency problem that prevents the normal
loading of libsumo when used in a virtual environment. A quick investigation of import tables and Windows's internal log
for calls to `LoadImage` revealed no immediate cause. As a workaround, install all dependencies to the system
interpreter. On Windows, this requires no administrative privilege anyway and should just work.

### SUMO on Linux

The `requirements.txt` exported from the poetry config in the repository includes a SUMO redistributable from pip (
`ellipse-sumo`, etc). However, this package contains only part of the dependencies for SUMO and consequently causes an
import error when libsumo is imported in Python. To solve this, install SUMO also from the distribution's package
manager. This should come with all the necessary dependencies.

### Run time measurement

The original script uses a rather hacky way of launching tasks with `subprocess.run` and with `time` to measure the task
run time. Necessary patches were added to programmatically launch tasks and measure with Python's builtin `time`
package.
This also allows for easier IDE debugging and Windows compatibility.

## Procedure and tasks

Please note that unless otherwise specified, all runs in this chapter assumes the config file
`scenario_test_32_sumo_new.yml` and is dispatched on a system with a Zen 3 processor@4GHz with 6 physical cores.

### Baseline and overview

The following table gives the baseline measurement of run time for all required tasks for a successful full run.
It also gives an overview of the current progress of the new implementation. The most time-consuming tasks are marked in
bold italic. For tasks that allows choosing individual protocols to run
on (e.g., `intramap_optimized`), the run time is collected from runs over only Bluetooth and LTE.

| Task name                   | Run time (second, Bluetooth & LTE) | Run time (second - percentage, all protocols) | New run time (second - speedup, all protocols) |
|-----------------------------|------------------------------------|-----------------------------------------------|------------------------------------------------|
| **_sumo_**                  | **_980.22_**                       | **_980.22_**   -  **_5.96%_**                 | **_980.22_**  -  **_1x_**                      |
| **_filter_users_polygon_**  | **_349.09_**                       | **_349.09_**   -  **_2.12%_**                 | **_10.86_**   -  **_32.14x_** \<               |
| filter_users_RI_Count       | 23.14                              | 23.14          -  0.14%                       | 23.14         -  1x                            |
| generate_user_data          | 21.68                              | 21.68          -  0.13%                       | 21.68         -  1x                            |
| **_generate_sniffer_data_** | **_679.62_**                       | **_679.62_**   -  **_4.14%_**                 | **_3.7_**     -  **_183.68x_** \<              |
| filter_sniffer_data         | 1.33                               | 1.33           -  0.01%                       | 1.33          -  1x                            |
| aggregate                   | 0.63                               | 0.63           -  0.00%                       | 1.63          -  1x                            |
| **_intramap_optimized_**    | **_162.22_**                       | **_4,866.67_** -  **_29.61%_**                | **_2.99_**    -  **_1627.65x_** \<             |
| **_intermap_optimized_**    | **_880.26_**                       | **_9,499.16_** -  **_57.80%_**                | **_5.73_**    -  **_1657.79x_** \<             |
| refine_intramap             | 0.67                               | 0.67           -  0.00% \&                    | 0.67          -  1x                            |
| intra_filter                | 0.48                               | 0.48           -  0.00% \&                    | 0.48          -  1x                            |
| reconstruction_multi        | 5.91                               | 5.91           -  0.04% \&                    | 5.91          -  1x                            |
| reconstruction_single       | 3.97                               | 3.97           -  0.02% \&                    | 3.97          -  1x                            |
| plot                        | 0.86                               | 0.86           -  0.01% \&                    | 0.86          -  1x                            |
| --                          | --                                 | --                                            | --                                             |
| **_Major total_**           | **_3051.41_**                      | **_16,374.76_**                               | **_1003.50_** -  **_16.32x_**                  |
| *Total*                     | 3110.08                            | 16,433.43                                     | 1062.17       -  15.47x                        |
| *Major percentage*          | 98.11%                             | 99.64%                                        |                                                |

`&` denotes measurements that have yet been tested in a full-protocol run. `>` denotes tasks that have been ported
to the new implementation.

### Correctness

Currently, we employ three strategies to verify the correctness of the new implementation:

- We compare the results between the new and the original implementation, and between new implementations (Rust and C#)
  where applicable.
- We compare the results from before and after we introduced our modification to the algorithm.
- We keep the real user id in the generate observation samples which reflects the ground truth. We then use this
  baseline to measure the performance of the algorithm.

### SUMO

The `sumo` task is in charge of loading the predefined SUMO config files and running the actual simulation for
pedestrians and vehicles. The speed of this task is bound by SUMO itself and there is not much room for improvement.
SUMO also does not have stable support for parallel processing. As a result, this step usually takes more than 15
minutes.

The simulation also produces a ton of warning of pedestrians and/or vehicles getting jammed and/or having to be
teleported elsewhere in the map. There might be some potential for optimisation here as per SUMO's documentation,
constant jamming often slows down the simulation.

### Filter users by polygon

This tasks filters out users that are not within the area described by the given polygon. This step is the fourth most
time-consuming tasks. Luckily, there is a clear opportunity for optimisation with parallel processing since there is no
inter-data dependency. This optimisation can be done directly in Python. Meanwhile, despite using a native
implementation of point-in-polygon algorithm, the frequent crossing of C-Python boundary incurs non-trivial interface
cost (as opposed to big-and-bulky usages). A quick C# implementation yields promising results and a Rust port is
expected
to cut the run time by a further half.

One important discrepancy moving to native implementation is that we have chosen to use single-precision floating numbers
(`f32` in Rust) instead of double as used by CPython and numpy by default. This allows more compact storage and slightly faster
computation, while the loss of precision has so far caused no deviation of results between the new and the original
implementation.

| Task                 | Baseline | Python multiprocessing | C#             |
|----------------------|----------|------------------------|----------------|
| filter_users_polygon | 349.09   | 124.44 (2.8x)          | 10.86 (32.14x) |

### Generate user data

It is unclear if it is also required to run the tasks `filter_users_polygon` and `filter_users_RI_count` after `sumo` is
completed. However, the original simulation result produced by SUMO contains more than 35 million data points and takes
multiple hours to process through user data generation. By contrast, `filter_users_RI_count` produces filtered result
where data points for each simulation timestep is limited to a certain threshold. This greatly reduces the data volume (
e.g., to ~3 million) and accelerates the data generation.

However, results generated by the `filter_users_RI_count` task also do not bear the expected filename of this task. It
is necessary as of now to manually rename te desired filtered outputs (e.g., from
`raw_user_data_scenario_test_32_sumo_new_32.csv` to `raw_user_data_scenario_test_32.csv`). It remains unclear why there
exists no task that so generates. The original README suggested that the `sumo` task does this, but evidently is not the
case.

Speed-wise, the script contains a few weird choices that largely crippled the performance.

- Use of `deque` appears pointless. It can only be assumed that it was favoured over the simple list in the hope that
  appending never incurs array resizing and thus avoids unnecessary data copy. However, deque internally employs a
  linked list which has horrible data locality and sequential read performance, both of which negatively impacts the
  performance while the collected data is later iterated over to another data frame and to disk. Copying cost is also
  easily marginalised under high data volume.
- Converting loaded data frames into a dictionary seems pointless and exacerbates memory waste.

Fixing the above reduces run time by ~50%.

### Generate sniffer data

Generating sniffer data evaluates the observer against all user samples to generate observations. This task, despite
being parallelized in the original implementation, still takes prohibitively long. This is largely due to the fact that
the core computation of distance between observers and user devices happens in Python ——albeit understandably so since
the computation logic is not trivial to express with numpy operations.

| Task                  | Baseline | C#             | Rust           |
|-----------------------|----------|----------------|----------------|
| generate_sniffer_data | 679.62   | 10.48 (64.85x) | 3.70 (189.31x) |

### Intra-protocol mapping

Intra-protocol mapping involves two steps: first, to identify all pairs of traces that are temporally; then, each pair
is
evaluated to see if the traces associated with the ID pair are compatible, that is, the distance between all possible
combinations of points between the two traces do not exceed the fastest speed at which human can move (as defined by
`MAX_MOBILITY_FACTOR`).

Performance-wise, this task does most of the second step in numpy, and thus benefits greatly. However, the first step is
done in pure Python and is not optimised for parallel execution. The computation of the second part is done in
numpy and adapted for parallel processing. However, it could still benefit greatly from short-circuiting (i.e. since a
pair is considered incompatible as soon as at least one combination of samples is out of range, there is no need to
evaluate the remaining combinations).

We make a further observation that **it is more likely for the incompatibility to arise between two sniffer samples
that are temporally _separated_ than those _adjacent_**. Thus, we examine the combination of samples in the same order:
from two far ends of the sorted samples to two near ends.

Another key observation is that **it is not necessary to compute the compatibility of _all_ combination of points
between each pair of traces**. It is enough just to evaluate the compatibility for the potential transitional period
plus a maximum grace period of the length of transmission interval. This allows us to further trim down the number of
the number of combinations to evaluate, especially for LTE where each trace tends to contain many samples.

This trimming scheme has been verified across multiple pedestrian pool sizes to be correct. It also provides an
identical
TPR as the orginal implementation (i.e. how much of the trace pairs produced at the end are actually from the same
user).

| Task     | Baseline | C#             | Rust           | C# with trimming+reverse_order | Rust with trimming+reverse_order |
|----------|----------|----------------|----------------|--------------------------------|----------------------------------|
| intramap | 4866.67  | 8.77 (554.92x) | 7.15 (680.65x) | 4.83 (1007.59x)                | 2.99 (1627.45x)                  |

### Inter-protocol mapping

Inter-protocol mapping is largely symmetric with intra-protocol mapping. The main difference is that we filter
for pairs of traces that overlaps temporally instead of being immediately adjacent. We also apply the same trimming and
ordering scheme to reduce the number of combinations of trace points to evaluate in each candidate pair. Since the
overlapping
boundaries are no longer guaranteed to be reasonably close to the two ends of sorted sample arrays, we use binary
search here to locate the boundaries vis-à-vis the linear search used for intra-protocol mapping.

This trimming scheme has also been verified across multiple pedestrian pool sizes to be correct. This includes the TPR.

| Task     | Baseline | Rust            | Rust with trimming+reverse_order |
|----------|----------|-----------------|----------------------------------|
| intermap | 9499.16  | 18.35 (517.66x) | 5.73 (1657.79x)                  |
