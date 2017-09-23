"""
XS1 HTTP Web API constants used to create GET request URLs and parse the JSON answer.
"""

from enum import Enum


class UrlParam(Enum):
    """
    URL parameters
    """

    USER = 'user'
    """'User' parameter"""

    PASSWORD = 'pwd'
    """'Password' parameter"""

    COMMAND = 'cmd'
    """command parameter that specifies the method the api is queried with"""

    NUMBER = 'number'
    """number parameter that specifies the id of an actuator or sensor"""

    VALUE = 'value'
    """'value' parameter that specifies the new value to set an actuator (or sensor) to"""

    FUNCTION = 'function'
    """parameter that specifies the function to execute (on an actuator)"""


class Command(Enum):
    """
    XS1 Web API (HTTP) commands
    """

    GET_PROTOCOL_INFO = 'get_protocol_info'
    """Command to get information about the protocol version used by the XS1"""

    GET_CONFIG_INFO = 'get_config_info'
    """Command to get (final) configuration information about the XS1"""

    GET_CONFIG_MAIN = 'get_config_main'
    """Command to get additional configuration information about the XS1"""

    GET_LIST_SYSTEMS = 'get_list_systems'
    """Returns a list of currently compatible systems"""

    GET_LIST_FUNCTIONS = 'get_list_functions'
    """Returns a list of available functions / actions for actuators"""

    GET_TYPES_ACTUATORS = 'get_types_actuators'
    """Retrieves the types of compatible actuators"""

    GET_TYPES_SENSORS = 'get_types_sensors'
    """Retrieves the types of compatible sensors"""

    GET_LIST_RFMODES = 'get_list_rfmodes'
    """Returns a list of currently active and compatible RF modes of the XS1"""

    GET_CONFIG_ACTUATOR = 'get_config_actuator'
    """Command to get the configuration of an actuator"""

    SET_CONFIG_ACTUATOR = 'set_config_actuator'
    """Command to set the configuration of an actuator"""

    GET_CONFIG_SENSOR = 'get_config_sensor'
    """Command to get the configuration of a sensor"""

    SET_CONFIG_SENSOR = 'set_config_sensor'
    """Command to set the configuration of a sensor"""

    GET_LIST_ACTUATORS = 'get_list_actuators'
    """Command to get a list of all actuators"""

    GET_LIST_SENSORS = 'get_list_sensors'
    """Command to get a list of all sensors"""

    GET_STATE_ACTUATOR = 'get_state_actuator'
    """Command to get the state of a specific actuator"""

    GET_STATE_SENSOR = 'get_state_sensor'
    """Command to get the state of a specific sensor"""

    SET_STATE_ACTUATOR = 'set_state_actuator'
    """Command to set a new value on an actuator"""

    SET_STATE_SENSOR = 'set_state_sensor'
    """Command to set a new value on a sensor (for debugging)"""


class Node(Enum):
    """
    JSON API nodes
    """

    VERSION = 'version'
    """Node with protocol version info"""

    INFO = 'info'
    """Node with gateway specific information"""

    SYSTEM = 'system'
    """Node with gateway main configuration"""

    ACTUATOR = 'actuator'
    """Node with an array of actuators"""

    SENSOR = 'sensor'
    """Node with an array of sensors"""

    FUNCTION = 'function'
    """Node with an array of functions"""

    ERROR = 'error'
    """Node containing the error code"""

    # device info nodes
    DEVICE_NAME = 'devicename'
    """Hostname"""

    DEVICE_HARDWARE_VERSION = 'hardware'
    """Hardware revision"""

    DEVICE_BOOTLOADER_VERSION = 'bootloader'
    """Bootloader version number"""

    DEVICE_FIRMWARE_VERSION = 'firmware'
    """Firmware version number"""

    DEVICE_UPTIME = 'uptime'
    """Uptime in seconds"""

    DEVICE_MAC = 'mac'
    """MAC address"""

    # inner nodes
    PARAM_ID = 'id'
    """Device id (only unique within actuators/sensors)"""

    PARAM_NUMBER = 'number'
    """Alternative device id (only unique within actuators/sensors)"""

    PARAM_NAME = 'name'
    """Device name"""

    PARAM_TYPE = 'type'
    """Device type"""

    PARAM_VALUE = 'value'
    """Current device value"""

    PARAM_NEW_VALUE = 'newvalue'
    """New value to set for the device"""

    PARAM_UTIME = 'utime'
    """Time this device was last updated"""

    PARAM_UNIT = 'unit'
    """Device value unit"""

    PARAM_FUNCTION = 'function'
    """Array of functions"""

    PARAM_DESCRIPTION = 'dsc'
    """Device description"""


