from env import *
from random import uniform, randint, random
from services.general import random_identifier

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

        self.pause_time = uniform(PAUSE_DURATION_MIN, PAUSE_DURATION_MAX)  # Random initial pause time
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
        
        self.randomized_bluetooth = False
        self.randomized_wifi = False
        self.randomized_lte = False
        
        self.set_next_bluetooth_refresh()
        self.set_next_wifi_refresh()
        self.set_next_lte_refresh()
        
    def set_next_bluetooth_transmit(self):
        duration = round(uniform(BLUETOOTH_MIN_TRANSMIT, BLUETOOTH_MAX_TRANSMIT) / 0.25) * 0.25
        self.next_bluetooth_transmit = self.identifier_counter + duration

    def set_next_wifi_transmit(self):
        duration = round(uniform(WIFI_MIN_TRANSMIT, WIFI_MAX_TRANSMIT) / 0.25) * 0.25
        self.next_wifi_transmit = self.identifier_counter + duration

    def set_next_lte_transmit(self):
        duration = round(uniform(LTE_MIN_TRANSMIT, LTE_MAX_TRANSMIT) / 0.25) * 0.25
        self.next_lte_transmit = self.identifier_counter + duration

    def set_next_bluetooth_refresh(self):
        duration = randint(BLUETOOTH_MIN_REFRESH, BLUETOOTH_MAX_REFRESH)
        self.next_bluetooth_refresh = self.identifier_counter + duration

    def set_next_wifi_refresh(self):
        duration = randint(WIFI_MIN_REFRESH, WIFI_MAX_REFRESH)
        self.next_wifi_refresh = self.identifier_counter + duration

    def set_next_lte_refresh(self):
        duration = randint(LTE_MIN_REFRESH, LTE_MAX_REFRESH)
        self.next_lte_refresh = self.identifier_counter + duration

    def move(self):
        if self.is_paused:
            self.pause_time -= 1
            if self.pause_time <= 0:
                self.is_paused = False
                self.pause_time = uniform(PAUSE_DURATION_MAX, PAUSE_DURATION_MAX)
            return

        # Simulate random walk movement within a predefined area
        x = self.location[0] + uniform(-self.max_step_size, self.max_step_size)
        y = self.location[1] + uniform(-self.max_step_size, self.max_step_size)

        # Ensure user stays within predefined area (e.g., a city)
        x = max(min(x, AREA_SIZE), -AREA_SIZE)
        y = max(min(y, AREA_SIZE), -AREA_SIZE)

        self.location = (x, y)

        # Randomly pause after movement
        if random() < PROBABILITY_PAUSE:
            self.is_paused = True

    def randomize_identifiers(self):
        self.identifier_counter += 1

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
