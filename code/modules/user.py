from env import *
from random import uniform, randint, random
from services.general import random_identifier

class User:
    def __init__(
        self, user_id, location, bluetooth_id, wifi_id, lte_id, max_step_size=0.1
    ):
        self.user_id = user_id
        self.bluetooth_id = bluetooth_id
        self.wifi_id = wifi_id
        self.lte_id = lte_id
        self.location = location
        self.max_step_size = max_step_size

        self.pause_time = uniform(PAUSE_DURATION_MIN, PAUSE_DURATION_MAX)  # Random initial pause time
        # TODO: why do users start off paused?
        self.is_paused = True

        self.identifier_counter = 0
        self.set_next_bluetooth_refresh()
        self.set_next_wifi_refresh()
        self.set_next_lte_refresh()

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
