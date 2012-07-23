==============================================================================
Component Modeling
==============================================================================

This section will cover creation of a custom *DeviceComponent* subclass,
creation of a relationship to our *NetBotDevice* class, and modeling of the
components to fill the relationship.

In the *Device Modeling* section we added a *temp_sensor_count* attribute
to our NetBotz devices. This isn't very useful. It would be more useful to
monitor the temperature being reported by each of these sensors. So that's what
we'll do. Modeling each sensor as a component allows Zenoss to automatically
discover and monitor sensors regardless of how many a particular device has.


Find Temperature Sensor Attributes
==============================================================================

In the *Device Modeling* section we used `smidump` to extract temperature
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
          meta_type = portal_type = 'NetBotzTemperatureSensor'

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
      ``NetBotzTemperatureSensor``. This is used as the friendly name for the
      type of our object in various places in the web interface such as the
      global search. `meta_type` and `portal_type` should always be the same.
      They both exist for backwards compatibility reasons.

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

We must now create and test the API for our new `TemperatureSensor` class much
like we did for the `NetBotzDevice` API. There's a slight difference in the
base interfaces and classes that we use because `TemperatureSensor` is a
`DeviceComponent` subclass instead of a `Device` subclass.

1. Create the `IInfo` interface.

   To create the public interface for the `TemperatureSensor` class we add the
   following class to the end of ``$ZP_DIR/interfaces.py``.

   .. sourcecode:: python

      class ITemperatureSensorInfo(IComponentInfo):
          enclosure = schema.TextLine(title=_t('Sensor Enclosure ID'))
          port = schema.TextLine(title=_t('Sensor Port ID'))

   We must also add an import for our base interface, `IComponentInfo`.

   .. sourcecode:: python

      from Products.Zuul.interfaces.component import IComponentInfo

   .. note::

      The attributes you add to your `IComponentInfo` interface control the
      fields that will be displayed when the *Details* for a component are
      viewed in the web interface.

2. Create the `Info` adapter.

   To create the `Info` adapter for the `TemperatureSensor` class we add the
   following class to the end of ``$ZP_DIR/info.py``.

   .. sourcecode:: python

      class TemperatureSensorInfo(ComponentInfo):
          implements(ITemperatureSensorInfo)

          enclosure = ProxyProperty('enclosure')
          port = ProxyProperty('port')

   We must also add an import for our base class, `ComponentInfo`.

   .. sourcecode:: python

      from Products.Zuul.infos.component import ComponentInfo

   Additionally, we need to add an import of `ITemperatureSensorInfo` from our
   own `interfaces` module. This will require an update to the existing line.

   .. sourcecode:: python

      from ZenPacks.training.NetBotz.interfaces import (
          INetBotzDeviceInfo,
          ITemperatureSensorInfo,
          )

3. Register the `Info` adapter.

   To register the `Info` adapter for `TemperatureSensor` we add the following
   before the browser include in ``$ZP_DIR/configure.zcml``.

   .. sourcecode:: xml

      <adapter
          provides=".interfaces.ITemperatureSensorInfo"
          for=".TemperatureSensor.TemperatureSensor"
          factory=".info.TemperatureSensorInfo"
          />


Test the API
------------------------------------------------------------------------------

We can now test the API using *zendmd*. Be sure to restart *zendmd* after
making changes to interfaces.py, info.py, or configure.zcml.

1. Execute the following snippet in *zendmd*.

   .. sourcecode:: python

      from Products.Zuul.interfaces import IInfo

      device = find("Netbotz01")
      sensor = device.temperature_sensors._getOb('nbHawkEnc_1_TEMP1')
      sensor_info = IInfo(sensor)

      print "id: %s, enclosure: %s, port: %s" % (
          sensor_info.id, sensor_info.enclosure, sensor_info.port)

   You should see the following line printed::

       id: nbHawkEnc_1_TEMP1, enclosure: nbHawkEnc_1, port: nbHawkEnc_1_DIN1


Add Component Display JavaScript
==============================================================================

.. todo:: Write this section.

Typically when a new type of component like `TemperatureSensor` is added, you
will want to add two JavaScript elements to provide for a more attractive
display in the web interface.

1. `registerName` to change *TemperatureSensor* to *Temperature Sensors* in the
   device's left navigation pane under *Components.*

   Add the following to ``$ZP_DIR/browser/resources/js/NetBotzDevice.js``.

   .. sourcecode:: javascript

      (function(){

      var ZC = Ext.ns('Zenoss.component');

      ZC.registerName(
          'NetBotzTemperatureSensor',
          _t('Temperature Sensor'),
          _t('Temperature Sensors'));

      })();

   1. The JavaScript code is wrapped in an anonymous function to keep it out
      of the global namespace. Ideally all ZenPack JavaScript code should be
      wrapped in this way.

      The wrapping is done using the first and last lines of the JavaScript
      snippet above.

   2. Next we get a handle to the `Zenoss.component` ExtJS namespace and store
      it in the `ZA` variable.

   3. Finally we actually register the name. The parameters to `registerName`
      are:

      1. `meta_type` of the class we're registering names for.
      2. Singular form of the human-friendly name of the class.
      3. Plural form of the human-friendly name of the class.

