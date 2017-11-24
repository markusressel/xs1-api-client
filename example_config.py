"""
This is an example of how to use this api.
There may be other methods besides the ones shown here. Have a look at the documentation at
http://xs1-api-client.readthedocs.io/
to get more info.
"""

from random import randint

from xs1_api_client import api as xs1api
# Create an api object with private configuration
from xs1_api_client.api_constants import UrlParam

api = xs1api.XS1('192.168.2.75', None, None)

print("")
print(api.get_config_main())
print("")
print(api.get_list_systems())
print("")
print(api.get_list_functions())
print("")
print(api.get_types_actuators())
print("")
print(api.get_types_sensors())
print("")
print(api.get_config_actuator(1))
print("")
print(api.get_config_sensor(1))
print("")

# you can set a configuration for an actuator or sensor
# keep in mind though that additional parameters are different for each type
# and if you don't specify all necessary parameters the configuration might fail

# this is a simple example to change the name of an existing actuator configuration
# by using the RAW API method
# there is also a much simpler version of this, seen below
actuator_id_to_change = 17

# retrieve the current configuration
current_config = api.get_config_actuator(actuator_id_to_change)

print(current_config)
print("")

# copy the configuration and change the value of a key
new_config = current_config.copy()
new_config[UrlParam.NAME] = "My_new_name" + str(randint(0, 9))

# set the changed configuration and print the result of the request
print(api.set_config_actuator(actuator_id_to_change, new_config))

# you can also use convenience methods directly on the actuators and sensors
actuator = api.get_actuator(35)
print("Old name: " + actuator.name())
print("New name: " + actuator.set_name("ACTUATOR_35"))
print("New name: " + actuator.name())

sensor = api.get_sensor(8)
print("Old name: " + sensor.name())
print("New name: " + sensor.set_name("SENSOR_8"))
print("New name: " + sensor.name())
