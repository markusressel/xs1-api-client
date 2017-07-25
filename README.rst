xs1-api-client
==============

A python 3.3+ library for accessing actuator and sensor data on the the
EZcontrol® XS1 Gateway using its HTTP API.

Build Status
============

.. |build_master| image:: https://travis-ci.org/markusressel/xs1-api-client.svg?branch=master
    :target: https://travis-ci.org/markusressel/xs1-api-client/branches
    
.. |build_beta| image:: https://travis-ci.org/markusressel/xs1-api-client.svg?branch=beta
    :target: https://travis-ci.org/markusressel/xs1-api-client/branches
    
.. |build_dev| image:: https://travis-ci.org/markusressel/xs1-api-client.svg?branch=dev
    :target: https://travis-ci.org/markusressel/xs1-api-client/branches
    
    
.. |codebeat_master| image:: https://codebeat.co/badges/f11a5607-2193-4e86-b924-fc4b1698ec8f
    :target: https://codebeat.co/projects/github-com-markusressel-xs1-api-client-master
    
.. |codebeat_beta| image:: https://codebeat.co/badges/f11a5607-2193-4e86-b924-xxxxxxxxx
    :target: https://codebeat.co/projects/github-com-markusressel-xs1-api-client-beta
    
.. |codebeat_dev| image:: https://codebeat.co/badges/dc91633f-bf08-4314-8da4-31cae22a8706
    :target: https://codebeat.co/projects/github-com-markusressel-xs1-api-client-dev
    
+--------------------+------------------+-----------------+
| Master             | Beta             | Dev             |
+====================+==================+=================+
| |build_master|     | |build_beta|     | |build_dev|     |
+--------------------+------------------+-----------------+
| |codebeat_master|  | |codebeat_beta|  | |codebeat_dev|  |
+--------------------+------------------+-----------------+


How to use
==========

Installation
------------

``pip install xs1-api-client``

Usage
-----

For a basic example have a look at the [example.py] file. If you need
more info have a look at the [documentation] which should help.

Basic Example
-------------

Create the API Object
~~~~~~~~~~~~~~~~~~~~~

The basic way of creating an API object is by providing connection info
directly when creating it:

::

    from xs1_api_client import api as xs1api
    from xs1_api_client import api_constants

    # Create an api object with private configuration
    api = xs1api.XS1('192.168.2.20', "Username", "Password")

This will automatically try to connect to the gateway with the given credentials and retrieve basic
gateway information which you can output like this:

::

    print("Gateway Hostname: " + api.get_gateway_name())
    print("Gateway MAC: " + api.get_gateway_mac())
    print("Gateway Hardware Version: " + api.get_gateway_hardware_version())
    print("Gateway Bootloader Version: " + api.get_gateway_bootloader_version())
    print("Gateway Firmware Version: " + api.get_gateway_firmware_version())
    print("Gateway uptime: " + str(api.get_gateway_uptime()) + " seconds")

Now that you have a connection to your gateway we can retrieve its
configuration and set or retrieve values of the devices.

Currently there is **no way of setting configuration data** with this
library. This means you still have to do all your actuator and sensor
configuration using the webinterface of the XS1.

After you have done that you can head over to the next section.

Devices
~~~~~~~

All devices that you have configured in your XS1 are implemented using
the ``XS1Device`` base class which can be found at ``/device/base.py``.
This class provides basic functionality for every device like getting
the **id**, **name**, **type** and other values.

Retrieve Actuators
~~~~~~~~~~~~~~~~~~

To retrieve a list of all actuators that are configured
(``type != "disabled"``) use the following call:

::

    actuators = api.get_all_actuators()

This will return a list of ``XS1Actuator`` objects which is another base
class for all actuators. You can use something like this to print all
your actuators:

::

    for actuator in actuators:
        print("Actuator " + str(actuator.id()) + ": " + actuator.name() + " (" + str(actuator.type()) + ")")

Retrieving a single actuator is not yet possible.

Retrieve an Actuator Value
~~~~~~~~~~~~~~~~~~~~~~~~~~

To retrieve the current value of an actuator just call:

::

    current_value = actuator.value()

Set a new Actuator value
~~~~~~~~~~~~~~~~~~~~~~~~

To set a new value to this actuator use:

::

    actuator.set_value(100)

This will send the required request to the XS1 and set the ``new_value``
property to your value. Most of the time this value is set
instantaneously is in sync with the ``value`` property. However if this
value is different from the standard ``value`` the XS1 gateway is still
trying to update the value on the remote device. For some devices this
can take up to a couple of minutes (f.ex. FHT 80B heating).

Updating Actuator Information
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Currently there is **no callback** when the value is finally updated so
**you have to update the device information manually** if you want to
get an update on its current state:

::

    actuator.update()

After that the usual methods like ``actuator.value()`` will respond with
the updated state.

Executing Actuator Functions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you have defined function presets for a device you can get a list of
all functions using:

::

    functions = actuator.get_functions()

and print them like this:

::

    for function in functions:
        print("Function " + str(function.id()) + " (" + function.type() + "): " + function.description())

to execute one of the functions use type:

::

    function.execute()

This will (like set\_value) update the device state immediately with the
gateways response. Remember though that there can be a delay for sending
this value to the actual remote device like mentioned above.

Retrieve a List of Sensors
~~~~~~~~~~~~~~~~~~~~~~~~~~

To retrieve a list of all sensors that are configured
(``type != "disabled"``) use the following call:

::

    sensors = api.get_all_sensors()

| This will return a list of ``XS1Sensor`` objects which is the base
  class for all sensors.
| You can print basic information about them like this:

::

    for sensor in sensors:
        print("Sensor " + str(sensor.id()) + ": " + sensor.name() + " (" + str(sensor.value()) + ")")

Updating Sensor Information
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Just like with actuators there is no automatic updates for sensors
either. To get a state update from the XS1 gateway for your sensor
object call:

::

    sensor.update()

After that the complete state of this sensor should be updated.

Disabled Devices
~~~~~~~~~~~~~~~~

The XS1 allows up to 64 actuator and 64 sensor configurations. These 128
device configurations are accessible via the HTTP API at any time - even
when there is nothing configured for a specific device id/number.

To check if a device has been configured in the XS1 web interface call:

::

    device.enabled()

for both actuators and sensors alike.

Contributing
============

Github is for social coding: if you want to write code, I encourage contributions through pull requests from forks 
of this repository. Create Github tickets for bugs and new features and comment on the ones that you are interested in.

License
=======

::

    xs1-api-client by Markus Ressel
    Copyright (C) 2017  Markus Ressel

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

