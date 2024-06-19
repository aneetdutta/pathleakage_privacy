#Area of capture dimension (in meters)
AREA_SIZE = 500

# Duration of the simulation (in seconds)
DURATION_SIMULATION = 7200

# Create only same set of users for different run
TOTAL_NUMBER_OF_USERS = 256
ENABLE_USER_THRESHOLD = False

# Number of characters in identifier
IDENTIFIER_LENGTH = 12

USER_TIMESTEPS = 18300

# FIRST_TIMESTEP = 18001.25
#-------------------------#
#   Movement Parameters   #
#-------------------------#
POLYGON_COORDS = [
    (3499.77, 1500.07),
    (5798.43, 3799.93),
    (6452.11, 3150.56),
    (5401.44, 2099.71),
    (5751.91, 1749.63),
    (4500.10, 498.92),
]

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
WIFI_MIN_REFRESH = 10
WIFI_MAX_REFRESH = 15

# LTE refresh range uniform (in s)
LTE_MIN_REFRESH =  5*60
LTE_MAX_REFRESH =  10*60


# Bluetooth IDs transmit range uniform (in s)
BLUETOOTH_MIN_TRANSMIT = 0.25
BLUETOOTH_MAX_TRANSMIT = 5

# WifI ID transmit range uniform (in s)
WIFI_MIN_TRANSMIT = 0.25
WIFI_MAX_TRANSMIT = 15

# LTE transmit range uniform (in s)
LTE_MIN_TRANSMIT =  0.25
LTE_MAX_TRANSMIT =  5

#Range for communication protocols
BLUETOOTH_RANGE=10
WIFI_RANGE=30
LTE_RANGE=100

BLUETOOTH_LOCALIZATION_ERROR=1
WIFI_LOCALIZATION_ERROR=5
LTE_LOCALIZATION_ERROR=10

# Mobility factor in m/s
MAX_MOBILITY_FACTOR = 1.66

ENABLE_BLUETOOTH = False
# Sniffer timestep
SNIFFER_TIMESTEP = max(LTE_MAX_TRANSMIT, WIFI_MAX_TRANSMIT, BLUETOOTH_MAX_TRANSMIT)

SNIFFER_PROCESSING_BATCH_SIZE = 100

# Start SUMO as a subprocess
SUMO_BIN_PATH = "/usr/bin/"

sumo_binary = "sumo"
common_path = "/MoSTScenario/scenario/most.sumocfg"

SUMO_CFG_FILE = f"/home/anonymous{common_path}"
# SUMO_CFG_FILE = f"/home/aneet_wisec/privacy_cispa{common_path}"
# SUMO_CFG_FILE = f"/home/wisec{common_path}"

DELTA_P = 2
