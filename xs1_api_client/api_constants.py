"""
XS1 HTTP Web API constants used to create GET request URLs and parse the JSON answer.
"""

from enum import Enum


class ApiConstant(Enum):
    """
    Enum base class for all api constants
    """

    def __eq__(self, other) -> bool:
        """
        Compare an ApiConstant to another one.
        If the other type is not an ApiConstant it will be compared by value using str(other)

        :param other: object to compare with
        :return: True if the same or at least the same value
        """

        if self.__class__ == other.__class__:
            # if both are Enums compare directly
            return self is other
        else:
            # otherwise try to compare just by value
            return str(other) == self.value

    def __hash__(self):
        return super().__hash__()


class UrlParam(ApiConstant):
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
    """number parameter that specifies the number of an actuator or sensor"""

    NAME = 'name'

    TYPE = 'type'
    SYSTEM = 'system'

    VALUE = 'value'
    """'value' parameter that specifies the new value to set an actuator (or sensor) to"""

    FUNCTION = 'function'
    """parameter that specifies the function to execute (on an actuator)"""

    HC1 = "hc1"
    HC2 = "hc2"

    ADDRESS = 'address'

    INITVALUE = 'initvalue'

    FUNCTION1_DSC = 'function1.dsc'
    FUNCTION1_TYPE = 'function1.type'
    FUNCTION2_DSC = 'function2.dsc'
    FUNCTION2_TYPE = 'function2.type'
    FUNCTION3_DSC = 'function3.dsc'
    FUNCTION3_TYPE = 'function3.type'
    FUNCTION4_DSC = 'function4.dsc'
    FUNCTION4_TYPE = 'function4.type'

    FACTOR = 'factor'

    OFFSET = 'offset'

    X = 'x'
    Y = 'y'
    Z = 'z'

    LOG = 'log'


class Command(ApiConstant):
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


class Node(ApiConstant):
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


class ErrorCode(ApiConstant):
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

UNIT_BOOLEAN = 'boolean'
"""Boolean unit type"""


class ActuatorType(ApiConstant):
    """
    Actuator types
    """

    DISABLED = 'disabled'
    SWITCH = 'switch'
    DIMMER = 'dimmer'
    BLIND = 'blind'
    SUN_BLIND = 'sun-blind'
    DOOR = 'door'
    WINDOW = 'window'
    TEMPERATURE = 'temperature'
    SOUND = 'sound'
    SHUTTER = 'shutter'
    TIMERSWITCH = 'timerswitch'


class FunctionType(ApiConstant):
    """
    Function types
    """

    ON = 'on'
    OFF = 'off'
    DIM_ABSOLUT = 'dim_absolut'
    RELATIVE = 'relative'
    TOGGLE = 'toggle'
    ON_WAIT_OFF = 'on_wait_off'
    DIM_UP = 'dim_up'
    DIM_DOWN = 'dim_down'
    AUTO = 'auto'
    MANUAL = 'manual'
    LEARN = 'learn'
    ABSOLUT = 'absolut'
    BLIND_ABS = 'blind_abs'
    SPECIAL = 'special'
    WAIT = 'wait'
    LONG_ON = 'long_on'
    LONG_OFF = 'long_off'
    STOP = 'stop'
    OFF_WAIT_ON = 'off_wait_on'
    ON_WAIT_ON = 'on_wait_on'
    OFF_WAIT_OFF = 'off_wait_off'
    IMPULS = 'impuls'
    BUTTON_SHORT = 'button_short'
    BUTTON_LONG = 'button_long'
    DISABLED = 'disabled'
    UNKNOWN = 'unknown'


class SensorType(ApiConstant):
    """
    Sensor types
    """

    DISABLED = 'disabled'
    OTHER = 'other'
    REMOTECONTROL = 'remotecontrol'
    TEMPERATURE = 'temperature'
    HYGROMETER = 'hygrometer'
    BAROMETER = 'barometer'
    WINDSPEED = 'windspeed'
    WINDDIRECTION = 'winddirection'
    WINDVARIANCE = 'windvariance'
    LIGHT = 'light'
    PYRANOMETER = 'pyranometer'
    RAIN = 'rain'
    RAININTENSITY = 'rainintensity'
    RAIN_1H = 'rain_1h'
    RAIN_24H = 'rain_24h'
    SOILTEMP = 'soiltemp'
    SOILMOISTURE = 'soilmoisture'
    LEAFWETNESS = 'leafwetness'
    WATERLEVEL = 'waterlevel'
    MOTION = 'motion'
    PRESENCE = 'presence'
    SMOKEDETECTOR = 'smokedetector'
    HEATDETECTOR = 'heatdetector'
    WATERDETECTOR = 'waterdetector'
    AIR_QUALITY = 'air_quality'
    WINDOWBREAK = 'windowbreak'
    WINDOWOPEN = 'windowopen'
    DOOROPEN = 'dooropen'
    DOORBELL = 'doorbell'
    ALARMMAT = 'alarmmat'
    LIGHTBARRIER = 'lightbarrier'
    FENCEDETECTOR = 'fencedetector'
    MAIL = 'mail'
    COUNTER = 'counter'
    COUNTERDIFF = 'counterdiff'
    GAS_CO = 'gas_co'
    GAS_BUTAN = 'gas_butan'
    GAS_METHAN = 'gas_methan'
    GAS_PROPAN = 'gas_propan'
    WINDGUST = 'windgust'
    UV_INDEX = 'uv_index'
    PWR_CONSUMP = 'pwr_consump'
    PWR_PEAK = 'pwr_peak'
    WTR_CONSUMP = 'wtr_consump'
    WTR_PEAK = 'wtr_peak'
    GAS_CONSUMP = 'gas_consump'
    GAS_PEAK = 'gas_peak'
    OIL_CONSUMP = 'oil_consump'
    OIL_PEAK = 'oil_peak'


class SystemType(ApiConstant):
    VIRTUAL = 'virtual'
    FS10 = 'fs10'
    FS20 = 'fs20'
    RS200 = 'rs200'
    AB400 = 'ab400'
    AB601 = 'ab601'
    IT = 'it'
    REV = 'rev'
    BSQUIGG = 'bsquigg'
    MARMI = 'marmi'
    FC1 = 'fc1'
    OASEFM = 'oasefm'
    RS862 = 'rs862'
    WS433 = 'ws433'
    WS300 = 'ws300'
    FHT = 'fht'
    HMS = 'hms'
    WMR200 = 'wmr200'
    EM = 'em'
    VENT831 = 'vent831'
    WAREMA = 'warema'
    BGJ = 'bgj'
    RSL = 'rsl'
    HE = 'he'
    IT2 = 'it2'
    FA20RF = 'fa20rf'
    RGBLED1 = 'rgbled1'
    SCHALK = 'schalk'
    AB500 = 'ab500'
