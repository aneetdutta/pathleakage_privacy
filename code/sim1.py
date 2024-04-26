import random
import string
import json

import sys

###############################
# CONSTANTS AND CONFIGURATION #
###############################

# Area of capture dimension (in meters)
AREA_SIZE = 10

# Duration of the simulation (in seconds)
DURATION_SIMULATION = 500

# Number of characters in identifier
IDENTIFIER_LENGTH = 12

#-------------------------#
#   Movement Parameters   #
#-------------------------#

# Step size
MAX_STEP_SIZE = 0.5

PROBABILITY_PAUSE = 0.3
PAUSE_DURATION_MIN = 1
PAUSE_DURATION_MAX = 5


# Utility functions
def random_identifier():
    device_id = "".join(
        random.choices(string.ascii_uppercase + string.digits, k=IDENTIFIER_LENGTH)
    )
    return device_id


# Get the number of users from command line argument
if len(sys.argv) < 3:
    print("Usage: python script_name.py <number_of_users> <number_of_sniffers>")
    sys.exit(1)

try:
    num_users = int(sys.argv[1])
    num_sniffer = int(sys.argv[2])
except ValueError:
    print("Number of users must be an integer.")
    sys.exit(1)


class Device:
    def __init__(self, device_id, location):
        self.device_id = device_id
        self.location = location

    def update_location(self, new_location):
        self.location = new_location

    def __repr__(self):
        return f"[{self.__class__.__name__}: id={self.device_id}, loc={self.location}]"


class Bluetooth(Device):
    def __init__(self, location):
        device_id = random_identifier()
        super().__init__(device_id, location)


class WiFi(Device):
    def __init__(self, location):
        device_id = random_identifier()
        super().__init__(device_id, location)


class LTE(Device):
    def __init__(self, device_id, location):
        super().__init__(device_id, location)


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
        self.interval_ble = random.randint(1, 10)
        self.interval_wifi = random.randint(5, 50)
        self.interval_lte = random.randint(5, 15)

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

        if self.identifier_counter % self.interval_ble == 0:
            print("Randomized ble")
            self.bluetooth_id = random_identifier()

        if self.identifier_counter % self.interval_wifi == 0:
            print("randomized wifi")
            self.wifi_id = random_identifier()

        if self.identifier_counter % self.interval_lte == 0:
            print("randomized lte")
            self.lte_id = random_identifier()
            print(self.lte_id)


sniffed_devices = {}
detected_devices = []
detected_users = []


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

        record = {
            "timestep": timestep,
            "sniffer_id": self.id,
            "sniffer_location": self.location,
            "location": user.location,
        }

        if distance <= self.bluetooth_range:
            record.update(
                {
                    "protocol": "Bluetooth",
                    "bluetooth_id": user.bluetooth_id,
                }
            )
            detected_users.append(record)

        if distance <= self.wifi_range:
            record.update(
                {
                    "protocol": "WiFi",
                    "WiFi_id": user.wifi_id,
                }
            )
            detected_users.append(record)

        if distance <= self.lte_range:
            record.update(
                {
                    "protocol": "LTE",
                    "lte_id": user.lte_id,
                }
            )
            detected_users.append(record)


# Create users users
users = []
for i in range(num_users):
    user_id = "User{}".format(i + 1)

    bluetooth_id = random_identifier()
    wifi_id = random_identifier()
    lte_id = "LTEDevice{}".format(i + 1)

    # Pick a random initial location for the user
    location = (
        random.uniform(-AREA_SIZE, AREA_SIZE),
        random.uniform(-AREA_SIZE, AREA_SIZE),
    )

    user = User(
        user_id, bluetooth_id, wifi_id, lte_id, location, max_step_size=MAX_STEP_SIZE
    )
    users.append(user)


# Create sniffers
sniffers = []
for i in range(num_sniffer):
    # Pick a random location for the sniffer within the space
    sniffer_location = (
        random.uniform(-AREA_SIZE, AREA_SIZE),
        random.uniform(-AREA_SIZE, AREA_SIZE),
    )
    sniffer = Sniffer(i, sniffer_location, bluetooth_range=2, wifi_range=3, lte_range=5)
    sniffers.append(sniffer)


# Simulate user movement and randomize identifiers
user_data = []
for timestep in range(DURATION_SIMULATION):
    for user in users:
        user.move()
        user.randomize_identifiers()

        for sniffer in sniffers:
            sniffer.detect_users(user, timestep)

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
        print("---")

# Print locations of all users
# for user in users:
# print("User {} Location: {}".format(user.user_id, user.location))

# print(sniffer.detected_devices.items())
# print(detected_devices)
# Print detected devices with locations and timesteps
print("Detected Devices:")


detect_user = []
for item in detected_users:
    print(item)
    if item not in detect_user:
        detect_user.append(item)

print(len(detect_user))
with open("user_data.json", "w") as f:
    json.dump(user_data, f)
# sniffed_data=list(set(sniffer.detected_devices))

with open("sniffed_user.json", "w") as f:
    json.dump(detect_user, f)
