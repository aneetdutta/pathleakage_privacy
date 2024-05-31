from dataclasses import dataclass, field
from modules.user import User
from collections import deque
from math import sqrt
import uuid
from bson.objectid import ObjectId

@dataclass
class Sniffer:
    id: int
    location: tuple
    bluetooth_range: int
    wifi_range: int
    lte_range: int
    detected_devices: list = field(default_factory=list)
    sniffed_devices: dict = field(default_factory=dict)

    def detect_users(self, user: User, timestep):
        distance = sqrt(
            (float(self.location[0]) - float(user.location[0])) ** 2
            + (float(self.location[1]) - float(user.location[1])) ** 2
        )
        
        common_info = {
            "timestep": timestep,
            "user_id": user.user_id,
            "sniffer_id": self.id,
            "sniffer_location": self.location,
            "location": user.location,
        }

        # List of detected users
        detected_users = [None] * 3
        index = 0

        # if distance <= self.bluetooth_range:
        #     detected_users[index] = {
        #         **common_info,
        #         # "_id": ObjectId(),
        #         "protocol": "Bluetooth",
        #         "bluetooth_id": user.bluetooth_id,
        #     }
        #     index += 1

        if distance <= self.wifi_range:
            detected_users[index] = {
                **common_info,
                # "_id": ObjectId(),
                "protocol": "WiFi",
                "WiFi_id": user.wifi_id,
            }
            index += 1

        if distance <= self.lte_range:
            detected_users[index] = {
                **common_info,
                # "_id": ObjectId(),
                "protocol": "LTE",
                "lte_id": user.lte_id,
            }
            index += 1

        # Remove excess None values in the preallocated list
        return detected_users[:index]
    
    def detect_raw_users(self, user_id, timestep, user_location, user_lte_id = None, user_wifi_id=None, user_bluetooth_id = None):
        distance = sqrt(
            (float(self.location[0]) - float(user_location[0])) ** 2
            + (float(self.location[1]) - float(user_location[1])) ** 2
        )
        
        common_info = {
            "timestep": timestep,
            "user_id": user_id,
            "sniffer_id": self.id,
            "sniffer_location": self.location,
            "location": user_location,
        }

        # List of detected users
        detected_users = [None] * 3
        index = 0

        # if distance <= self.bluetooth_range:
        #     detected_users[index] = {
        #         **common_info,
        #         # "_id": ObjectId(),
        #         "protocol": "Bluetooth",
        #         "bluetooth_id": user_bluetooth_id,
        #     }
        #     index += 1

        if distance <= self.wifi_range:
            detected_users[index] = {
                **common_info,
                # "_id": ObjectId(),
                "protocol": "WiFi",
                "WiFi_id": user_wifi_id,
            }
            index += 1

        if distance <= self.lte_range:
            detected_users[index] = {
                **common_info,
                # "_id": ObjectId(),
                "protocol": "LTE",
                "lte_id": user_lte_id,
            }
            index += 1

        # Remove excess None values in the preallocated list
        return detected_users[:index]