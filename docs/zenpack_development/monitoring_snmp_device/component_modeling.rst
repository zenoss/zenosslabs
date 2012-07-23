==============================================================================
SNMP Component Modeling
==============================================================================

This section will cover creation of a custom *DeviceComponent* subclass,
creation of a relationship to our *NetBotDevice* class, and modeling of the
components to fill the relationship.

In the *SNMP Device Modeling* section we added a *temp_sensor_count* attribute
to our NetBotz devices. This isn't very useful. It would be more useful to
monitor the temperature being reported by each of these sensors. So that's what
we'll do. Modeling each sensor as a component allows Zenoss to automatically
discover and monitor sensors regardless of how many a particular device has.


Find Temperature Sensor Attributes
==============================================================================

In the *SNMP Device Modeling* section we used `smidump` to extract temperature
sensor information from `NETBOTZV2-MIB`. This will be even more applicable
as we decide what attributes and metrics are available on each sensor. Let's
use `smidump` and `snmpwalk` for a refresher on what's available.

Find temperature information in NETBOTZV2-MIB using the following command.

.. sourcecode:: bash

   smidump -f identifiers /usr/share/snmp/mibs/NETBOTZV2-MIB.mib | egrep -i temp

You should see the following in the output::

    NETBOTZV2-MIB tempSensorTable        table   1.3.6.1.4.1.5528.100.4.1.1
    NETBOTZV2-MIB tempSensorEntry        row     1.3.6.1.4.1.5528.100.4.1.1.1
    NETBOTZV2-MIB tempSensorId           column  1.3.6.1.4.1.5528.100.4.1.1.1.1
    NETBOTZV2-MIB tempSensorValue        column  1.3.6.1.4.1.5528.100.4.1.1.1.2
    NETBOTZV2-MIB tempSensorErrorStatus  column  1.3.6.1.4.1.5528.100.4.1.1.1.3
    NETBOTZV2-MIB tempSensorLabel        column  1.3.6.1.4.1.5528.100.4.1.1.1.4
    NETBOTZV2-MIB tempSensorEncId        column  1.3.6.1.4.1.5528.100.4.1.1.1.5
    NETBOTZV2-MIB tempSensorPortId       column  1.3.6.1.4.1.5528.100.4.1.1.1.6
    NETBOTZV2-MIB tempSensorValueStr     column  1.3.6.1.4.1.5528.100.4.1.1.1.7
    NETBOTZV2-MIB tempSensorValueInt     column  1.3.6.1.4.1.5528.100.4.1.1.1.8
    NETBOTZV2-MIB tempSensorValueIntF    column  1.3.6.1.4.1.5528.100.4.1.1.1.9

Let's now use `snmpwalk` to see what these values look like on our NetBotz
device.

.. sourcecode:: bash

   snmpwalk 127.0.1.113 1.3.6.1.4.1.5528.100.4.1.1.1

You should see a lot of output that begins with the following::

    NETBOTZV2-MIB::tempSensorId.21604919 = STRING: nbHawkEnc_1_TEMP
    NETBOTZV2-MIB::tempSensorId.1095346743 = STRING: nbHawkEnc_0_TEMP
    NETBOTZV2-MIB::tempSensorId.1382714817 = STRING: nbHawkEnc_2_TEMP1
    NETBOTZV2-MIB::tempSensorId.1382714818 = STRING: nbHawkEnc_2_TEMP2

Note the `21604919` in the first response. This is the SNMP index of the first
temperature sensor, or the first row in the table. I like to then restrict my
snmpwalk results to only show this row with a command like the following.

.. sourcecode:: bash

   snmpwalk 127.0.1.113 1.3.6.1.4.1.5528.100.4.1.1.1 | grep "\.21604919 ="

Which will show us the value of each column for that one temperature sensor::

    NETBOTZV2-MIB::tempSensorId.21604919 = STRING: nbHawkEnc_1_TEMP
    NETBOTZV2-MIB::tempSensorValue.21604919 = INTEGER: 265
    NETBOTZV2-MIB::tempSensorErrorStatus.21604919 = INTEGER: normal(0)
    NETBOTZV2-MIB::tempSensorLabel.21604919 = STRING: Temperature
    NETBOTZV2-MIB::tempSensorEncId.21604919 = STRING: nbHawkEnc_1
    NETBOTZV2-MIB::tempSensorPortId.21604919 = STRING:
    NETBOTZV2-MIB::tempSensorValueStr.21604919 = STRING: 26.500000
    NETBOTZV2-MIB::tempSensorValueInt.21604919 = INTEGER: 26
    NETBOTZV2-MIB::tempSensorValueIntF.21604919 = INTEGER: 79

