import random
import string
import json

import sys

#
# CONSTANTS AND CONFIGURATION
#

# Area of capture dimension (in meters)
AREA_SIZE = 10

# Number of characters in identifier
IDENTIFIER_LENGTH = 12


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
        self.pause_time = random.uniform(1, 5)  # Random initial pause time
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
                self.pause_time = random.uniform(1, 5)
            return

        # Simulate random walk movement within a predefined area
        x = self.location[0] + random.uniform(-self.max_step_size, self.max_step_size)
        y = self.location[1] + random.uniform(-self.max_step_size, self.max_step_size)

        # Ensure user stays within predefined area (e.g., a city)
        x = max(min(x, AREA_SIZE), -AREA_SIZE)
        y = max(min(y, AREA_SIZE), -AREA_SIZE)

        self.location = (x, y)

        # Randomly pause after movement
        if random.random() < 0.3:
            self.is_paused = True

    def randomize_identifiers(self):
        self.identifier_counter += 1
        if self.identifier_counter % self.interval_ble == 0:
            print("Randomized ble")
            self.bluetooth_id = random_identifier()
        if self.identifier_counter % self.interval_wifi == 0:
            print("randomized wifi")
            self.wifi_id = random_identifier()
            # self.identifier_counter = 0
            # self.bluetooth_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
            # self.wifi_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
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

    def detect_devices(self, devices, timestep):

        for device in devices:
            for i in range(0, 3):

                distance = (
                    (self.location[0] - device[i].location[0]) ** 2
                    + (self.location[1] - device[i].location[1]) ** 2
                ) ** 0.5
                # print(distance)
                # print(isinstance(device[i], Bluetooth))
                if (
                    isinstance(device[i], Bluetooth)
                    and distance <= self.bluetooth_range
                ):
                    print("Bluetooth Device Detected:", device[i].device_id)
                    # self.detected_devices[device[i].device_id] = (device[i].location, timestep)
                    protocol = "Bluetooth"
                    s = str(timestep) + str(device[i].device_id)
                    sniffed_devices[s] = [
                        timestep,
                        protocol,
                        device[i].device_id,
                        device[i].location,
                    ]
                    detected_devices.append(
                        {
                            "timestep": timestep,
                            "protocol": protocol,
                            "bluetooth_id": device[i].device_id,
                            "location": device[i].location,
                        }
                    )
                    # print(detected_devices)
                elif isinstance(device[i], WiFi) and distance <= self.wifi_range:
                    print("WiFi Device Detected:", device[i].device_id)
                    # self.detected_devices[device[i].device_id] = (device[i].location, timestep)
                    protocol = "WiFi"
                    s = str(timestep) + str(device[i].device_id)
                    sniffed_devices[s] = [
                        timestep,
                        protocol,
                        device[i].device_id,
                        device[i].location,
                    ]
                    detected_devices.append(
                        {
                            "timestep": timestep,
                            "protocol": protocol,
                            "wifi_id": device[i].device_id,
                            "location": device[i].location,
                        }
                    )
                elif isinstance(device[i], LTE) and distance <= self.lte_range:
                    print("LTE Device Detected:", device[i].device_id)
                    # self.detected_devices[device[i].device_id] = (device[i].location, timestep)
                    protocol = "LTE"
                    s = str(timestep) + str(device[i].device_id)
                    sniffed_devices[s] = [
                        timestep,
                        protocol,
                        device[i].device_id,
                        device[i].location,
                    ]
                    detected_devices.append(
                        {
                            "timestep": timestep,
                            "protocol": protocol,
                            "lte_id": device[i].device_id,
                            "location": device[i].location,
                        }
                    )
                    # print(sniffed_devices)

    def detect_users(self, user, timestep):

        distance = (
            (self.location[0] - user.location[0]) ** 2
            + (self.location[1] - user.location[1]) ** 2
        ) ** 0.5
        if distance <= self.bluetooth_range:
            protocol = "Bluetooth"
            detected_users.append(
                {
                    "timestep": timestep,
                    "sniffer_id": self.id,
                    "sniffer_location": self.location,
                    "protocol": protocol,
                    "bluetooth_id": user.bluetooth_id,
                    "location": user.location,
                }
            )
        if distance <= self.wifi_range:
            protocol = "WiFi"
            detected_users.append(
                {
                    "timestep": timestep,
                    "sniffer_id": self.id,
                    "sniffer_location": self.location,
                    "protocol": protocol,
                    "WiFi_id": user.wifi_id,
                    "location": user.location,
                }
            )
        if distance <= self.lte_range:
            protocol = "LTE"
            detected_users.append(
                {
                    "timestep": timestep,
                    "sniffer_id": self.id,
                    "sniffer_location": self.location,
                    "protocol": protocol,
                    "lte_id": user.lte_id,
                    "location": user.location,
                }
            )


# Create some devices and users
bluetooth_device = Bluetooth((0, 0))
wifi_device = WiFi((0, 0))
lte_device = LTE("LTEDevice1", (0, 0))

users = []
devices = []


for i in range(num_users):
    user_id = "User{}".format(i + 1)
    bluetooth_id = random_identifier()
    wifi_id = random_identifier()
    lte_id = "LTEDevice{}".format(i + 1)
    location = (random.uniform(-AREA_SIZE, AREA_SIZE), random.uniform(-AREA_SIZE, AREA_SIZE))
    bluetooth_device = Bluetooth(location)
    wifi_device = WiFi(location)
    lte_device = LTE(lte_id, location)
    user = User(user_id, bluetooth_id, wifi_id, lte_id, location, max_step_size=0.5)
    users.append(user)
    devices.append((bluetooth_device, wifi_device, lte_device))


sniffers = []
for i in range(num_sniffer):
    sniffer_location = (random.uniform(-AREA_SIZE, AREA_SIZE), random.uniform(-AREA_SIZE, AREA_SIZE))
    sniffer = Sniffer(i, sniffer_location, bluetooth_range=2, wifi_range=3, lte_range=5)
    sniffers.append(sniffer)

# Simulate user movement and randomize identifiers
user_data = []
for timestep in range(500):
    for user in users:
        user.move()
        user.randomize_identifiers()
        bluetooth_device.update_location(user.location)
        wifi_device.update_location(user.location)
        lte_device.update_location(user.location)
        for sniffer in sniffers:
            sniffer.detect_devices(devices, timestep)
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

detect = []
# for item in detected_devices:
#     print(item)
#    print("aneet")
#   if item not in detect:
#      detect.append(item)


detect_user = []
for item in detected_users:
    print(item)
    if item not in detect_user:
        detect_user.append(item)


print(len(detect_user))
with open("user_data.json", "w") as f:
    json.dump(user_data, f)
# sniffed_data=list(set(sniffer.detected_devices))

with open("sniffed_data.json", "w") as f:
    json.dump(detect, f)

with open("sniffed_user.json", "w") as f:
    json.dump(detect_user, f)
