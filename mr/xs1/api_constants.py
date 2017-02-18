"""
XS1 HTTP Web API constants used to create GET request URLs and parse the JSON answer.
"""

# URL Parameter
URL_PARAM_USER = 'user='
URL_PARAM_PASSWORD = 'pwd='
URL_PARAM_COMMAND = 'cmd='
URL_PARAM_NUMBER = 'number='
URL_PARAM_VALUE = 'value='
URL_PARAM_FUNCTION = 'function='

### XS1 Web API (HTTP) commands
COMMAND_GET_LIST_ACTUATORS = 'get_list_actuators'
COMMAND_GET_LIST_SENSORS = 'get_list_sensors'
COMMAND_GET_STATE_ACTUATOR = 'get_state_actuator'
COMMAND_GET_STATE_SENSOR = 'get_state_sensor'

COMMAND_SET_STATE_ACTUATOR = 'set_state_actuator'
COMMAND_SET_STATE_SENSOR = 'set_state_sensor'

### JSON API nodes
NODE_ACTUATOR = 'actuator'
NODE_SENSOR = 'sensor'

# inner nodes
NODE_PARAM_ID = 'id'
NODE_PARAM_NUMBER = 'number'
NODE_PARAM_NAME = 'name'
NODE_PARAM_TYPE = 'type'
NODE_PARAM_VALUE = 'value'
NODE_PARAM_NEW_VALUE = 'newvalue'
NODE_PARAM_UTIME = 'utime'
NODE_PARAM_UNIT = 'unit'
NODE_PARAM_FUNCTION = 'function'

# node values
VALUE_DISABLED = 'disabled'

UNIT_BOOLEAN = 'boolean'

### Device types
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
