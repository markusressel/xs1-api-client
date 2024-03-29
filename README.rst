.. |pypi_version| image:: https://badge.fury.io/py/xs1-api-client.svg
    :target: https://badge.fury.io/py/xs1-api-client

xs1-api-client |pypi_version|
=============================

A python 3.8+ library for accessing actuator and sensor data on the the
EZcontrol® XS1 Gateway using its HTTP API.

Build Status
============

.. |build_master| image:: https://travis-ci.org/markusressel/xs1-api-client.svg?branch=master
    :target: https://travis-ci.org/markusressel/xs1-api-client/branches
    
.. |codebeat_master| image:: https://codebeat.co/badges/f11a5607-2193-4e86-b924-fc4b1698ec8f
    :target: https://codebeat.co/projects/github-com-markusressel-xs1-api-client-master
    
+--------------------+
| Master             |
+====================+
| |build_master|     |
+--------------------+
| |codebeat_master|  |
+--------------------+

Home Assistant
==============
The initial goal of this library was to be able to integrate the EZcontrol® XS1 Gateway with `Home Assistant <https://www.home-assistant.io>`_.
You can find the related integration documentation here: 
`XS1 Home Assistant component documentation <https://www.home-assistant.io/components/xs1/>`_

Note:
xs1-api-client was designed to have reusable device objects, meaning device objects can be updated.
When a user changes the order of devices within the XS1 gateway, their ids don't change but their numbers (orders) do.
This causes the "device object" <-> device id association to get messed up. Since there is no way for us to know
about this change, it's impossible for us to tell that the device number we use for an already created device object
does not correspond to the correct device anymore without fetching all devices again, which requires the recreation
of all device objects.

**TL;DR:**
**Do not change the order of the devices in the XS1 Gateway** if you can avoid it, and if you do,
restart the service that relies on xs1-api-client to force a re-fetch of all devices.

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

.. code-block:: python

    from xs1_api_client import api as xs1api
    from xs1_api_client import api_constants

    # Create an api object with private configuration
    api = xs1api.XS1(host='192.168.2.20', user="Username", password="Password")

This will automatically try to connect to the gateway with the given credentials and retrieve basic
gateway information which you can output like this:

.. code-block:: python

    print("Gateway Hostname: " + api.get_gateway_name())
    print("Gateway MAC: " + api.get_gateway_mac())
    print("Gateway Hardware Version: " + api.get_gateway_hardware_version())
    print("Gateway Bootloader Version: " + api.get_gateway_bootloader_version())
    print("Gateway Firmware Version: " + api.get_gateway_firmware_version())
    print("Gateway uptime: " + str(api.get_gateway_uptime()) + " seconds")

You can also specify a custom port and enable SSL:

.. code-block:: python

    api = xs1api.XS1(host='192.168.2.20', port=1234, ssl=True, user="Username", password="Password")

Now that you have a connection to your gateway we can retrieve its
configuration and set or retrieve values of configured actuators and sensors or even modify their configuration.

Devices
~~~~~~~

All devices that you have configured in your XS1 are implemented using
the ``XS1Device`` base class which can be found at ``/device/__init__.py``.
This class provides basic functionality for every device like getting
the **id**, **name**, **type** and other values.

Retrieve Actuators
~~~~~~~~~~~~~~~~~~

To retrieve a list of all 64 actuators use the following call:

.. code-block:: python

    actuators = api.get_all_actuators()

This will return a list of ``XS1Actuator`` objects which is another base
class for all actuators. You can use something like this to print all
your actuators:

.. code-block:: python

    for actuator in actuators:
        print("Actuator " + str(actuator.id()) + ": " + actuator.name() + " (" + str(actuator.type()) + ")")

There is also an integrated ``__str__`` method to print out most of the useful properties just like this:

.. code-block:: python

    for actuator in actuators:
        print(actuator)

You can also filter the elements by ``enabled`` and ``disabled`` state using:

.. code-block:: python

    enabled_actuators = api.get_all_actuators(True)

Retrieve a single actuator simply by using:

.. code-block:: python

    actuator_1 = api.get_actuator(1)

Retrieve an Actuator Value
~~~~~~~~~~~~~~~~~~~~~~~~~~

To retrieve the current value of an actuator just call:

.. code-block:: python

    current_value = actuator.value()

Set a new Actuator value
~~~~~~~~~~~~~~~~~~~~~~~~

To set a new value to this actuator use:

.. code-block:: python

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

.. code-block:: python

    actuator.update()

After that the usual methods like ``actuator.value()`` will respond with
the updated state.

Executing Actuator Functions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you have defined function presets for a device you can get a list of
all functions using:

.. code-block:: python

    functions = actuator.get_functions()

and print them like this:

.. code-block:: python

    for function in functions:
        print(function)

to execute one of the functions type:

.. code-block:: python

    function.execute()

This will (like set\_value) update the device state immediately with the
gateways response. Remember though that there can be a delay for sending
this value to the actual remote device like mentioned above.

Retrieve a List of Sensors
~~~~~~~~~~~~~~~~~~~~~~~~~~

To retrieve a list of all 64 sensors use the following call:

.. code-block:: python

    sensors = api.get_all_sensors()

Just like with actuators you can filter the elements by ``enabled`` and ``disabled`` state using:

.. code-block:: python

    enabled_sensors = api.get_all_sensors(True)

| This will return a list of ``XS1Sensor`` objects which is the base
  class for all sensors.
| You can print basic information about them like this:

.. code-block:: python

    for sensor in sensors:
        print("Sensor " + str(sensor.id()) + ": " + sensor.name() + " (" + str(sensor.value()) + ")")

Just like mentioned above you can also use:

.. code-block:: python

    for sensor in sensors:
        print(sensor)

or:

.. code-block:: python

    sensor_1 = api.get_sensor(1)

to retrieve a specific sensor.

Updating Sensor Information
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Just like with actuators there is no automatic updates for sensors
either. To get a state update from the XS1 gateway for your sensor
object call:

.. code-block:: python

    sensor.update()

After that the complete state of this sensor is updated.

Disabled Devices
~~~~~~~~~~~~~~~~

The XS1 allows up to 64 actuator and 64 sensor configurations. These 128
device configurations are accessible via the HTTP API at any time - even
when there is nothing configured for a specific device id/number.

To check if a device has been configured (and enabled) in the XS1 web interface call:

.. code-block:: python

    device.enabled()

for both actuators and sensors alike.

Get a device configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~

Since version 2.0 it is possible to get and set device configurations on the XS1 using this library.

Please have a look at the ``example_config.py`` file to get an idea of how to retrieve a device configuration.

Modify a device configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Before you proceed**

Every configuration change will write to the internal flash memory of the XS1.
Please keep in mind that that the use flash memory can and will probably degrade when written too often.

Copy a device configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~

There is a very detailed example in this project called ``example_config_copy_actuator.py`` that will show you
how to copy a device configuration and also explains most of the important configuration parameters you will have
to use to set a custom configuration. Keep in mind though that the configuration parameters can vary between device
types and systems.


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