Now we have everything we should need to make decisions about what attributes
we should model for our sensors and which would better be collected as
datasources to have thresholds applied and plotted over time on graphs.

My initial thoughts would be to model the following as attributes.

- `tempSensorId`
- `tempSensorEncId` (enclosure ID)
- `tempSensorPortId`

I would then want to collect `tempSensorValueStr` as a datasource because it
offers the best precision. Zenoss is capable of handling numeric strings so we
don't have to collect `tempSensorValue` and divide it by 10 like other systems
might.


Create a DeviceComponent Subclass
==============================================================================

Use the following steps to create a *TemperatureSensor* class with the
attributes discovered above.

1. Create ``$ZP_DIR/TemperatureSensor.py`` with the following contents.

   .. sourcecode:: python

      from Products.ZenModel.DeviceComponent import DeviceComponent
      from Products.ZenModel.ManagedEntity import ManagedEntity
      from Products.ZenModel.ZenossSecurity import ZEN_CHANGE_DEVICE
      from Products.ZenRelations.RelSchema import ToManyCont, ToOne


      class TemperatureSensor(DeviceComponent, ManagedEntity):
          meta_type = portal_type = 'TemperatureSensor'

          enclosure = None
          port = None

          _properties = ManagedEntity._properties + (
              {'id': 'enclosure', 'type': 'string'},
              {'id': 'port', 'type': 'string'},
              )

          _relations = ManagedEntity._relations + (
              ('sensor_device', ToOne(ToManyCont,
                  'ZenPacks.training.NetBotz.NetBotzDevice',
                  'temperature_sensors',
                  )),
              )

          factory_type_information = ({
              'actions': ({
                  'id': 'perfConf',
                  'name': 'Template',
                  'action': 'objTemplates',
                  'permissions': (ZEN_CHANGE_DEVICE,),
                  },),
              },)

          def device(self):
              return self.sensor_device()

   1. Start by importing the symbols we'll need.

   2. Define the `TemperatureSensor` class. This name must match the filename.

   3. Extend (inherit from) both the `DeviceComponent` and `ManagedEntity`
      classes.

      `DeviceComponent` provides the core functionality that's needed to
      associate our temperature sensor with a device.

      `ManagedEntity` provides base functionality for objects that are to be
      monitored. This base class provides attributes such as `snmpindex`,
      `monitor` and `productionState`.

   4. Next we set both the `meta_type` and `portal_type` of the class to
      ``TemperatureSensor``. This is used as the friendly name for the type
      of our object in various places in the web interface such as the global
      search. `meta_type` and `portal_type` should always be the same. They
      both exist for backwards compatibility reasons.

   5. Next we add the `enclosure` and `port` attributes in the same way as we
      did for our `NetBotzDevice` class.

      .. note::

         Despite noting above that we always wanted to model the *tempSensorId*
         attribute, we aren't adding an attribute for it here. This is because
         `DeviceComponent` already has both an `id` and `title` attribute that
         wherein we can store the value of *tempSensorId*.

   6. Next we have to setup `_relations` for our component type. This wasn't
      mandatory for our `NetBotzDevice` class because devices automatically
      get a containing relationship in their device class. Component's don't
      automatically get a containing relationship in their device because it
      can't automatically be known which one of their device's relations they
      belong in, or if they're perhaps nested under another component.

      The single relationship we're adding can be expressed in English as
      "`TemperatureSensor` has a relation named `sensor_device` that refers to
      a single object of the `ZenPacks.training.NetBotz.NetBotzDevice` type."

      We also describe the other side of this relationship as "`NetBotzDevice`
      has a relation named `temperature_sensors` that contains zero or more
      objects of the `TemperatureSensor` type."

   7. The `factory_type_information` section is boilerplate that should be
      used for any component types to which you will bind monitoring
      templates.

   8. Finally we must define the `device` method for our component. Every
      component must provide this method. We can find our device by calling
      the `sensor_device` relation.

2. Edit ``$ZP_DIR/NetBotzDevice.py`` to add the following to the bottom.

   .. sourcecode:: python

      _relations = Device._relations + (
          ('temperature_sensors', ToManyCont(ToOne,
              'ZenPacks.training.NetBotz.TemperatureSensor',
              'sensor_device',
              )),
          )

   You'll also need to add the following imports to the top of the file.

   .. sourcecode:: python

      from Products.ZenRelations.RelSchema import ToManyCont, ToOne

   It is mandatory that this relationship definition exist, and be an exact
   mirror of the definition on the other side.

