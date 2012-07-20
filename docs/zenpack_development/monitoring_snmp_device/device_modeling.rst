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
      commit()

      device = find("Netbotz01")
      print device.__class__

   Now you should see *<class 'ZenPacks.training.NetBotz.NetBotzDevice'>*
   printed. This confirms that our *Device* subclass works, and that we've
   configure *zPythonClass* correctly for the */NetBotz* device class.


Find Temperature Sensor Count
==============================================================================

Before we can write a modeler plugin to populate our new *temp_sensor_count*
attribute, we need to figure out how to get the information. There are a few
ways we could approach this. One way is to use that NETBOTZV2-MIB as a
reference to see if we can find anything about temperature sensors
specifically.

Zenoss comes with a tool called ``smidump`` that makes finding information in
MIBs much easier. There are a lot of MIB browser tools out there that make this
even easier, but I primarily use a Mac and haven't found very good options
there.

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

You'll also see another *node* and a bunch of *notification* entries. These are
related to SNMP traps, and not relevant to what we're interested in polling
right now.

What we see here is that there isn't a single OID we can request that will tell
us the number of temperature sensors. We're going to have to do an *snmpwalk*
of the table then count how many rows are in the response. Specifically we want
to remember the name and OID for the *row*: *tempSensorEntry*. Due to the
hierarchical nature of a MIBs representation this is the most specific OID that
will return the data we need.

.. sourcecode:: bash

   snmpwalk 127.0.1.113 1.3.6.1.4.1.5528.100.4.1.1.1

You'll see a lot of output that starts with::

    NETBOTZV2-MIB::tempSensorId.21604919 = STRING: nbHawkEnc_1_TEMP
    NETBOTZV2-MIB::tempSensorId.1095346743 = STRING: nbHawkEnc_0_TEMP
    NETBOTZV2-MIB::tempSensorId.1382714817 = STRING: nbHawkEnc_2_TEMP1
    NETBOTZV2-MIB::tempSensorId.1382714818 = STRING: nbHawkEnc_2_TEMP2
    NETBOTZV2-MIB::tempSensorId.1382714819 = STRING: nbHawkEnc_2_TEMP3
    NETBOTZV2-MIB::tempSensorId.1382714820 = STRING: nbHawkEnc_2_TEMP4
    NETBOTZV2-MIB::tempSensorId.1382714833 = STRING: nbHawkEnc_3_TEMP1
    NETBOTZV2-MIB::tempSensorId.1382714834 = STRING: nbHawkEnc_3_TEMP2
    NETBOTZV2-MIB::tempSensorId.1382714865 = STRING: nbHawkEnc_1_TEMP1
    NETBOTZV2-MIB::tempSensorId.1382714866 = STRING: nbHawkEnc_1_TEMP2
    NETBOTZV2-MIB::tempSensorId.1382714867 = STRING: nbHawkEnc_1_TEMP3
    NETBOTZV2-MIB::tempSensorId.1382714868 = STRING: nbHawkEnc_1_TEMP4
    NETBOTZV2-MIB::tempSensorId.2169088567 = STRING: nbHawkEnc_3_TEMP
    NETBOTZV2-MIB::tempSensorId.3242830391 = STRING: nbHawkEnc_2_TEMP

