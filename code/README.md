# CrossLink: Breaking Location Privacy by Linking Device Identifiers Across Protocols

---

Official Repository for the paper titled "CrossLink: Breaking Location Privacy by Linking Device Identifiers Across Protocols" 

![pipeline of the attack](design/design_arch.png)

Adversary can sniff the user data through multiple protocols like Bluetooth, WiFi, and LTE.  The sniffed data from all the sniffers would be sent to the tracking algorithm present at the backend. The sniffed data would consists of identifiers of all protocols and the probable distance between the sniffer and the measured user location. The adversary through the tracking algorithm would perform following steps:

1) Create inter-links of the identifiers from each sniffer based on the localization error and user mobility. (Maintain a list of not possible inter-linkages. Discard any linkages if linkages exists in not possible inter-linkages.)
2) Create intra-links of the identifiers based on if new identifiers of same protocol are present at the consecutive timestep. (Maintain a list of not possible intra-linkages. Discard any linkages if linkages exists in not possible intra-linkages.)
3) Refine the inter-linkages with help of intra-linkages and refine the intra-linkages with help of updated inter-linkages.
4) Store and utilize this linkage data for the next timesteps as the data is sent by the sniffer at every timestep.
5) Finally, reconstruct the user location traces after sometime to measure the privacy leakage of the users.

---

Here is a brief introduction to start with the code. 

## Hardware
Our code works on most of the hardware settings. However, for efficiency and speed, we recommend Core i7 CPUs and memory (Atleast 16GB+) and disk size of 100GB. We ran our code on 11th Gen Intel Core i7-1165G7 @2.80Ghz Processor. Overall memory of our system was 32Gb with operating system Ubuntu 22.04LTS and disk space of 2TB. The CPU Blowfish benchmarks scored 1.33.

## Package Dependency
The requirements for the code are listed in the ```pyproject.toml```. These requirements require poetry package to be installed. ```pip3 install poetry```.
Once the poetry tool is installed, the packages can be installed using ```poetry install``` command and then using ```poetry shell```, the temporary shell can be invoked to run the code.


## TODO before you start

1) Check the ```*.yml``` file which you make. This file contains the conigurations required for the simulation setup.

2) Install mongodb through the [official website](https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-ubuntu/).

3) Check if the mongodb service is enabled. For ubuntu, this can be checked via ```sudo systemctl status mongod```

4) For every scenarios configured through the yml file, the yml file name would become the database name where the respective collections would be added. 

5) The code consists of various scripts in the folders namely group, tracking, sumo, sanity, reconstruction. While these scripts could run individual by prescribing the environment variables, these scripts are stitched using the ```main.py``` and ```pipeline.py```. The ```main.py``` used **setuptools** to create various pipelines as showcased in ```pipeline.py```. For future purpose, more such pipeline functions can be added to ```pipeline.py```.

6) Code utilizes SuMO simulation package and the configurations used for the setup are located in the ```scenario``` folder at the root of the repository.


## Simulation Setup

To ensure our readers have an understand of the code, we will try to follow an example.

#### 1. Initialization

First we configure the ```project.yml``` file. All the below mentioned environment variables are part of this config file. This would be situated in the code folder of the repository. 

To understand the argument params, the command used would be:
```python3 main.py -h```

To know the pipelines for running the code, run the command
```python3 main.py -c project.yml -t help```

**(Ensure that the shell path is situated in the code folder and not in the root folder to run the code.)**.

#### 2. Data Generation Phase

The environment variables required are ```POLYGON_COORDS``` and ```USER_TIMESTEPS``` for running the sumo simulation code. Here the user movements data would generated.

This can be run with the command
```python3 main.py -c project.yml -t sumo```

With this command, the file with name ```raw_user_data_<config filename>.csv``` would be created.
Here for ```project.yml```, ```raw_user_data_project.csv``` file would be created in the ```data/``` folder.



To generate user data based on this obtained sumo simulation data, we require to configure following env variables: 