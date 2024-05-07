import os
import sys
import traci
import csv
import random
import string
import json
from datetime import datetime
import sys


#Area of capture dimension (in meters)
AREA_SIZE = 500

# Duration of the simulation (in seconds)
DURATION_SIMULATION = 7200

# Number of characters in identifier
IDENTIFIER_LENGTH = 12

config_elements={'area_size':AREA_SIZE,'duration_simulation':DURATION_SIMULATION,'identifier_length':IDENTIFIER_LENGTH}

#-------------------------#
#   Movement Parameters   #
#-------------------------#

# Step size
MAX_STEP_SIZE = 2

PROBABILITY_PAUSE = 0.3
PAUSE_DURATION_MIN = 1
PAUSE_DURATION_MAX = 5

#-------------------------#
#    Refresh Intervals    #
#-------------------------#

# Next refresh is always drawn from the intervals specified below

# Bluetooth IDs refresh range uniform (in s)
BLUETOOTH_MIN_REFRESH = 10*60 
BLUETOOTH_MAX_REFRESH = 45*60

# WifI ID refresh range uniform (in s)
WIFI_MIN_REFRESH = 20*60
WIFI_MAX_REFRESH = 55*60

# LTE refresh range uniform (in s)
LTE_MIN_REFRESH =  10
LTE_MAX_REFRESH =  60

#Range for communication protocols
bluetooth_range=10
wifi_range=30
lte_range=100





# Start SUMO as a subprocess
SUMO_BIN_PATH = "/usr/bin/"

sumo_binary = "sumo"
SUMO_CFG_FILE = "most.sumocfg"

#sumo_cmd = [sumo_binary, "-c", "most.sumocfg"]
#sumo_process = subprocess.Popen(sumo_cmd, stdout=sys.stdout, stderr=sys.stderr)

sumo_cmd = [os.path.join(SUMO_BIN_PATH, "sumo"), "-c", SUMO_CFG_FILE]

traci.start(sumo_cmd)
# Connect to TraCI
#traci.connect()

# Open CSV file for writing
#csv_file = open("person_locations.csv", "w", newline='')
#csv_writer = csv.writer(csv_file)
#csv_writer.writerow(["Timestep", "PersonID", "X", "Y"])

def random_identifier():
    device_id = "".join(
        random.choices(string.ascii_uppercase + string.digits, k=IDENTIFIER_LENGTH)
    )
    return device_id


class User:
    def __init__(
        self, user_id, bluetooth_id, wifi_id, lte_id, location, max_step_size=0.1
    ):
        self.user_id = user_id
        self.bluetooth_id = bluetooth_id
        self.wifi_id = wifi_id
        self.lte_id = lte_id
        self.location = location
        self.max_step_size = max_step_size

        self.pause_time = random.uniform(PAUSE_DURATION_MIN, PAUSE_DURATION_MAX)  # Random initial pause time
        # TODO: why do users start off paused?
        self.is_paused = True

        self.identifier_counter = 0
        self.set_next_bluetooth_refresh()
        self.set_next_wifi_refresh()
        self.set_next_lte_refresh()

    def set_next_bluetooth_refresh(self):
        duration = random.randint(BLUETOOTH_MIN_REFRESH, BLUETOOTH_MAX_REFRESH)
        self.next_bluetooth_refresh = self.identifier_counter + duration

    def set_next_wifi_refresh(self):
        duration = random.randint(WIFI_MIN_REFRESH, WIFI_MAX_REFRESH)
        self.next_wifi_refresh = self.identifier_counter + duration

    def set_next_lte_refresh(self):
        duration = random.randint(LTE_MIN_REFRESH, LTE_MAX_REFRESH)
        self.next_lte_refresh = self.identifier_counter + duration

    def move(self):
        if self.is_paused:
            self.pause_time -= 1
            if self.pause_time <= 0:
                self.is_paused = False
                self.pause_time = random.uniform(PAUSE_DURATION_MAX, PAUSE_DURATION_MAX)
            return

        # Simulate random walk movement within a predefined area
        x = self.location[0] + random.uniform(-self.max_step_size, self.max_step_size)
        y = self.location[1] + random.uniform(-self.max_step_size, self.max_step_size)

        # Ensure user stays within predefined area (e.g., a city)
        x = max(min(x, AREA_SIZE), -AREA_SIZE)
        y = max(min(y, AREA_SIZE), -AREA_SIZE)

        self.location = (x, y)

        # Randomly pause after movement
        if random.random() < PROBABILITY_PAUSE:
            self.is_paused = True

    def randomize_identifiers(self):
        self.identifier_counter += 1

        if self.identifier_counter >= self.next_bluetooth_refresh:
            print("Randomized ble")
            self.set_next_bluetooth_refresh()
            self.bluetooth_id = random_identifier()

        if self.identifier_counter >= self.next_wifi_refresh:
            print("randomized wifi")
            self.set_next_wifi_refresh()
            self.wifi_id = random_identifier()

        if self.identifier_counter >= self.next_lte_refresh:
            print("randomized lte")
            self.set_next_lte_refresh()
            self.lte_id = random_identifier()






