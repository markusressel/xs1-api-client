from xs1_api_client import api as xs1api
from xs1_api_client import api_constants

api = xs1api.XS1()  # Create an api object
api.set_connection_info('192.168.2.75', None, None)  # set connection info (globally)

# access api values (f.ex. for actuator or sensor type)
print(api_constants.NODE_ACTUATOR)

# receive a list of all actuators
actuators = api.get_all_actuators()

# print their name and current value
for actuator in actuators:
    print("Actuator " + str(actuator.id()) + ": " + actuator.name() + " (" + str(actuator.value()) + ")")
    ##" " + str(actuator.unit()) +

# receive a list of all sensors
sensors = api.get_all_sensors()

# print their name and current value
for sensor in sensors:
    print("Sensor " + str(sensor.id()) + ": " + sensor.name() + " (" + str(sensor.value()) + ")")
    ## + " " + str(sensor.unit())

# set a new value for an actuator
changing_actuator = actuators[0]  # pick one from the retreived list
print("Old value: " + str(changing_actuator.value()))  # print old value
changing_actuator.set_value(0)  # use the object method to set a new value
print("New value: " + str(
    changing_actuator.value()))  # print the new value (will be updated with the response of the gateway)
