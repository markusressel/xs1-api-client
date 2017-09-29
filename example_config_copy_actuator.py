"""
This is an example of how to use this api.
There may be other methods besides the ones shown here. Have a look at the documentation at
http://xs1-api-client.readthedocs.io/
to get more info.
"""

from xs1_api_client import api as xs1api
# Create an api object with private configuration
from xs1_api_client.api_constants import FunctionType, SystemType, ActuatorType, UrlParam

api = xs1api.XS1('192.168.2.75', None, None)

# to set a completely new configuration for an actuator
# you have to get all of its configuration parameters right
# otherwise the request will fail

# it is also possible to update only part of a configuration
# but I was not able to find any documentation on what is possible

# this is just one example how to create a configuration
# configuration parameters can vary depending on the type and system of your device

# Tip: when using a dictionary to manually set values (like in this example)
# try to use UrlParam enum constants as keys to avoid typos

my_config = {}

# this is only one example

# {
#     "number": 1,
#     "id": 0,
#     "name": "Fernsehlampe",
#     "system": "ab400",
#     "type": "switch",
#     "hc1": 26,
#     "hc2": 0,
#     "address": 1,
#     "function": [
#         {"type": "on", "dsc": "ON"},
#         {"type": "off", "dsc": "OFF"},
#         {"type": "disabled", "dsc": ""},
#         {"type": "disabled", "dsc": ""}
#     ],
#     "room": 1,
#     "x": 0,
#     "y": 0,
#     "z": 0,
#     "log": "off"
# }


# first of all your configuration must specify the actuator/sensor id
# BUT this is done for you when calling the api method
# so you don't have to worry about that just yet

# next provide a name
# Note: be aware of the character limitations of the xs1 though!
# when using the actuator.set_name() method this is checked automatically for you
my_config[UrlParam.NAME] = "My_Actuator"

# now provide a system
my_config[UrlParam.SYSTEM] = SystemType.IT.value

# and a corresponding type
my_config[UrlParam.TYPE] = ActuatorType.SWITCH.value

# now comes the tricky part
# provide a "connection" configuration for your device
# this can vary greatly between types and systems

my_config['hc1'] = 2
my_config['hc2'] = 0
my_config['address'] = 5

# every actuator can have up to 4 functions,
# you can set those individually using exact url parameters like this

my_config[UrlParam.FUNCTION1_DSC] = "On"
my_config[UrlParam.FUNCTION1_TYPE] = FunctionType.ON.value

my_config[UrlParam.FUNCTION2_DSC] = "Off"
my_config[UrlParam.FUNCTION2_TYPE] = FunctionType.OFF.value

my_config[UrlParam.FUNCTION3_DSC] = ""
my_config[UrlParam.FUNCTION3_TYPE] = FunctionType.DISABLED.value

my_config[UrlParam.FUNCTION4_DSC] = ""
my_config[UrlParam.FUNCTION4_TYPE] = FunctionType.DISABLED.value

# you can also use a list of dictionaries instead
# like seen in a json configuration response from the gateway
# the functions will be numbered ascending

my_config[UrlParam.FUNCTION] = [
    {"type": FunctionType.ON, "dsc": "On"},
    {"type": FunctionType.ON, "dsc": "OFF"},
    {"type": FunctionType.DISABLED, "dsc": ""},
    {"type": FunctionType.DISABLED, "dsc": ""}
]

# you can set a configuration for an actuator or sensor
# keep in mind though that parameters will be different for some types
# and if you don't specify all necessary parameters the configuration might fail

# in this example we will try to copy an existing actuator to a new actuator slot
# ATTENTION: This will (if successful) overwrite any existing configuration!
# Make a BACKUP!

actuator_id_to_copy = 30
target_id = 31

# retrieve the current configuration
configuration = api.get_config_actuator(actuator_id_to_copy)

print("Source: " + str(configuration))
print("")

# change the name (duplicate names will raise an error)
copy = configuration.copy()
copy[UrlParam.NAME.value] = "Actuator_30_CPY"

# set the changed configuration
api.set_config_actuator(target_id, copy)

# print the new state
print("Target: " + str(api.get_config_actuator(target_id)))


# print(api.set_config_actuator(actuator_id_to_change, my_config))

# new_config = api.get_config_actuator(actuator_id_to_change)
# print(new_config)