class Sniffer:
    def __init__(
        self, sniffer_identifier, location, bluetooth_range, wifi_range, lte_range
    ):
        self.id = sniffer_identifier
        self.location = location
        self.bluetooth_range = bluetooth_range
        self.wifi_range = wifi_range
        self.lte_range = lte_range
        self.detected_devices = []
        # self.sniffed_devices={}

    def detect_users(self, user, timestep):
        distance = (
            (self.location[0] - user.location[0]) ** 2
            + (self.location[1] - user.location[1]) ** 2
        ) ** 0.5

        #record = {
         #   "timestep": timestep,
          #  "sniffer_id": self.id,
          #  "sniffer_location": self.location,
          #  "location": user.location,
       # }

        if distance <= self.bluetooth_range:
            record={
                    "timestep": timestep,
                    "user_id": user.user_id,
                    "sniffer_id": self.id,
                    "sniffer_location": self.location,
                    "location": user.location,
 
                    "protocol": "Bluetooth",
                    "bluetooth_id": user.bluetooth_id,
                
            }
            detected_users.append(record)

        if distance <= self.wifi_range:
            record={
                    "timestep": timestep,
                    "user_id": user.user_id,
                    "sniffer_id": self.id,
                    "sniffer_location": self.location,
                    "location": user.location,

                    "protocol": "WiFi",
                    "WiFi_id": user.wifi_id,
                 
            }

            detected_users.append(record)

        if distance <= self.lte_range:
            record={
                    "timestep": timestep,
                    "user_id": user.user_id,
                    "sniffer_id": self.id,
                    "sniffer_location": self.location,
                    "location": user.location,

                    "protocol": "LTE",
                    "lte_id": user.lte_id,
                 
            }

            detected_users.append(record)








try:
    # Simulation loop
    detected_users=[]
    user_data=[]
    users=[]
    sniffers=[]
    timestep=14400
    sniffer_locs=[(9832.86,5109.03),(3075.86,686.18),(4749.59,1973.95),(5053.60,2440.58),(4106.14,1580.96),(5022.89,2397.47),(2447.68,335.84),(1541.62,594.71),(2333.54,663.48),(4823.42,2244.27),(8251.47,4557.67),(5085.25,2361.61)]
    for i in range(len(sniffer_locs)):
        sniffer_location=sniffer_locs[i]
        sniffer = Sniffer(i, sniffer_location, bluetooth_range, wifi_range, lte_range)
        sniffers.append(sniffer)
    while(timestep<19400):
        #print(i)
        # Get current simulation time
        timestep = traci.simulation.getTime()
        print(timestep)
        # Get list of person IDs
        person_ids = traci.person.getIDList()
        
        # Iterate over each person ID
        for person_id in person_ids:
            # Get person's position
            user_exists = next((user for user in users if user.user_id == 1), None)
            if user_exists:
                 user_exists.location=traci.person.getPosition(person_id)
                 user_exists.randomize_identifiers()
                 for sniffer in sniffers:
                      sniffer.detect_users(user_exists, timestep)
                 user_data.append(
                 {
                     "timestep": timestep,
                     "user_id": user_exists.user_id,
                     "location": user_exists.location,
                     "bluetooth_id": user_exists.bluetooth_id,
                     "wifi_id": user_exists.wifi_id,
                     "lte_id": user_exists.lte_id,
                 }
                 )
            else:
                 user_id=person_id
                 location=traci.person.getPosition(person_id)
                 bluetooth_id = random_identifier()
                 wifi_id = random_identifier()
                 lte_id = random_identifier()
                 user = User(user_id, bluetooth_id, wifi_id, lte_id, location, max_step_size=MAX_STEP_SIZE)
                 users.append(user)
                 for sniffer in sniffers:
                     sniffer.detect_users(user,timestep)
           
                 user_data.append(
                 {
                     "timestep": timestep,
                     "user_id": user.user_id,
                     "location": user.location,
                     "bluetooth_id": user.bluetooth_id,
                     "wifi_id": user.wifi_id,
                     "lte_id": user.lte_id,
                 }
                 )
            # Write data to CSV
            #csv_writer.writerow([timestep, person_id, x, y])
        
        # Advance simulation
        traci.simulationStep()
        
    # Clean up
    traci.close()
    #csv_file.close()
    #sys.exit()

except Exception as e:
    print("Error:", e)
    traci.close()
    #csv_file.close()
    sys.exit(1)


timestamp=datetime.now().strftime("%Y%m%d%H%M%S")
user_file = f"{timestamp}_user_data.json"


with open(user_file, "w") as f:
    json.dump(user_data, f)

sniffed_file=f"{timestamp}_sniffed_data.json"

with open(sniffed_file, "w") as f:
    json.dump(detected_users, f)
  

