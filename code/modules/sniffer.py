from dataclasses import dataclass, field
from modules.user import User
from collections import deque
# from numba import jit

@dataclass
class Sniffer:
    id: int
    location: tuple
    bluetooth_range: int
    wifi_range: int
    lte_range: int
    detected_devices: list = field(default_factory=list)
    sniffed_devices: dict = field(default_factory=dict)

    def detect_users(self, user: User, timestep, detected_users: deque):
        distance = (
            (self.location[0] - user.location[0]) ** 2
            + (self.location[1] - user.location[1]) ** 2
        ) ** 0.5

        if distance <= self.bluetooth_range:
            detected_users.extend([
                {
                    "timestep": timestep,
                    "user_id": user.user_id,
                    "sniffer_id": self.id,
                    "sniffer_location": self.location,
                    "location": user.location,
                    "protocol": "Bluetooth",
                    "bluetooth_id": user.bluetooth_id,
                }]
            )

        if distance <= self.wifi_range:
            detected_users.extend([
                {
                    "timestep": timestep,
                    "user_id": user.user_id,
                    "sniffer_id": self.id,
                    "sniffer_location": self.location,
                    "location": user.location,
                    "protocol": "WiFi",
                    "WiFi_id": user.wifi_id,
                }]
            )

        if distance <= self.lte_range:
            detected_users.extend([
                {
                    "timestep": timestep,
                    "user_id": user.user_id,
                    "sniffer_id": self.id,
                    "sniffer_location": self.location,
                    "location": user.location,
                    "protocol": "LTE",
                    "lte_id": user.lte_id,
                }]
            )
        return detected_users
