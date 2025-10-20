# Notes to the original README

## Setting up the environment

### Poetry vs venv

It might be easier altogether just to use venv to manage the dependencies especially given that there is currently no plan to publish this project as a ready-to-use library. To produce the regular `requirements.txt` for pip, run the following command. Note that the `export` command in poetry is provided by a dedicated plugin since version 2 and must be installed separately.

```shell
poetry export --without-hashes -o requirements.txt
```

### SUMO on Windows

Despite official support of SUMO for Windows, there still seems to be some dependency problem that prevents the normal loading of libsumo when used in a virtual environment. A quick investigation of import tables and Windows's internal log for calls to `LoadImage` revealed no immediate cause. As a workaround, install all dependencies to the system interpreter. On Windows, this requires no administrative privilege anyway and should just work.

### SUMO on Linux

The `requirements.txt` exported from the poetry config in the repository includes a SUMO redistributable from pip (`ellipse-sumo`, etc). However, this package contains only part of the dependencies for SUMO and consequently causes an import error when libsumo is imported in Python. To solve this, install SUMO also from the distribution's package manager. This should come with all the necessary dependencies.

### Run time measurement

The original script uses a rather hacky way of launching tasks with `subprocess.run` and with `time` to measure the task run time. Necessary patches are added to programmatically launch tasks and measure with Python's builtin `time` package. This also allows for easier IDE debugging and Windows compatibility.

## Procedure and tasks

Please note that unless otherwise specified, all runs in this chapter assumes the config file `scenario_test_32_sumo_new.yml` and is dispatched on a system with a Zen 3 processor@4GHz with 6 physical cores.

### Baseline

The following table gives the baseline measurement of run time for all required tasks for a successful round of attack. The most time-consuming tasks are marked in bold italic.

| Task name | Run time (second) |
|-----------|-------------------|
| **_sumo_**      | **_980.22_**            |
| **_filter_users_polygon_**          | **_349.09_**            |
| filter_users_RI_Count          | 23.14             |
| generate_user_data          | 21.68             |
| **_generate_sniffer_data_**          | **_679.62_**            |
| filter_sniffer_data          | 1.33              |
| aggregate          | 0.63              |
| **_intramap_optimized_**          | **_134.22_**            |
| **_intermap_optimized_**          | **_880.26_**            |
| refine_intramap          | 0.67              |
| intra_filter          | 0.48              |
| reconstruction_multi          | 5.91              |
| reconstruction_single          | 3.97              |
| plot          | 0.86              |


### SUMO

The `sumo` task is in charge of loading the predefined SUMO config files and running the actual simulation for pedestrians and vehicles. The speed of this task is bound by SUMO itself and there is not much room for improvement. SUMO also does not have stable support for parallel processing. As a result, this step usually takes more than 15 minutes.

The simulation also produces a ton of warning of pedestrians and/or vehicles getting jammed and/or having to be teleported elsewhere in the map. There might be some potential for optimisation here as per SUMO's documentation, constant jamming often slows down the simulation.

### Filter users by polygon

This tasks filters out users that are not within the area described by the given polygon. This step is the third most time-consuming tasks. Luckily, there is a clear opportunity for optimisation by parallel processing since there is no inter-data dependency, this can be done directly in Python. Further, despite using a native implementation of point-in-polygon algorithm, the frequent crossing of C-Python boundary incurs non-trivial interface cost (as opposed to big-and-bulky usages), this requires a re-implementation in potentially a pure-native language. Here we offer an example C# one.


| Task | Baseline | Python multiprocessing | C#   |
|----------|----------|--------------------------------|---------------|
| filter_users_polygon    | 349.09   | 124.44 (2.8x)   | 18.26 (19.4x) |


### Generate user data

It is unclear if it is also required to run the tasks `filter_users_polygon` and `filter_users_RI_count` after `sumo` is completed. However, the original simulation result produced by SUMO contains more than 35 million data points and takes multiple hours to process through user data generation. By contrast, `filter_users_RI_count` produces filtered result where data points for each simulation timestep is limited to a certain threshold. This greatly reduces the data volume (e.g., to ~3 million) and accelerates the data generation.

However, results generated by the `filter_users_RI_count` task also do not bear the expected filename of this task. It is necessary as of now to manually rename te desired filtered outputs (e.g., from `raw_user_data_scenario_test_32_sumo_new_32.csv` to `raw_user_data_scenario_test_32.csv`). It remains unclear why there exists no task that so generates. The original README suggested that the `sumo` task does this, but evidently is not the case.

Speed-wise, the script contains weird choices and antipatterns that largely crippled the performance. 

- Use of `deque` appears pointless. It can only be assumed that it was favoured over the simple list in the hope that appending never incurs array resizing and thus avoids unnecessary data copy. However, deque internally employs a linked list which has horrible data locality and sequential read performance, both of which negatively impacts the performance while the collected data is later iterated over to another data frame and to disk. Copying cost is also easily marginalised under high data volume.
- Converting loaded data frames into a dictionary is completely pointless and exacerbates memory waste.

Fixing the above reduced runtime by ~50%.

### Generate sniffer data

Generating sniffer data takes a long time.
