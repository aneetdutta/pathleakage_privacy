## Simulation Experiment


### Code Flow
The following is the structure of the code.

#### 1. Sumo Simulation

- Run the sumo simulation (sumo_simulation.py) in order to generate the data corresponding to the required environment variables
This creates 2 json files
     - sniffed_data.json (user data captured by the sniffer)
     - user_data.json (user data)

     Add these two files to mongodb under the database named "code"

#### 2. Grouping

- Run the aggregation.py and group.py to generate the groups. These groups are stored in mongodb under the collection "groups". Same database is used.

- test_group.py file can be used to create test cases to test the grouping_algorithm

#### 3. Tracking

- Run tracking.py to find the linkability between the identifiers. The code saves the jsons obtained every timestep to the mongodb.

More to be written soon