from dataclasses import dataclass

@dataclass
class Device:
    bluetooth_id: str
    wifi_id: str
    lte_id: str