.. note::

   See the :ref:`relationship-types` section for more information on
   relationships.


Test TemperatureSensor Class
------------------------------------------------------------------------------

With our component class defined and relationships setup we can use *zendmd*
to make sure we didn't make any mistakes. Execute the following snippet in
*zendmd*.

.. sourcecode:: python

   from ZenPacks.training.NetBotz.TemperatureSensor import TemperatureSensor

   sensor = TemperatureSensor('test_sensor_01')
   device = find("Netbotz01")
   device.temperature_sensors._setObject(sensor.id, sensor)
   sensor = device.temperature_sensors._getOb(sensor.id)
   print sensor
   print sensor.device()

You'll most likely get the following error when executing the above snippet::

    Traceback (most recent call last):
      File "<console>", line 1, in <module>
    AttributeError: temperature_sensors

This error is indicating that we have no `temperature_sensors` relationship on
the device object. This would seemingly make no sense because we just added it
to *NetBotzDevice.py* above. The key here is that existing objects like the
*Netbotz01* device don't automatically get new relationships. We have to either
delete the device and add it again, or execute the following in *zendmd* to
create the newly-defined relationship.

.. sourcecode: python

   device.buildRelations()
   commit()

Now you can go back and run the original snippet again. You should see the name
of the sensor and device objects printed if everything worked as planned.


Update the Modeler Plugin
==============================================================================

As with the `NetBotzDevice` class, the next step after creating our model class
is to populate it with a modeler plugin. We could create a new modeler plugin
to only capture the temperature sensor components, but we'll update the
`NetBotz` modeler plugin we previously created to model the sensors instead.

1. Edit ``$ZP_DIR/modeler/plugins/training/snmp/NetBotz.py`` and replace its
   contents with the following.

   .. sourcecode:: python

      from Products.DataCollector.plugins.CollectorPlugin import (
          SnmpPlugin, GetTableMap,
          )


      class NetBotz(SnmpPlugin):
          relname = 'temperature_sensors'
          modname = 'ZenPacks.training.NetBotz.TemperatureSensor'

          snmpGetTableMaps = (
              GetTableMap(
                  'tempSensorTable', '1.3.6.1.4.1.5528.100.4.1.1.1', {
                      '.1': 'tempSensorId',
                      '.5': 'tempSensorEncId',
                      '.6': 'tempSensorPortId',
                      }
                  ),
              )

          def process(self, device, results, log):
              temp_sensors = results[1].get('tempSensorTable', {})

              rm = self.relMap()
              for snmpindex, row in temp_sensors.items():
                  name = row.get('tempSensorId')
                  if not name:
                      log.warn('Skipping temperature sensor with no name')
                      continue

                  rm.append(self.objectMap({
                      'id': self.prepId(name),
                      'title': name,
                      'snmpindex': snmpindex,
                      'enclosure': row.get('tempSensorEncId'),
                      'port': row.get('tempSensorPortId'),
                      }))

              return rm

   .. todo:: Detail changes from last iteration of modeler plugin.

2. Restart *zopectl* and *zenhub* to load the changed module.


Test the Modeler Plugin
------------------------------------------------------------------------------

We already added the *training.snmp.NetBotz* modeler plugin the the */NetBotz*
device class in an earlier exercise. So we only need to run *zenmodeler* to
test the temperature sensor modeling updates.

1. Run ``zenmodeler run --device=Netbotz01``

   We should see *Changes in configuration applied* near the end of
   zenmodeler's output. The changes referred to should be 14 temperature sensor
   objects being created and added to the device's temperature_sensors
   relationship.

2. Execute the following snipped in *zendmd*.

   .. sourcecode:: python

      device = find("Netbotz01")
      pprint(device.temperature_sensors())

   You should see a list of all 14 temperature sensors printed. We can test in
   more depth by validating that all of our modeled attributes were set
   properly.

   .. sourcecode:: python

      for sensor in device.temperature_sensors():
          print "%17s: %-17s %-11s %-11s %-11s" % (
            sensor.id, sensor.title, sensor.snmpindex, sensor.enclosure,
            sensor.port)


Create the API
==============================================================================

.. todo:: Write this section.


Test the API
------------------------------------------------------------------------------

.. todo:: Write this section.


Add Component Display JavaScript
==============================================================================

.. todo:: Write this section.


Test the Component Display
------------------------------------------------------------------------------

.. todo:: Write this section.
