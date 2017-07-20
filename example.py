"""
This is an example of how to use this api.
There are other methods besides the ones shown here. Have a look at the documentation at
http://xs1-api-client.readthedocs.io/
to get more info.
"""
import time

from xs1_api_client import api as xs1api
from xs1_api_client import api_constants

# Create an api object with private configuration
api = xs1api.XS1('192.168.2.75', None, None)

# Update the connection info at a later time
api.set_connection_info('192.168.2.75', None, None)

print("Gateway Hostname: " + api.get_gateway_name())
print("Gateway MAC: " + api.get_gateway_mac())
print("Gateway Hardware Version: " + api.get_gateway_hardware_version())
print("Gateway Bootloader Version: " + api.get_gateway_bootloader_version())
print("Gateway Firmware Version: " + api.get_gateway_firmware_version())
print("Gateway uptime: " + str(api.get_gateway_uptime()) + " seconds")

print("")

# access api values (f.ex. for actuator or sensor type)
print(api_constants.NODE_ACTUATOR)
print(api_constants.ACTUATOR_TYPE_SWITCH)
print(api_constants.UNIT_BOOLEAN)

print("")

# you can directly interface with the gateway using the api methods:
print(str(api.get_state_actuator(3)))
# ATTENTION: this would raise an EXCEPTION (id 65 > 64 = max)!
# print(str(api.get_state_actuator(65)))

# or set a new value using:
print(str(api.set_actuator_value(3, 100)))

print("")

# but I would recommend using the objects to get and set values like so:
# receive a list of all actuators
actuators = api.get_all_actuators()

print("Actuators:")
# print their name and current value
for actuator in actuators:
    print("Actuator " + str(actuator.id()) + ": " + actuator.name() + " (" + str(actuator.value()) + ")")
    ##" " + str(actuator.unit()) +

# receive a list of all sensors
sensors = api.get_all_sensors()

print("")
print("Sensors:")
# print their name and current value
for sensor in sensors:
    print("Sensor " + str(sensor.id()) + ": " + sensor.name() + " (" + str(sensor.value()) + ")")
    ## + " " + str(sensor.unit())

# set a new value for an actuator
changing_actuator = actuators[6]  # pick one from the received list
print("Old value: " + str(changing_actuator.value()))  # print old value
print("Old new_value: " + str(changing_actuator.new_value()))  # print old new_value
changing_actuator.set_value(16)  # use the object method to set a new value (turn light on)
print("Updated value: " + str(
    changing_actuator.value()))  # print the updated value (will be updated with the response of the gateway)
print("Updated new_value: " + str(
    changing_actuator.new_value()))  # print the updated new_value

print("Sleeping...")
time.sleep(3)

print("")
# alternatively you can call a function that is defined for an actuator (in the gateway)

# list all functions
for func in changing_actuator.get_functions():
    print("Function " + str(func.id()) + " (" + func.type() + "): " + func.description())

# find a function by type
func_off = changing_actuator.get_function_by_type(api_constants.FUNCTION_TYPE_OFF)
if func_off:
    func_off.execute()

# or id
print("")
func_0 = changing_actuator.get_function_by_id(1)
if func_0:
    print("Function 1:")
    print("Function " + str(func_0.id()) + " (" + func_0.type() + "): " + func_0.description())

print("")
print("Updated value: " + str(
    changing_actuator.value()))  # print the updated value (will be updated with the response of the gateway)
print("Updated new_value: " + str(
    changing_actuator.new_value()))  # print the updated new_value