2. Create a `ComponentGridPanel`.

   A custom `ComponentGridPanel` allows us to customize the grid that will
   display in the top-right panel when we select *Temperature Sensors* from our
   device's component tree. Typically we customize what columns we want to
   appear, how we want those columns to appear, and how they should be sorted.

   Add the following to ``$ZP_DIR/browser/resources/js/NetBotzDevice.js``
   beneath the *ZC.registerName* but before the ``})();`` that ends the
   anonymous function.

   .. sourcecode:: javascript

      ZC.NetBotzTemperatureSensorPanel = Ext.extend(ZC.ComponentGridPanel, {
          constructor: function(config) {
              config = Ext.applyIf(config||{}, {
                  componentType: 'NetBotzTemperatureSensor',
                  autoExpandColumn: 'name',
                  sortInfo: {
                      field: 'name',
                      direction: 'ASC'
                  },
                  fields: [
                      {name: 'uid'},
                      {name: 'name'},
                      {name: 'status'},
                      {name: 'severity'},
                      {name: 'usesMonitorAttribute'},
                      {name: 'monitor'},
                      {name: 'monitored'},
                      {name: 'locking'},
                      {name: 'enclosure'},
                      {name: 'port'}
                  ],
                  columns: [{
                      id: 'severity',
                      dataIndex: 'severity',
                      header: _t('Events'),
                      renderer: Zenoss.render.severity,
                      sortable: true,
                      width: 50
                  },{
                      id: 'name',
                      dataIndex: 'name',
                      header: _t('Name'),
                      sortable: true
                  },{
                      id: 'enclosure',
                      dataIndex: 'enclosure',
                      header: _t('Enclosure ID'),
                      sortable: true,
                      width: 120
                  },{
                      id: 'port',
                      dataIndex: 'port',
                      header: _t('Port ID'),
                      sortable: true,
                      width: 120
                  },{
                      id: 'monitored',
                      dataIndex: 'monitored',
                      header: _t('Monitored'),
                      renderer: Zenoss.render.checkbox,
                      sortable: true,
                      width: 70
                  },{
                      id: 'locking',
                      dataIndex: 'locking',
                      header: _t('Locking'),
                      renderer: Zenoss.render.locking_icons,
                      width: 65
                  }]
              });

              ZC.NetBotzTemperatureSensorPanel.superclass.constructor.call(
                  this, config);
          }
      });

      Ext.reg('NetBotzTemperatureSensorPanel', ZC.NetBotzTemperatureSensorPanel);

   This is a length snippet of JavaScript. Let's go through it section by
   section.

   1. Define a new ExtJS class named `NetBotzTemperatureSensorPanel`.

      We define this class within the *Zenoss.component* namespace by using the
      `ZC` variable we created in the previous step. Just like we've been
      defining our Python classes by extending existing Zenoss Python classes,
      we do the same with JavaScript classes within the ExtJS framework. In
      this case we're extending the `ComponentGridPanel` class.

   2. Create the `NetBotzTemperatureSensorPanel` constructor.

      Our constructor method only does two things. First we override the
      `config` variable. Then we close by calling our superclass' constructor.
      Our superclass is the `ComponentGridPanel` we extended.

   3. Override `config` variable.

      This is where all of the interesting stuff happens, and where we'll be
      making changes. Let's look at each of the fields we're changing within
      `config`.

      1. `componentType`

         Must match the `meta_type` on our `TemperatureSensor` Python class.

      2. `autoExpandColumn`

         One of the following columns can be picked to automatically expand to
         use the remaining space within the user's web browser. Typically this
         is set to the `name` field, but it can be useful to choose a
         different field if the name is a well-known length and another field
         is more variable.

      3. `sortInfo`

         Controls which field and direction that the grid will be sorted by
         when it initially appears. This is an optional field and defaults to
         sort by name in ascending order if not set. So in this example the
         sortInfo field could have been left out.

      4. `fields`

         Controls which fields will be requested from the
         `TemperatureSensorInfo` API adapter on the server to display a column.
         You can request any attribute that you made available on the `Info`
         adapter. This even includes fields that are not present in the `IInfo`
         interface.

         You must be sure to include fields needed to display all of the
         `columns` specified below. For consistency I recommend having the
         following minimum set plus any that are specific to your component
         type.

         - uid
         - name
         - status
         - severity
         - usesMonitorAttribute
         - monitor
         - monitored
         - locking

      5. `columns`

         Controls the visual display of columns in the grid. Each column can
         specify the following fields.

         - `id`

           A unique identifier for the field. Typically this is set to the
           same value as `dataIndex`.

         - `dataIndex`

           Reference to one of the items from `fields` above.

         - `header`

           Text that will appear in the column's header.

         - `renderer`

           JavaScript function that will be used to render the column's data.
           This is an optional field and will default to displaying the data's
           natural string representation.

           You can find the standard renderer choices in the following file::

               $ZENHOME/Products/ZenUI3/browser/resources/js/zenoss/Renderers.js

         - `sortable`

           Whether or not the user can choose to sort the grid by this column.

         - `width`

           The width in pixels of the column. This is an optional field, but
           I highly recommend setting in on all columns except for the column
           that's referenced in `autoExpandColumn`.


Test the Component Display
------------------------------------------------------------------------------

We test our component display JavaScript by looking at it in the web interface.

If you're running *zopectl* in the foreground, it is not necessary to restart
it after making changes to existing files within our `resourceDirectory`.
However, you will have to force your browser to do a full refresh to make sure
your browser cache isn't interfering. This can typically be done by holding the
SHIFT key while clicking the refresh button or typing the refresh shortcut.

I recommend having the browser's JavaScript console open while testing so you
don't miss any errors.
