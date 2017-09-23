"""
This is an example of how to use this api.
There are other methods besides the ones shown here. Have a look at the documentation at
http://xs1-api-client.readthedocs.io/
to get more info.
"""

from random import randint

from xs1_api_client import api as xs1api

# Create an api object with private configuration
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

# this is a simple example to change the name of an existing configuration
actuator_id_to_change = 17
current_config = api.get_config_actuator(actuator_id_to_change)

print(current_config)
print("")
new_config = current_config.copy()
new_config["name"] = "My_new_name" + str(randint(0, 9))

print(api.set_config_actuator(actuator_id_to_change, new_config))

actuator = api.get_actuator(35)
print("Old name: " + actuator.name())
print("New name: " + actuator.set_name("FF_s2"))
print("New name: " + actuator.name())

sensor = api.get_sensor(8)
print("Old name: " + sensor.name())
print("New name: " + sensor.set_name("SENSOR_8"))
print("New name: " + sensor.name())
