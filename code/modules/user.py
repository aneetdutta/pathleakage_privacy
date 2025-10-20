# from env import *
import os
from random import uniform, randint, random
from modules.general import random_identifier, str_to_bool
import numpy as np
import math

class User:
    def __init__(
        self, user_id, location, bluetooth_id, wifi_id, lte_id, max_step_size=0.1
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
        # self.mf = mf

        # self.pause_time = uniform(PAUSE_DURATION_MIN, PAUSE_DURATION_MAX)  # Random initial pause time
        # TODO: why do users start off paused?
        self.is_paused = True

        self.identifier_counter = 0
        
        self.lte_counter = 0
        
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
        self.randomized = False
    
        # these clearly should be int
        self.BLUETOOTH_MIN_TRANSMIT = int(os.getenv("BLUETOOTH_MIN_TRANSMIT"))
        self.BLUETOOTH_MAX_TRANSMIT = int(os.getenv("BLUETOOTH_MAX_TRANSMIT"))
        self.WIFI_MIN_TRANSMIT = int(os.getenv("WIFI_MIN_TRANSMIT"))
        self.WIFI_MAX_TRANSMIT = int(os.getenv("WIFI_MAX_TRANSMIT"))
        self.LTE_MIN_TRANSMIT = int(os.getenv("LTE_MIN_TRANSMIT"))
        self.LTE_MAX_TRANSMIT = int(os.getenv("LTE_MAX_TRANSMIT"))
        self.BLUETOOTH_MIN_REFRESH = int(os.getenv("BLUETOOTH_MIN_REFRESH"))
        self.BLUETOOTH_MAX_REFRESH = int(os.getenv("BLUETOOTH_MAX_REFRESH"))
        self.WIFI_MIN_REFRESH = int(os.getenv("WIFI_MIN_REFRESH"))
        self.WIFI_MAX_REFRESH = int(os.getenv("WIFI_MAX_REFRESH"))
        self.LTE_MIN_REFRESH = int(os.getenv("LTE_MIN_REFRESH"))
        self.LTE_MAX_REFRESH = int(os.getenv("LTE_MAX_REFRESH"))
        self.ID_RANDOMIZATION = os.getenv("ID_RANDOMIZATION")
        
        
        self.ENABLE_SYNCED_RANDOMIZATION = str_to_bool(os.getenv("ENABLE_SYNCED_RANDOMIZATION", "false"))
        self.ENABLE_LTE_RANDOMIZATION = str_to_bool(os.getenv("ENABLE_LTE_RANDOMIZATION", "false"))
        self.PROTOCOL_MIN_REFRESH = float(os.getenv("PROTOCOL_MIN_REFRESH", 0))
        self.PROTOCOL_MAX_REFRESH = float(os.getenv("PROTOCOL_MAX_REFRESH", 0))
        
        self.TRANSMIT_WHEN_RANDOMIZED = str_to_bool(os.getenv("TRANSMIT_WHEN_RANDOMIZED", "true"))
        # print(self.TRANSMIT_WHEN_RANDOMIZED)
        
        # print(self.PROTOCOL_MIN_REFRESH)
        # print(self.PROTOCOL_MAX_REFRESH)
        
        if not self.ENABLE_SYNCED_RANDOMIZATION:
            self.set_next_bluetooth_refresh()
            self.set_next_wifi_refresh()
            self.set_next_lte_refresh()
        else:
            self.set_next_protocol_refresh()
        
    def set_next_bluetooth_transmit(self):
        # rate_parameter = np.random.uniform(low=self.BLUETOOTH_MIN_TRANSMIT, high=self.BLUETOOTH_MAX_TRANSMIT, size=1)
        # duration = math.ceil(np.random.exponential(scale=1/rate_parameter))
        duration = round(uniform(self.BLUETOOTH_MIN_TRANSMIT, self.BLUETOOTH_MAX_TRANSMIT))
        # duration=round(np.random.exponential(self.BLUETOOTH_MAX_TRANSMIT))
        self.next_bluetooth_transmit = self.identifier_counter + duration

    def set_next_wifi_transmit(self):
        # rate_parameter = np.random.uniform(low=self.WIFI_MIN_TRANSMIT, high=self.WIFI_MAX_TRANSMIT, size=1)
        # duration = math.ceil(np.random.exponential(scale=1/rate_parameter))       
        duration = round(uniform(self.WIFI_MIN_TRANSMIT, self.WIFI_MAX_TRANSMIT))
        #duration=round(np.random.exponential(self.WIFI_MAX_TRANSMIT))
        self.next_wifi_transmit = self.identifier_counter + duration

    def set_next_lte_transmit(self):
        # rate_parameter = np.random.uniform(low=self.LTE_MIN_TRANSMIT, high=self.LTE_MAX_TRANSMIT, size=1)
        # duration = math.ceil(np.random.exponential(scale=rate_parameter))
        # print(self.user_id, duration, rate_parameter)
        duration = round(uniform(self.LTE_MIN_TRANSMIT, self.LTE_MAX_TRANSMIT))
        #duration=round(np.random.exponential(self.LTE_MAX_TRANSMIT))
        if self.ENABLE_LTE_RANDOMIZATION:
            self.next_lte_transmit = self.lte_counter + duration
        else:
            self.next_lte_transmit = self.identifier_counter + duration

    def set_next_bluetooth_refresh(self):
        if self.ID_RANDOMIZATION == "exponential":
            rate_parameter = np.random.uniform(low=self.BLUETOOTH_MIN_REFRESH, high=self.BLUETOOTH_MAX_REFRESH, size=1)
            duration = math.ceil(np.random.exponential(scale=rate_parameter))
        elif self.ID_RANDOMIZATION == "uniform":
            duration = round(np.random.uniform(low=self.BLUETOOTH_MIN_REFRESH, high=self.BLUETOOTH_MAX_REFRESH))
        else:
            # Follow random
            # who the fuck feeds float type into randint?
            duration = randint(self.BLUETOOTH_MIN_REFRESH, self.BLUETOOTH_MAX_REFRESH)

        self.next_bluetooth_refresh = self.identifier_counter + duration

    def set_next_protocol_refresh(self):
        if self.ID_RANDOMIZATION == "exponential":
            rate_parameter = np.random.uniform(low=self.PROTOCOL_MIN_REFRESH, high=self.PROTOCOL_MAX_REFRESH, size=1)
            duration = math.ceil(np.random.exponential(scale=rate_parameter))
        elif self.ID_RANDOMIZATION == "uniform":
            duration = round(np.random.uniform(low=self.PROTOCOL_MIN_REFRESH, high=self.PROTOCOL_MAX_REFRESH))
        else:
            # Follow random
            duration = randint(self.PROTOCOL_MIN_REFRESH, self.PROTOCOL_MAX_REFRESH)
            
        rate_parameter = np.random.uniform(low=self.PROTOCOL_MIN_REFRESH, high=self.PROTOCOL_MAX_REFRESH, size=1)
        
        self.next_protocol_refresh = self.identifier_counter + duration
        
    def set_next_wifi_refresh(self):
        if self.ID_RANDOMIZATION == "exponential":
            rate_parameter = np.random.uniform(low=self.WIFI_MIN_REFRESH, high=self.WIFI_MAX_REFRESH, size=1)
            duration = math.ceil(np.random.exponential(scale=rate_parameter))
        elif self.ID_RANDOMIZATION == "uniform":
            duration = round(np.random.uniform(low=self.WIFI_MIN_REFRESH, high=self.WIFI_MAX_REFRESH))
        else:
            # Follow random
            duration = randint(self.WIFI_MIN_REFRESH, self.WIFI_MAX_REFRESH)
            
        self.next_wifi_refresh = self.identifier_counter + duration

    def set_next_lte_refresh(self):
        if self.ID_RANDOMIZATION == "exponential":
            rate_parameter = np.random.uniform(low=self.LTE_MIN_REFRESH, high=self.LTE_MAX_REFRESH, size=1)
            duration = math.ceil(np.random.exponential(scale=rate_parameter))
        elif self.ID_RANDOMIZATION == "uniform":
            duration = round(np.random.uniform(low=self.LTE_MIN_REFRESH, high=self.LTE_MAX_REFRESH))
        else:
            # Follow random
            duration = randint(self.LTE_MIN_REFRESH, self.LTE_MAX_REFRESH)
            
        if self.ENABLE_LTE_RANDOMIZATION:
            self.next_lte_refresh = self.lte_counter + duration
        else:
            self.next_lte_refresh = self.identifier_counter + duration
            

    def randomize_identifiers(self, reset_timers = False):    
        self.identifier_counter += 1
        if self.ENABLE_SYNCED_RANDOMIZATION:
            if reset_timers:
                self.identifier_counter = 0
                self.set_next_protocol_refresh()
                self.temp_bluetooth_id = f"{self.user_id}_B_{random_identifier()}"
                print("Is random_identifier a function?", callable(random_identifier))
                self.temp_lte_id = f"{self.user_id}_L_{random_identifier()}"
                self.temp_wifi_id = f"{self.user_id}_W_{random_identifier()}"
                self.randomized = True
                self.randomized_bluetooth = True
                self.randomized_wifi = True
                self.randomized_lte = True
            else:
                if self.identifier_counter >= self.next_protocol_refresh:
                    self.set_next_protocol_refresh()
                    self.temp_bluetooth_id = f"{self.user_id}_B_{random_identifier()}"
                    self.temp_lte_id = f"{self.user_id}_L_{random_identifier()}"
                    self.temp_wifi_id = f"{self.user_id}_W_{random_identifier()}"
                    self.randomized = True
                    self.randomized_bluetooth = True
                    self.randomized_wifi = True
                    self.randomized_lte = True
                else:
                    self.randomized_bluetooth = False
                    self.randomized_wifi = False
                    self.randomized_lte = False
                    self.randomized = False
            return
            
        
        if self.identifier_counter >= self.next_bluetooth_refresh:
            # print("Randomized ble")
            self.set_next_bluetooth_refresh()
            self.temp_bluetooth_id = f"{self.user_id}_B_{random_identifier()}"
            self.randomized_bluetooth = True
        else:
            self.randomized_bluetooth = False

        if self.identifier_counter >= self.next_wifi_refresh:
            # print("randomized wifi")
            self.set_next_wifi_refresh()
            self.temp_wifi_id = f"{self.user_id}_W_{random_identifier()}"
            self.randomized_wifi = True
        else:
            self.randomized_wifi = False
            
        if self.ENABLE_LTE_RANDOMIZATION:
            self.lte_counter += 1
            if reset_timers:
                self.lte_counter = 0
                self.randomized = True
                self.set_next_lte_refresh()
                self.temp_lte_id = f"{self.user_id}_L_{random_identifier()}"
                self.randomized_lte = True
            else:
                if self.lte_counter >= self.next_lte_refresh:
                    # print("randomized lte")
                    self.set_next_lte_refresh()
                    self.randomized = True
                    self.temp_lte_id = f"{self.user_id}_L_{random_identifier()}"
                    self.randomized_lte = True
                else:
                    self.randomized = False
                    self.randomized_lte = False
        else:
            if self.identifier_counter >= self.next_lte_refresh:
                # print("randomized lte")
                self.set_next_lte_refresh()
                self.temp_lte_id = f"{self.user_id}_L_{random_identifier()}"
                self.randomized_lte = True
            else:
                self.randomized_lte = False
            
            
    def transmit_identifiers_force(self):
        self.transmit_bluetooth = True
        self.transmit_wifi = True
        self.transmit_lte = True
        self.randomized_bluetooth = False
        self.randomized_wifi = False
        self.randomized_lte = False
        self.bluetooth_id = self.temp_bluetooth_id
        self.wifi_id = self.temp_wifi_id
        self.lte_id = self.temp_lte_id
        
        
    def transmit_identifiers(self):
            
        ''' since identifier count is increased in randomize identifiers, not increasing during transmit '''

        if self.identifier_counter >= self.next_bluetooth_transmit or (self.randomized_bluetooth == True and self.TRANSMIT_WHEN_RANDOMIZED):
            # print(self.randomized_bluetooth, "hello")
            self.set_next_bluetooth_transmit()
            self.bluetooth_id = self.temp_bluetooth_id
            self.transmit_bluetooth = True
        else:
            self.bluetooth_id = None
            self.transmit_bluetooth = False
            
        if self.identifier_counter >= self.next_wifi_transmit or (self.randomized_wifi == True and self.TRANSMIT_WHEN_RANDOMIZED):
            self.set_next_wifi_transmit()
            self.wifi_id = self.temp_wifi_id
            self.transmit_wifi = True
        else:
            self.wifi_id = None
            self.transmit_wifi = False

        if self.ENABLE_LTE_RANDOMIZATION:
            if self.lte_counter >= self.next_lte_transmit or (self.randomized_lte == True and self.TRANSMIT_WHEN_RANDOMIZED):
                self.set_next_lte_transmit()
                self.lte_id = self.temp_lte_id
                self.transmit_lte = True
            else:
                self.lte_id = None
                self.transmit_lte = False
        else:
            if self.identifier_counter >= self.next_lte_transmit or (self.randomized_lte == True and self.TRANSMIT_WHEN_RANDOMIZED):
                self.set_next_lte_transmit()
                self.lte_id = self.temp_lte_id
                self.transmit_lte = True
            else:
                self.lte_id = None
                self.transmit_lte = False