What you're seeing above is the tempSensorId column for all 14 rows in the
tempSensorTable. Continuing on you will see 14 rows for each of the other
columns in the table.


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
              temp_sensors = results[1].get('tempSensorTable', {})

              return self.objectMap({
                  'temp_sensor_count': len(temp_sensors.keys()),
                  })

   1. Start by importing SnmpPlugin and GetTableMap from Zenoss. SnmpPlugin
      will handle all of the SNMP requests for us and present the results in
      a format we can easily work with. GetTableMap will be used here because
      we need to request an SNMP table rather than specific OIDs.

   2. Out NetBotz class extends SnmpPlugin. Note that the NetBotz class name
      must match the filename (module name) of the modeler plugin.

   3. By defining snmpGetTableMaps as a tuple or list on our class we can add
      a GetTableMap object that requests that 1.3.6.1.4.1.5528.100.4.1.1.1 row
      OID and specify that we only want to get the first (.1) column and name
      it tempSensorId.

   4. The *process* method will receive a two-element tuple containing the SNMP
      request results in the *request* parameter. The first elememt,
      *results[0]*, of this tuple would be any direct OID gets of which we
      didn't request any in this plugin. The second element, *results[1]* will
      contain a dictionary of the table results. In this case *results[1]*
      would look like the following.

      .. sourcecode: python

         {
             'tempSensorTable': {
                 '21604919': 'nbHawkEnc_1_TEMP',
                 '1095346743': 'nbHawkEnc_0_TEMP',
                 '1382714817': 'nbHawkEnc_2_TEMP1',
                 '1382714818': 'nbHawkEnc_2_TEMP2',
                 '1382714819': 'nbHawkEnc_2_TEMP3',
                 '1382714820': 'nbHawkEnc_2_TEMP4',
                 '1382714833': 'nbHawkEnc_3_TEMP1',
                 '1382714834': 'nbHawkEnc_3_TEMP2',
                 '1382714865': 'nbHawkEnc_1_TEMP1',
                 '1382714866': 'nbHawkEnc_1_TEMP2',
                 '1382714867': 'nbHawkEnc_1_TEMP3',
                 '1382714868': 'nbHawkEnc_1_TEMP4',
                 '2169088567': 'nbHawkEnc_3_TEMP',
                 '3242830391': 'nbHawkEnc_2_TEMP',
             },
         }

   5. We then extract just the *tempSensorTable* results into *temp_sensors*
      to make the next *return* line a bit easier to understand.

   6. We then return a dictionary that sets the *temp_sensor_count* key's
      value to the number of keys in *temp_sensors*. Actually we return a
      dictionary that's been wrapped in an ObjectMap by the modeler plugin's
      *objectMap* utility method.

      The *process* method within all modeler plugins must return one of the
      following types of data.

      - None (makes no changes to the model)
      - ObjectMap (to apply directly to the device that's being modeled)
      - RelationshipMap (to apply to a relationship within the device)
      - A list containing 0 or more ObjectMap and/or RelationShipMap objects.

      An *ObjectMap* is simply a `dict` wrapped with some meta-data. A
      *RelationshipMap* is a `list` wrapped with some meta-data and containing
      zero or more *ObjectMap* instances.

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

This is where we define the public interface for the `NetBotzDevice` class we
created.

1. Create ``$ZP_DIR/interfaces.py`` with the following contents.

   .. sourcecode:: python

      from Products.Zuul.form import schema
      from Products.Zuul.interfaces.device import IDeviceInfo
      from Products.Zuul.utils import ZuulMessageFactory as _t

      class INetBotzDeviceInfo(IDeviceInfo):
          temp_sensor_count = schema.Int(title=_t('Number of Temperature Sensors'))

   1. Start by importing `schema`. This is how we specify the types of the
      attributes.

   2. We then import `IDeviceInfo`. This is the Info interface for standard
      devices. By extending it, we get the standard device API for free.

   3. `ZuulMessageFactory` as `_t` allows any strings we wrap in ``_t()`` to
      have translations to other languages provided for them.

   4. Next we create our Interface class, `INetBotzDeviceInfo`. Note that it's
      our model class name, `NetBotzDevice`, prefixed with *I* and suffixed
      with *Info*. This is a best practice that can make it easier to figure
      out what's going on for people later.

   5. Finally we define our single new attribute, `temp_sensor_count`. It's
      a number with no decimal precision so we use `Int`.


Create the Info Adapter
------------------------------------------------------------------------------

Now that we've defined the Info interface we have to provide the implementation
for it. This is what will be returned when the web interface asks for the Info
for one of our `NetBotzDevice` objects.

1. Create ``$ZP_DIR/info.py`` with the following contents.

   .. sourcecode:: python

      from zope.interface import implements

      from Products.Zuul.infos import ProxyProperty
      from Products.Zuul.infos.device import DeviceInfo

      from ZenPacks.training.NetBotz.interfaces import INetBotzDeviceInfo

      class NetBotzDeviceInfo(DeviceInfo):
          implements(INetBotzDeviceInfo)

          temp_sensor_count = ProxyProperty('temp_sensor_count')

   1. Import the symbols we'll need to implement our Info adapter.

   2. Just like with the interface, we can extend `DeviceInfo` to get all of
      the standard `Device` functionality for free. Note that we're again
      using a best practice naming convention for our Info adapter. It should
      be the name of the model class suffixed with ``Info``.

   3. The `implements` line tells the system that this is an implementation of
      the interface we previously defined.

   4. We then use the helpful `ProxyProperty` method to provide the
      `temp_sensor_count` directly from the attribute by the same name on the
      actual model object.

      Using `ProxyProperty` in this way is equivalent to the following.

      .. sourcecode:: python

         @property
         def temp_sensor_count(self):
             return self._adapted.temp_sensor_count

         @temp_sensor_count.setter
         def temp_sensor_count(self, value):
             self._adapted.temp_sensor_count = value

      As you can see, `ProxyProperty` is shorter and cleaner even if you were
      only interested in the getter.


Register the Info Adapter
------------------------------------------------------------------------------

Now that you've defined your API interface and implemented the adapter to the
model class you have to register them with the system. Otherwise they won't be
used, and the system will use the standard `IDeviceInfo` interface and
`DeviceInfo` adapter because they're the next best thing.

Follow these steps to register your API interface and adapter.

1. Create ``$ZP_DIR/configure.zcml`` with the following contents.

   .. sourcecode:: xml

      <?xml version="1.0" encoding="utf-8"?>
      <configure xmlns="http://namespaces.zope.org/zope">

          <adapter
              provides=".interfaces.INetBotzDeviceInfo"
              for=".NetBotzDevice.NetBotzDevice"
              factory=".info.NetBotzDeviceInfo"
              />

      </configure>

   1. We open with a standard XML header and declaring that the default XML
      namespace (xmlns) for the document will be Zope's main namespace.

   2. Registering the Info adapter is the only thing we need in here at this
      point. We must specify the interface the adapter *provides*, the type of
      object that it provides the interface *for*, and finally the adapter
      *factory* itself. This is boilerplate stuff that you'll see in a lot of
      other areas in Zenoss and ZenPack development.


Test the API
------------------------------------------------------------------------------

We can now test the API using *zendmd*. Be sure to restart *zendmd* after
making changes to interfaces.py, info.py, or configure.zcml.

1. Execute the following snippet in *zendmd*.

   .. sourcecode:: python

      from Products.Zuul.interfaces import IInfo

      device = find("Netbotz01")
      device_info = IInfo(device)

      print device_info.temp_sensor_count

   1. Calling ``IInfo(device)`` will return the best `IInfo` adapter for
      `device` which is a `NetBotzDevice` instance in this case.

   You should see *14* printed if everything worked.



Change the Device Overview
==============================================================================

We've come a long way, but aside from going into *zendmd* to test that the API
works, we don't have much to show for it. The next step will be to show the
number of temperature sensors to users of the web interface. We'll replace the
*Memory/Swap* field in the top-left box of the device overview page with the
count of temperature sensors.

Follow these steps to customize the device Overview page.

1. Create a directory to store our ZenPack's JavaScript.

   .. sourcecode:: bash

      mkdir -p $ZP_DIR/browser/resources/js

2. Create *__init__.py* or *dunder-init* files.

   .. sourcecode:: bash

      touch $ZP_DIR/browser/__init__.py

3. Create ``$ZP_DIR/browser/resources/js/NetBotzDevice.js`` with the
   following contents.

   .. sourcecode:: javascript

      Ext.onReady(function() {
          var DEVICE_OVERVIEW_ID = 'deviceoverviewpanel_summary';
          Ext.ComponentMgr.onAvailable(DEVICE_OVERVIEW_ID, function(){
              var overview = Ext.getCmp(DEVICE_OVERVIEW_ID);
              overview.removeField('memory');

              overview.addField({
                  name: 'temp_sensor_count',
                  fieldLabel: _t('# Temperature Sensors')
              });
          });
      });

   1. Wait for Ext to be ready.
   2. Find the overview summary panel (top-left on Overview page)
   3. Remove the *memory* field.
   4. Add our *temp_sensor_count* field.

   Zenoss uses ExtJS as its JavaScript framework. You can find more in ExtJS's
   documentation about manipulating objects in this way.

4. Create ``$ZP_DIR/browser/configure.zcml`` with the following contents.

   .. sourcecode:: xml

      <?xml version="1.0" encoding="utf-8"?>
      <configure xmlns="http://namespaces.zope.org/browser">

          <resourceDirectory
              name="netbotz"
              directory="resources"
              />

          <viewlet
              name="js-netbotzdevice"
              paths="/++resource++netbotz/js/NetBotzDevice.js"
              weight="10"
              for="..NetBotzDevice.NetBotzDevice"
              manager="Products.ZenUI3.browser.interfaces.IJavaScriptSrcManager"
              class="Products.ZenUI3.browser.javascript.JavaScriptSrcBundleViewlet"
              permission="zope2.Public"
              />

      </configure>

   1. We open with a standard XML header and declaring that the default XML
      namespace (xmlns) for the document will be Zope's browser namespace.

   2. Next we register the *resourceDirectory*. This allows files within your
      ZenPack's */browser/resources/* directory to be served from URLs such as
      *http://zenoss.example.com/++resource++netbotz/filename.js*.

   3. Next we use a *viewlet* register a JavaScript snippet. You can see that
      we're referencing a URL within the *resourceDirectory* and limiting the
      snippet to only appear on pages where the context is a `NetBotzDevice`.
      This is the important part that keeps our customizations local to
      NetBotz devices.

5. Edit ``$ZP_DIR/configure.zcml``. Add the following section before the
   closing ``</configure>``.

   .. sourcecode:: xml

      <include package=".browser"/>

   This makes Zenoss load our ``browser/configure.zcml`` on startup.


Test the Device Overview
------------------------------------------------------------------------------

That's it. We can restart *zopectl* and navigate to our NetBotz device's
overview page in the web interface. You should see ``# Temperature Sensors``
label with a value of 14 at the bottom of the top-left panel.
