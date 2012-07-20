==============================================================================
SNMP Device Modeling
==============================================================================

This section will cover creation of a custom *Device* subclass and modeling of
device attributes.

For purposes of this example, we'll add a *temp_sensor_count* attribute to
NetBotz devices. We'll walk through adding the attribute to the model, modeling
it from the device, and displaying it in the overview screen for NetBotz
devices.

Starting in this section we'll be working with a lot of files within the
NetBotz ZenPack's directory. To keep the path names short, I'll assume the
*$ZP_DIR_TOP* and *$ZP_DIR* environment variables have been set as follows.

.. sourcecode:: bash

    export ZP_DIR_TOP=$ZENHOME/ZenPacks/ZenPacks.training.NetBotz
    export ZP_DIR=$ZP_DIR_TOP/ZenPacks/training/NetBotz


Create a Device Subclass
==============================================================================

A *Device* subclass should not be confused with a *device class*. In the
previous section we created the /NetBotz device class from the web interface.
Creating a *Device* subclass means to extend the actual Python class of a
*Device* object. You'd do this to add new attributes, methods or relationships
to special device types.

Use the following steps to create a *NetBotzDevice* class with a new attribute
called *temp_sensor_count*.

1. Create ``$ZP_DIR/NetBotzDevice.py`` with the following contents.

   .. sourcecode:: python

       from Products.ZenModel.Device import Device


       class NetBotzDevice(Device):
           temp_sensor_count = None

           _properties = Device._properties + (
               {'id': 'temp_sensor_count', 'type': 'int'},
               )

   We're importing the base *Device* class then creating our own class called
   *NetBotzDevice* that extends it. We then add a default value of *None* for
   the new *temp_sensor_count* attribute. We then add to our base class'
   _properties collection to describe the type of data we'll be putting into
   our *temp_sensor_count* attribute. This _properties system comes from Zope.


2. Restart your *zopectl* process so the web interface can load our new module.

3. Change the *zPythonClass* property on the */NetBotz* device class to
   ``ZenPacks.training.NetBotz.NetBotzDevice``

   The *zPythonClass* property controls tells Zenoss what class of object to
   instantiate when a new device is added to the device class. The default
   value for this property is blank. If the value is blank or invalid,
   *Products.ZenModel.Device* will be used.

   .. note::

      Those with Python experience might notice that
      *ZenPacks.training.NetBotz.NetBotzDevice* is a module, not a class. This
      is true. The terminology is wrong. One can only assume that the creator
      of this functionality didn't appreciate the difference between Python
      modules and classes.


4. Reset the Python class of our existing device.

   Run ``zendmd`` and execute the following snippet.

   .. sourcecode:: python

      device = find("Netbotz01")
      print device.__class__

   You should see *<class 'Products.ZenModel.Device.Device'>*. We see this
   instead of the Python class we just created because the *zPythonClass*
   property is only used when a new device is created in a device class, or
   when a device is moved into a device class with a differing *zPythonClass*
   value.

   So we have two options for getting our NetBotz device to use the new Python
   class we created. We can either delete the device and add it back, or move
   it to a different device class and back. Actually, there's a third option
   that I use most frequently to solve this problem. I move it into the same
   device class using *zendmd*. Execute the following snippet within *zendmd*
   to reset the device's Python class.

   .. sourcecode:: python

      dmd.Devices.NetBotz.moveDevices('/NetBotz', 'Netbotz01')
      device = find("Netbotz01")
      print device.__class__

   Now you should see *<class 'ZenPacks.training.NetBotz.NetBotzDevice'>*
   printed. This confirms that our *Device* subclass works, and that we've
   configure *zPythonClass* correctly for the */NetBotz* device class.


Create a Modeler Plugin
==============================================================================

The next step is to build a modeler plugin. A modeler plugin's responsibility
reach out into the world, gather data, and plug it into the attributes and
relationships of our model classes. In this example, this means to make the
SNMP requests necessary to determine how many temperature sensors a NetBotz
device has, and populate our *temp_sensor_count* attribute with the result.

Use the following steps to create our modeler plugin.

1. Make the directory that'll contain our modeler plugin.

   .. sourcecode:: bash

      mkdir -p $ZP_DIR/modeler/plugins/training/snmp

   Note that we're using our ZenPack's *training* namespace, then *snmp*.
   This is the recommended approach to make it clear what protocol the
   modeler plugin will use, and to avoid our modeler plugin conflicting with
   one from someone else's ZenPack.

2. Create *__init__.py* or *dunder-init* files.

   .. sourcecode:: bash

      touch $ZP_DIR/modeler/__init__.py
      touch $ZP_DIR/modeler/plugins/__init__.py
      touch $ZP_DIR/modeler/plugins/training/__init__.py
      touch $ZP_DIR/modeler/plugins/training/snmp/__init__.py

   These empty *__init__.py* files are mandatory if we ever expect Python to
   import modules from these directories.

3. Create ``$ZP_DIR/modeler/plugins/training/snmp/NetBotz.py`` with the
   following contents.

   .. sourcecode:: python

      from Products.DataCollector.plugins.CollectorPlugin import (
          SnmpPlugin, GetTableMap,
          )

      class NetBotz(SnmpPlugin):
          snmpGetTableMaps = (
              GetTableMap(
                  'tempSensorTable', '1.3.6.1.4.1.5528.100.4.1.1.1', {
                      '.1': 'tempSensorId',
                      }
                  ),
              )

          def process(self, device, results, log):
              return self.objectMap({
                  'temp_sensor_count': len(results[1].keys()),
                  })

   .. todo:: Describe the modeler plugin implementation in detail.

4. Restart *zopectl* and *zenhub* to load the new module.

5. Add our new *training.snmp.NetBotz* modeler plugin to the list of modeler
   plugins for the */NetBotz* device class.


Test the Modeler Plugin
------------------------------------------------------------------------------

Now that we've created and enabled a basic modeler plugin, we should test it.

1. Remodel the NetBotz device.

   You can do this from the web interface, but I usually use the command line
   because it can be easier to work with if further debugging is necessary.

   .. sourcecode:: bash

      zenmodeler run --device=Netbotz01

2. Execute the following snippet in *zendmd*.

   .. sourcecode:: python

      device = find("Netbotz01")
      print device.temp_sensor_count

   You should see *14* printed as the number of temperature sensors.


Create the API
==============================================================================

The Zenoss web interface is a consumer of the Zenoss JSON API. This is now
relevant to you because you have to make sure that you extend the API to allow
the web interface to know about the new class of object you've created.

Now that you're creating custom classes, you'll need to instruct Zenoss how
your Python objects should be translated when the web interface or other API
user requests information about them. This is a three part process that
involves creating an *IInfo* interface for your class, an *Info* adapter, and
finally registering them for use.

Create the IInfo Interface
------------------------------------------------------------------------------

.. todo:: Create this section.


Create the Info Adapter
------------------------------------------------------------------------------

.. todo:: Create this section.


Register the Info Adapter
------------------------------------------------------------------------------

.. todo:: Create this section.


Test the API
------------------------------------------------------------------------------

.. todo:: Create this section.


Change the Device Overview
==============================================================================

.. todo:: Create this section.
