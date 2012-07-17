==============================================================================
SNMP Device Monitoring
==============================================================================

This section will cover monitoring device-level metrics using SNMP. This
requires no code, and you can find instructions for doing it in the normal
Zenoss documentation. However, there are some extra considerations and steps
required to package your configuration in a ZenPack.


Create a Device Class
==============================================================================

To support our new NetBotz environmental sensor device we will want to create a
new device class. This will give us full control over how these types of
devices are modeled and monitored. Use the following steps to add a new device
class.

#. Navigate to the *Infrastructure* view.

#. Select the root of the *DEVICES* tree.

#. Click the *+* button at the bottom of the list to add a new organizer.

#. Set the *Name* to ``NetBotz`` then click *SUBMIT*.

   The new *NetBotz* device will now be selected. We'll want to check on some
   important configuration properties using the following steps.


Set Device Class Properties
------------------------------------------------------------------------------

#. Click the *DETAILS* button at the top of the list.
#. Select *Modeler Plugins*.

   The modeler plugins are what model information about the device. We should
   see a list something like the following. This list is being acquired from
   the root (/ or /Devices) device class.

   - zenoss.snmp.NewDeviceMap
   - zenoss.snmp.DeviceMap
   - zenoss.snmp.InterfaceMap
   - zenoss.snmp.RouteMap

   This is a good basic list that uses standard MIB-2 support that works with
   most SNMP-enabled devices. However, it's unlikely that we care about the
   routing table on our environmental sensors, so there's no reason to model
   it.

#. Remove *zenoss.snmp.RouteMap* from the list.

#. Click *Save*.

   Now you can see the *Path* at which our modeler plugin configuration is set
   has changed from */* to */NetBotz*. This allows us to know that regardless
   of what the user sets their default modeler plugins to in the system that
   NetBotz appliances will be collected using the set of modeler plugins we
   configure here.

#. Select *Configuration Properties* from the left navigation pane.

   There are a lot of configuration properties. You don't have to worry about
   understanding all of them. However, some will be critical to monitoring
   NetBotz appliances. We know that we're going to be using SNMP so let's make
   sure that it's enabled.

#. Find the *zSnmpMonitorIgnore* property and set its value to true.
#. Now set the value for *zSnmpMonitorIgnore* to false.

   The reason for flipping the value back to it's original value is the same as
   saving the list of modeler plugins. While the system default is to have SNMP
   monitoring enabled, a user could easily disable it globally and cause our
   NetBotz monitoring to stop working. By flipping the value, we've set it
   locally within our device class and will prevent changes in the global
   default from affecting the operation of our ZenPack.


Add Device Class to ZenPack
------------------------------------------------------------------------------

Now that we've setup the NetBotz device class, it's time to add it to our
ZenPack using the following steps. Adding a device class to your ZenPack causes
all settings in that device class to be added to the ZenPack. This includes
modeler plugin configuration, configuration property values and monitoring
templates.

#. Make sure you've already created the ZenPack.

#. Make sure that you have the NetBotz device class selected in the
   *Infrastructure* view.

#. Choose *Add to ZenPack* from the gear menu in the bottom-left.

#. Select your NetBotz ZenPack then click *SUBMIT*.


Configure Monitoring Templates
==============================================================================

Before adding a monitoring template we should look to see what monitoring
templates are already being used in our new device class.


Validate Existing Monitoring Templates
------------------------------------------------------------------------------

We created the NetBotz device class directly within the root (or /) device
class. This means that we'll be inheriting the system default monitoring
templates and binding. Use the following steps to validate this.

#. Select the *NetBotz* device class in the *Infrastructure* view.

#. Choose *Bind Templates* from the gear menu in the bottom-left.

   You should only see ``Device (/Devices)`` in the *Selected* box. Depending
   on what other ZenPacks you have installed in the system you may see zero or
   more other templates listed in the *Available* box.


Now we investigate what this system default *Device* monitoring template does.

#. Click *CANCEL* on the *Bind Templates* dialog.

#. Click the *DETAILS* button at the top of the device class tree.

#. Select ``Device (/Devices)`` under *Monitoring Templates*.

   You'll see that there's a single SNMP datasource named sysUpTime. If you
   expand this datasource you will see that it contains a single datapoint
   which is also named sysUpTime. This single datapoint named the same as its
   containing datasource is always what you'll see for SNMP datasources. The
   reason for having the conceptual separation between datasources and
   datapoints is that other types of datasources such as COMMAND are capable of
   returning multiple datapoints.

   You'll note that this monitoring template has no threshold or graphs
   defined. This is unusual. Typically there'd be no reason to collect data
   that you weren't going to either threshold against or show in a graph. The
   *sysUpTime* datapoint is an exception because it is shown on a device's
   *Overview* page in the *Uptime* field and therefore doesn't need to be
   graphed.


