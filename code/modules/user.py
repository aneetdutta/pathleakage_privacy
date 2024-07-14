# from env import *
import os
from random import uniform, randint, random
from services.general import random_identifier, str_to_bool

class User:
    def __init__(
        self, user_id, location, bluetooth_id, wifi_id, lte_id, mf, max_step_size=0.1
    ):
        self.user_id = user_id
        self.bluetooth_id = bluetooth_id
        self.wifi_id = wifi_id
        self.lte_id = lte_id
        
        self.temp_bluetooth_id = bluetooth_id
        self.temp_wifi_id = wifi_id
        self.temp_lte_id = lte_id
        
        self.location = location
        self.max_step_size = max_step_size
        self.mf = mf

        # self.pause_time = uniform(PAUSE_DURATION_MIN, PAUSE_DURATION_MAX)  # Random initial pause time
        # TODO: why do users start off paused?
        self.is_paused = True

        self.identifier_counter = 0
        
        self.transmit_bluetooth = True
        self.transmit_wifi = True
        self.transmit_lte = True
        
        self.next_bluetooth_transmit = 0
        self.next_wifi_transmit = 0
        self.next_lte_transmit = 0
        
        self.next_bluetooth_refresh = 0
        self.next_wifi_refresh = 0
        self.next_lte_refresh = 0
        
        self.next_protocol_refresh = 0
        
        self.randomized_bluetooth = False
        self.randomized_wifi = False
        self.randomized_lte = False
    
        self.BLUETOOTH_MIN_TRANSMIT = float(os.getenv("BLUETOOTH_MIN_TRANSMIT"))
        self.BLUETOOTH_MAX_TRANSMIT = float(os.getenv("BLUETOOTH_MAX_TRANSMIT"))
        self.WIFI_MIN_TRANSMIT = float(os.getenv("WIFI_MIN_TRANSMIT"))
        self.WIFI_MAX_TRANSMIT = float(os.getenv("WIFI_MAX_TRANSMIT"))
        self.LTE_MIN_TRANSMIT = float(os.getenv("LTE_MIN_TRANSMIT"))
        self.LTE_MAX_TRANSMIT = float(os.getenv("LTE_MAX_TRANSMIT"))
        self.BLUETOOTH_MIN_REFRESH = float(os.getenv("BLUETOOTH_MIN_REFRESH"))
        self.BLUETOOTH_MAX_REFRESH = float(os.getenv("BLUETOOTH_MAX_REFRESH"))
        self.WIFI_MIN_REFRESH = float(os.getenv("WIFI_MIN_REFRESH"))
        self.WIFI_MAX_REFRESH = float(os.getenv("WIFI_MAX_REFRESH"))
        self.LTE_MIN_REFRESH = float(os.getenv("LTE_MIN_REFRESH"))
        self.LTE_MAX_REFRESH = float(os.getenv("LTE_MAX_REFRESH"))
        
        
        self.ENABLE_SYNCED_RANDOMIZATION = str_to_bool(os.getenv("ENABLE_SYNCED_RANDOMIZATION", "false"))
        self.PROTOCOL_MIN_REFRESH = float(os.getenv("PROTOCOL_MIN_REFRESH", 0))
        self.PROTOCOL_MAX_REFRESH = float(os.getenv("PROTOCOL_MAX_REFRESH", 0))
        
        # print(self.PROTOCOL_MIN_REFRESH)
        # print(self.PROTOCOL_MAX_REFRESH)
        
        if not self.ENABLE_SYNCED_RANDOMIZATION:
            self.set_next_bluetooth_refresh()
            self.set_next_wifi_refresh()
            self.set_next_lte_refresh()
        else:
            self.set_next_protocol_refresh()
        
    def set_next_bluetooth_transmit(self):
        duration = round(uniform(self.BLUETOOTH_MIN_TRANSMIT, self.BLUETOOTH_MAX_TRANSMIT) / 0.25) * 0.25
        self.next_bluetooth_transmit = self.identifier_counter + duration

    def set_next_wifi_transmit(self):
        duration = round(uniform(self.WIFI_MIN_TRANSMIT, self.WIFI_MAX_TRANSMIT) / 0.25) * 0.25
        self.next_wifi_transmit = self.identifier_counter + duration

    def set_next_lte_transmit(self):
        duration = round(uniform(self.LTE_MIN_TRANSMIT, self.LTE_MAX_TRANSMIT) / 0.25) * 0.25
        self.next_lte_transmit = self.identifier_counter + duration

    def set_next_bluetooth_refresh(self):
        duration = randint(self.BLUETOOTH_MIN_REFRESH, self.BLUETOOTH_MAX_REFRESH)
        self.next_bluetooth_refresh = self.identifier_counter + duration

    def set_next_protocol_refresh(self):
        duration = randint(self.PROTOCOL_MIN_REFRESH, self.PROTOCOL_MAX_REFRESH)
        self.next_protocol_refresh = self.identifier_counter + duration
        
    def set_next_wifi_refresh(self):
        duration = randint(self.WIFI_MIN_REFRESH, self.WIFI_MAX_REFRESH)
        self.next_wifi_refresh = self.identifier_counter + duration

    def set_next_lte_refresh(self):
        # print(self.LTE_MIN_REFRESH, self.LTE_MAX_REFRESH)
        duration = randint(self.LTE_MIN_REFRESH, self.LTE_MAX_REFRESH)
        self.next_lte_refresh = self.identifier_counter + duration

    def randomize_identifiers(self):
        self.identifier_counter += 1

        if self.ENABLE_SYNCED_RANDOMIZATION:
            if self.identifier_counter >= self.next_protocol_refresh:
                # print("Randomized ble")
                self.set_next_protocol_refresh()
                self.temp_bluetooth_id = random_identifier()
                self.temp_lte_id = random_identifier()
                self.temp_wifi_id = random_identifier()
                self.randomized_bluetooth = True
                self.randomized_wifi = True
                self.randomized_lte = True
            else:
                self.randomized_bluetooth = False
                self.randomized_wifi = False
                self.randomized_lte = False
                
            return
                
        if self.identifier_counter >= self.next_bluetooth_refresh:
            # print("Randomized ble")
            self.set_next_bluetooth_refresh()
            self.temp_bluetooth_id = random_identifier()
            self.randomized_bluetooth = True
        else:
            self.randomized_bluetooth = False

        if self.identifier_counter >= self.next_wifi_refresh:
            # print("randomized wifi")
            self.set_next_wifi_refresh()
            self.temp_wifi_id = random_identifier()
            self.randomized_wifi = True
        else:
            self.randomized_wifi = False

        if self.identifier_counter >= self.next_lte_refresh:
            # print("randomized lte")
            self.set_next_lte_refresh()
            self.temp_lte_id = random_identifier()
            self.randomized_lte = True
        else:
            self.randomized_lte = False
            
    def transmit_identifiers(self):
        ''' since identifier count is increased in randomize identifiers, not increasing during transmit '''

        if self.identifier_counter >= self.next_bluetooth_transmit or self.randomized_bluetooth == True:
            self.set_next_bluetooth_transmit()
            self.bluetooth_id = self.temp_bluetooth_id
            self.transmit_bluetooth = True
        else:
            self.bluetooth_id = None
            self.transmit_bluetooth = False
            
        if self.identifier_counter >= self.next_wifi_transmit or self.randomized_wifi == True:
            self.set_next_wifi_transmit()
            self.wifi_id = self.temp_wifi_id
            self.transmit_wifi = True
        else:
            self.wifi_id = None
            self.transmit_wifi = False

        if self.identifier_counter >= self.next_lte_transmit or self.randomized_lte == True:
            self.set_next_lte_transmit()
            self.lte_id = self.temp_lte_id
            self.transmit_lte = True
        else:
            self.lte_id = None
            self.transmit_lte = False
