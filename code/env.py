#Area of capture dimension (in meters)
AREA_SIZE = 500

# Duration of the simulation (in seconds)
DURATION_SIMULATION = 7200

# Number of characters in identifier
IDENTIFIER_LENGTH = 12


TIMESTEPS = 18400

#-------------------------#
#   Movement Parameters   #
#-------------------------#

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
WIFI_MIN_REFRESH = 2*60
WIFI_MAX_REFRESH = 5*60

# LTE refresh range uniform (in s)
LTE_MIN_REFRESH =  10
LTE_MAX_REFRESH =  60

#Range for communication protocols
BLUETOOTH_RANGE=10
WIFI_RANGE=30
LTE_RANGE=100

BLUETOOTH_LOCALIZATION_ERROR=0.1
WIFI_LOCALIZATION_ERROR=0.1
LTE_LOCALIZATION_ERROR=0.1

# Start SUMO as a subprocess
SUMO_BIN_PATH = "/usr/bin/"

sumo_binary = "sumo"
SUMO_CFG_FILE = "/home/anonymous/MoSTScenario/scenario/most.sumocfg"
# SUMO_CFG_FILE = "/home/aneet_wisec/privacy_cispa/MoSTScenario/scenario/most.sumocfg"


DELTA_P = 2