class ErrorCode(Enum):
    """
    Error codes
    """

    INVALID_COMMAND = '01'
    """Error code for 'invalid command' """

    CMD_TYPE_MISSING = '02'
    """Error code for 'cmd type missing'"""

    NOT_FOUND = '03'
    """Error code for 'number/name not found'"""

    DUPLICATE = '04'
    """Error code for 'duplicate name'"""

    INVALID_SYSTEM = '05'
    """Error code for 'invalid system'"""

    INVALID_FUNCTION = '06'
    """Error code for 'invalid function'"""

    INVALID_DATE_TIME = '07'
    """Error code for 'invalid date/time'"""

    OBJECT_NOT_FOUND = '08'
    """Error code for 'object not found'"""

    TYPE_NOT_VIRTUAL = '09'
    """Error code for 'type not virtual'"""

    SYNTAX_ERROR = '10'
    """Error code for 'syntax error'"""

    INVALID_TIME_RANGE = '11'
    """Error code for 'error time range'"""

    PROTOCOL_VERSION_MISMATCH = '12'
    """Error code for 'protocol version mismatch'"""

    @staticmethod
    def get_message(error_code) -> str:
        if error_code == ErrorCode.INVALID_COMMAND:
            return 'invalid command'
        elif error_code == ErrorCode.CMD_TYPE_MISSING:
            return 'cmd type missing'
        elif error_code == ErrorCode.NOT_FOUND:
            return 'number/name not found'
        elif error_code == ErrorCode.DUPLICATE:
            return 'duplicate name'
        elif error_code == ErrorCode.INVALID_SYSTEM:
            return 'invalid system'
        elif error_code == ErrorCode.INVALID_FUNCTION:
            return 'invalid function'
        elif error_code == ErrorCode.INVALID_DATE_TIME:
            return 'invalid date/time'
        elif error_code == ErrorCode.OBJECT_NOT_FOUND:
            return 'object not found'
        elif error_code == ErrorCode.TYPE_NOT_VIRTUAL:
            return 'type not virtual'
        elif error_code == ErrorCode.SYNTAX_ERROR:
            return 'syntax error'
        elif error_code == ErrorCode.INVALID_TIME_RANGE:
            return 'error time range'
        elif error_code == ErrorCode.PROTOCOL_VERSION_MISMATCH:
            return 'protocol version mismatch'
        else:
            return 'unknown error code'


# node values
VALUE_DISABLED = 'disabled'
"""'Disabled' type"""

UNIT_BOOLEAN = 'boolean'
"""Boolean unit type"""


class ActuatorType(Enum):
    """
    Actuator types
    """

    SWITCH = 'switch'
    DIMMER = 'dimmer'
    DOOR = 'door'
    SUN_BLIND = 'sun-blind'
    BLIND = 'blind'
    SHUTTER = 'shutter'
    SOUND = 'sound'
    THERMOSTAT = 'temperature'
    TIMERSWITCH = 'timerswitch'
    WINDOW = 'window'


class FunctionType(Enum):
    """
    Function types
    """

    ON = 'on'
    OFF = 'off'
    UNKNOWN = 'unknown'


class SensorType(Enum):
    """
    Sensor types
    """

    OTHER = 'other'
    REMOTECONTROL = 'remotecontrol'
    HYGROMETER = 'hygrometer'
    BAROMETER = 'barometer'
    WIND_SPEED = 'windspeed'
    WIND_DIRECTION = 'winddirection'
    WIND_VARIANCE = 'windvariance'
    LIGHT = 'light'
    PYRANOMETER = 'pyranometer'
    RAIN = 'rain'
    RAIN_INTENSITY = 'rainintensity'
    RAIN_1H = 'rain_1h'
    RAIN_24H = 'rain_24h'
    SOIL_TEMP = 'soiltemp'
    SOIL_MOISTURE = 'soilmoisture'
    LEAF_WETNESS = 'leafwetness'
    WATERLEVEL = 'waterlevel'
    MOTION = 'motion'
    PRESENCE = 'presence'
    SMOKEDETECTOR = 'smokedetector'
    HEATDETECTOR = 'heatdetector'
    WATERDETECTOR = 'waterdetector'
    AIRQUALITY = 'air_quality'
    WINDOW_OPEN = 'windowopen'
    DOOR_OPEN = 'dooropen'
    DOOR_BELL = 'doorbell'
    ALARMMAT = 'alarmmat'
    LIGHTBARRIER = 'lightbarrier'
    FENCEDETECTOR = 'fencedetector'
    MAIL = 'mail'
    GAS_CO = 'gas_co'
    GAS_BUTAN = 'gas_butan'
    GAS_METHAN = 'gas_methan'
    GAS_PROPAN = 'gas_propan'
    WINDGUST = 'windgust'
    UV_INDEX = 'uv_index'
    POWER_CONSUMPTION = 'pwr_consump'
    WATER_CONSUMPTION = 'wtr_consump'
    GAS_CONSUMPTION = 'gas_consump'
    OIL_CONSUMPTION = 'oil_consump'
    POWER_PEAK = 'pwr_peak'
    WATER_PEAK = 'wtr_peak'
    GAS_PEAK = 'gas_peak'
    OIL_PEAK = 'oil_peak'
