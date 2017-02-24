"""
XS1 HTTP Web API constants used to create GET request URLs and parse the JSON answer.
"""

# === URL Parameters ===
URL_PARAM_USER = 'user='
"""'User' parameter"""

URL_PARAM_PASSWORD = 'pwd='
"""'Password' parameter"""

URL_PARAM_COMMAND = 'cmd='
"""command parameter that specifies the method the api is queried with"""

URL_PARAM_NUMBER = 'number='
"""number parameter that specifies the id of an actuator or sensor"""

URL_PARAM_VALUE = 'value='
"""'value' parameter that specifies the new value to set an actuator (or sensor) to"""

URL_PARAM_FUNCTION = 'function='
"""parameter that specifies the function to execute (on an actuator)"""

# === XS1 Web API (HTTP) commands ===
COMMAND_GET_PROTOCOL_INFO = 'get_protocol_info'
"""Command to get information about the protocol version used by the gateway"""

COMMAND_GET_CONFIG_INFO = 'get_config_info'
"""Command to get (final) configuration information about the gateway"""

COMMAND_GET_LIST_ACTUATORS = 'get_list_actuators'
"""Command to get a list of all actuators"""

COMMAND_GET_LIST_SENSORS = 'get_list_sensors'
"""Command to get a list of all sensors"""

COMMAND_GET_STATE_ACTUATOR = 'get_state_actuator'
"""Command to get the state of a specific actuator"""

COMMAND_GET_STATE_SENSOR = 'get_state_sensor'
"""Command to get the state of a specific sensor"""

COMMAND_SET_STATE_ACTUATOR = 'set_state_actuator'
"""Command to set a new value on an actuator"""

COMMAND_SET_STATE_SENSOR = 'set_state_sensor'
"""Command to set a new value on a sensor (for debugging)"""

# === JSON API nodes ===
NODE_VERSION = 'version'
"""Node with protocol version info"""

NODE_INFO = 'info'
"""Node with gateway specific information"""

NODE_ACTUATOR = 'actuator'
"""Node with an array of actuators"""

NODE_SENSOR = 'sensor'
"""Node with an array of sensors"""

# device info nodes
NODE_DEVICE_NAME = 'devicename'
"""Hostname"""

NODE_DEVICE_HARDWARE_VERSION = 'hardware'
"""Hardware revision"""

NODE_DEVICE_BOOTLOADER_VERSION = 'bootloader'
"""Bootloader version number"""

NODE_DEVICE_FIRMWARE_VERSION = 'firmware'
"""Firmware version number"""

NODE_DEVICE_UPTIME = 'uptime'
"""Uptime in seconds"""

NODE_DEVICE_MAC = 'mac'
"""MAC address"""


# inner nodes
NODE_PARAM_ID = 'id'
"""Device id (only unique within actuators/sensors)"""

NODE_PARAM_NUMBER = 'number'
"""Alternative device id (only unique within actuators/sensors)"""

NODE_PARAM_NAME = 'name'
"""Device name"""

NODE_PARAM_TYPE = 'type'
"""Device type"""

NODE_PARAM_VALUE = 'value'
"""Current device value"""

NODE_PARAM_NEW_VALUE = 'newvalue'
"""New value to set for the device"""

NODE_PARAM_UTIME = 'utime'
"""Time this device was last updated"""

NODE_PARAM_UNIT = 'unit'
"""Device value unit"""

NODE_PARAM_FUNCTION = 'function'
"""Array of functions"""

NODE_PARAM_DESCRIPTION = 'dsc'
"""Device description"""

# node values
VALUE_DISABLED = 'disabled'
"""'Disabled' type"""

UNIT_BOOLEAN = 'boolean'
"""Boolean unit type"""

# === Device Types ===
# actuator
ACTUATOR_TYPE_SWITCH = 'switch'
ACTUATOR_TYPE_DIMMER = 'dimmer'
ACTUATOR_TYPE_DOOR = 'door'
ACTUATOR_TYPE_SUN_BLIND = 'sun-blind'
ACTUATOR_TYPE_BLIND = 'blind'
ACTUATOR_TYPE_SHUTTER = 'shutter'
ACTUATOR_TYPE_SOUND = 'sound'
ACTUATOR_TYPE_THERMOSTAT = 'temperature'
ACTUATOR_TYPE_TIMERSWITCH = 'timerswitch'
ACTUATOR_TYPE_WINDOW = 'window'

# function
FUNCTION_TYPE_ON = 'on'
FUNCTION_TYPE_OFF = 'off'

# sensor
SENSOR_TYPE_OTHER = 'other'
SENSOR_TYPE_REMOTECONTROL = 'remotecontrol'
SENSOR_TYPE_HYGROMETER = 'hygrometer'
SENSOR_TYPE_BAROMETER = 'barometer'
SENSOR_TYPE_WIND_SPEED = 'windspeed'
SENSOR_TYPE_WIND_DIRECTION = 'winddirection'
SENSOR_TYPE_WIND_VARIANCE = 'windvariance'
SENSOR_TYPE_LIGHT = 'light'
SENSOR_TYPE_PYRANOMETER = 'pyranometer'
SENSOR_TYPE_RAIN = 'rain'
SENSOR_TYPE_RAIN_INTENSITY = 'rainintensity'
SENSOR_TYPE_RAIN_1H = 'rain_1h'
SENSOR_TYPE_RAIN_24H = 'rain_24h'
SENSOR_TYPE_SOIL_TEMP = 'soiltemp'
SENSOR_TYPE_SOIL_MOISTURE = 'soilmoisture'
SENSOR_TYPE_LEAF_WETNESS = 'leafwetness'
SENSOR_TYPE_WATERLEVEL = 'waterlevel'
SENSOR_TYPE_MOTION = 'motion'
SENSOR_TYPE_PRESENCE = 'presence'
SENSOR_TYPE_SMOKEDETECTOR = 'smokedetector'
SENSOR_TYPE_HEATDETECTOR = 'heatdetector'
SENSOR_TYPE_WATERDETECTOR = 'waterdetector'
SENSOR_TYPE_AIRQUALITY = 'air_quality'
SENSOR_TYPE_WINDOW_OPEN = 'windowopen'
SENSOR_TYPE_DOOR_OPEN = 'dooropen'
SENSOR_TYPE_DOOR_BELL = 'doorbell'
SENSOR_TYPE_ALARMMAT = 'alarmmat'
SENSOR_TYPE_LIGHTBARRIER = 'lightbarrier'
SENSOR_TYPE_FENCEDETECTOR = 'fencedetector'
SENSOR_TYPE_MAIL = 'mail'
SENSOR_TYPE_GAS_CO = 'gas_co'
SENSOR_TYPE_GAS_BUTAN = 'gas_butan'
SENSOR_TYPE_GAS_METHAN = 'gas_methan'
SENSOR_TYPE_GAS_PROPAN = 'gas_propan'
SENSOR_TYPE_WINDGUST = 'windgust'
SENSOR_TYPE_UV_INDEX = 'uv_index'
SENSOR_TYPE_POWER_CONSUMPTION = 'pwr_consump'
SENSOR_TYPE_WATER_CONSUMPTION = 'wtr_consump'
SENSOR_TYPE_GAS_CONSUMPTION = 'gas_consump'
SENSOR_TYPE_OIL_CONSUMPTION = 'oil_consump'
SENSOR_TYPE_POWER_PEAK = 'pwr_peak'
SENSOR_TYPE_WATER_PEAK = 'wtr_peak'
SENSOR_TYPE_GAS_PEAK = 'gas_peak'
SENSOR_TYPE_OIL_PEAK = 'oil_peak'