Let's use ``snmpwalk`` to check if our NetBotz device supports *sysUpTime*. The
OID listed for the *sysUpTime* datasource is ``1.3.6.1.2.1.1.3.0`` so we run
the following command::

    # snmpwalk 127.0.1.113 1.3.6.1.2.1.1.3.0
    DISMAN-EVENT-MIB::sysUpTimeInstance = Timeticks: (7275488) 20:12:34.88


This response indicates that the NetBotz device does support the *sysUpTime*
OID. This is a mandatory field for SNMP devices to support so you will be able
to get it in almost all cases.


Add a Monitoring Template
------------------------------------------------------------------------------

Now that we've validated that the existing *Device* monitoring template will
work on our NetBotz device, we'll add another monitoring template to collect
additional information.

.. note::
   We could create a local copy of the *Device* monitoring template in the
   NetBotz device class and add new datasources, thresholds and graphs to it.
   However, this prevents us from taking advantage of changes made to the
   system default *Device* template in the future.


Follow these steps to create and bind a new template to the NetBotz device
class.

#. Navigate to *Advanced* -> *Monitoring Templates*.

#. Click the *+* button in the bottom-left to add a template.

  #. Set the *Name* field to ``NetBotzDevice``.
  #. Set the *Template Path* field to */NetBotz*.

#. Click *SUBMIT*.

#. Bind this template to the *NetBotz* device class.

  #. Navigate to *Infrastructure*.
  #. Select the *NetBotz* device class.
  #. Choose *Bind Templates* from the gear menu in the bottom-left.
  #. Move *NetBotzDevice* from available to selected.
  #. Click *SAVE*.


Build the Monitoring Template
------------------------------------------------------------------------------

Now that we've created the *NetBotzDevice* monitoring template and bound it to
the *NetBotz* device class, we need to add datasources, thresholds and graphs.
We don't already know what might be interesting to graph for each NetBotz
device, so let's go exploring with ``snmpwalk``::

    # snmpwalk 127.0.1.113
    SNMPv2-MIB::sysDescr.0 = STRING: Linux Netbotz01 2.4.26 #1 Wed Oct 31 18:09:53 CDT 2007 ppc
    SNMPv2-MIB::sysObjectID.0 = OID: NETBOTZV2-MIB::netBotz420ERack
    ... lots of lines removed ...
    SNMPv2-MIB::snmpInTotalReqVars.0 = Counter32: 4406
    ... and more removed ...

There isn't much of interest to collect at the device level. By "device-level"
I mean values that only have a single instance for the device. Typical examples
of these kinds of metrics would be memory utilization or the previous sysUpTime
example. With SNMP it can be easy to find these kinds of single-instance values
because their OID ends in ``.0`` as in ``SNMPv2-MIB::snmpInTotalReqVars.0``.

.. note::
   We'll get into monitoring multi-instance values in the component monitoring
   section.

Since there aren't any extremely interesting single-instance values to collect,
we'll collect that snmpInTotalReqVars for illustrative purposes. We'll need to
know the numeric OID for this value. Use snmptranslate to find it::

    # snmptranslate -On SNMPv2-MIB::snmpInTotalReqVars.0
    .1.3.6.1.2.1.11.13.0


Add an SNMP Datasource
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use the steps below to add an SNMP datasource for snmpInTotalReqVars.

#. Navigate to *Advanced* -> *Monitoring Templates*.

#. Expand *NetBotzDevice* then select */NetBotz*.

#. Click *+* on the *Data Sources* pane.

  #. Set *Name* to ``snmpInTotalReqVars``
  #. Set *Type* to ``SNMP``
  #. Click *SUBMIT*.

#. Double-click to edit the *snmpInTotalReqVars* datasource.

  #. Set *OID* to ``1.3.6.1.2.1.11.13.0``
  #. Click *SAVE*.


We now have a choice about how we want to handle the value that comes back from
polling that OID. As you can see above in the snmpwalk output, it is a
*Counter32* type. This means that it starts at 0 and, in this case, increments
each time an SNMP variable is requested. The most common way to handle counters
like these is as a delta. It's not very interesting to know how many variables
have been requested since the device last rebooted, but it might be interesting
to know how many variables are requested per second.

The default type for a datapoint is *GAUGE* which would record the actual value
you see in the snmpwalk output. If we'd rather monitor the rate of requests,
we'd change the datapoint type to *DERIVE* using the following steps.

#. Double-click on the *snmpInTotalReqVars.snmpInTotalReqVars* datapoint.

  You may need to expand the *snmpInTotalReqVars* datasource first.

  #. Set *RRD Type* to *DERIVE*
  #. Set *RRD Minimum* to ``0``
  #. Click *SAVE*.

.. warning::
  It is very important to always set the *RRD Minimum* to ``0`` for *DERIVE*
  type datapoints. If you fail to do this, you will get large negative spikes
  in your data anytime the device reboots or the counter resets for any other
  reason.

  The only time you wouldn't set a minimum of 0 is when the value you're
  monitoring can increase and decrease and you're interested in tracking rates
  of negative change as well as rates of positive change.
