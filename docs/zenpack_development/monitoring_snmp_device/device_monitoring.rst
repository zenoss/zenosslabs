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

1. Navigate to the *Infrastructure* view.

2. Select the root of the *DEVICES* tree.

3. Click the *+* button at the bottom of the list to add a new organizer.

4. Set the *Name* to ``NetBotz`` then click *SUBMIT*.

   The new *NetBotz* device will now be selected. We'll want to check on some
   important configuration properties using the following steps.


Set Device Class Properties
------------------------------------------------------------------------------

1. Click the *DETAILS* button at the top of the list.

2. Select *Modeler Plugins*.

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

3. Remove *zenoss.snmp.RouteMap* from the list.

4. Click *Save*.

   Now you can see the *Path* at which our modeler plugin configuration is set
   has changed from */* to */NetBotz*. This allows us to know that regardless
   of what the user sets their default modeler plugins to in the system that
   NetBotz appliances will be collected using the set of modeler plugins we
   configure here.

5. Select *Configuration Properties* from the left navigation pane.

   There are a lot of configuration properties. You don't have to worry about
   understanding all of them. However, some will be critical to monitoring
   NetBotz appliances. We know that we're going to be using SNMP so let's make
   sure that it's enabled.

6. Find the *zSnmpMonitorIgnore* property and set its value to true.

7. Now set the value for *zSnmpMonitorIgnore* to false.

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

1. Make sure you've already created the ZenPack.

2. Make sure that you have the NetBotz device class selected in the
   *Infrastructure* view.

3. Choose *Add to ZenPack* from the gear menu in the bottom-left.

4. Select your NetBotz ZenPack then click *SUBMIT*.


Configure Monitoring Templates
==============================================================================

Before adding a monitoring template we should look to see what monitoring
templates are already being used in our new device class.


Validate Existing Monitoring Templates
------------------------------------------------------------------------------

We created the NetBotz device class directly within the root (or /) device
class. This means that we'll be inheriting the system default monitoring
templates and binding. Use the following steps to validate this.

1. Select the *NetBotz* device class in the *Infrastructure* view.

2. Choose *Bind Templates* from the gear menu in the bottom-left.

   You should only see ``Device (/Devices)`` in the *Selected* box. Depending
   on what other ZenPacks you have installed in the system you may see zero or
   more other templates listed in the *Available* box.


Now we investigate what this system default *Device* monitoring template does.

3. Click *CANCEL* on the *Bind Templates* dialog.

4. Click the *DETAILS* button at the top of the device class tree.

5. Select ``Device (/Devices)`` under *Monitoring Templates*.

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

1. Navigate to *Advanced* -> *Monitoring Templates*.

2. Click the *+* button in the bottom-left to add a template.

  1. Set the *Name* field to ``NetBotzDevice``.
  2. Set the *Template Path* field to */NetBotz*.

3. Click *SUBMIT*.

4. Bind this template to the *NetBotz* device class.

  1. Navigate to *Infrastructure*.
  2. Select the *NetBotz* device class.
  3. Choose *Bind Templates* from the gear menu in the bottom-left.
  4. Move *NetBotzDevice* from available to selected.
  5. Click *SAVE*.


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

1. Navigate to *Advanced* -> *Monitoring Templates*.

2. Expand *NetBotzDevice* then select */NetBotz*.

3. Click *+* on the *Data Sources* pane.

  1. Set *Name* to ``snmpInTotalReqVars``
  2. Set *Type* to ``SNMP``
  3. Click *SUBMIT*.

4. Double-click to edit the *snmpInTotalReqVars* datasource.

  1. Set *OID* to ``1.3.6.1.2.1.11.13.0``
  2. Click *SAVE*.

.. note::
   Best practice is to name SNMP datasources according to the name of the OID
   that's being polled from the MIB.


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

1. Double-click on the *snmpInTotalReqVars.snmpInTotalReqVars* datapoint.

  You may need to expand the *snmpInTotalReqVars* datasource first.

  1. Set *RRD Type* to *DERIVE*
  2. Set *RRD Minimum* to ``0``
  3. Click *SAVE*.

.. warning::

  It is very important to always set the *RRD Minimum* to ``0`` for *DERIVE*
  type datapoints. If you fail to do this, you will get large negative spikes
  in your data anytime the device reboots or the counter resets for any other
  reason.

  The only time you wouldn't set a minimum of 0 is when the value you're
  monitoring can increase and decrease and you're interested in tracking rates
  of negative change as well as rates of positive change.


Add a Threshold
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Now we can add a threshold to our monitoring template. Let's say we want to
raise a warning event anytime the rate of SNMP variable requests exceeds 10 per
second. This can be done with the following steps.

1. Click *+* on the *Thresholds* pane.

  1. Set *Name* to ``high SNMP variable request rate``
  2. Set *Type* to *MinMaxThreshold*
  3. Click *ADD*.

2. Double-click to edit the *high SNMP variable request rate* threshold.

  1. Drag the *snmpInTotalReqVars* datapoint to the left box.
  2. Set *Severity* to *Warning*
  3. Set *Maximum Value* to ``10``
  4. Set *Event Class* to */Perf/Snmp*
  5. Click *SAVE*.

.. note::

   A *MinMaxThreshold* can be used to handle a variety of conditions including
   over a maximum value, under a minimum value, outside a defined range or
   within a defined range. See the regular Zenoss documentation for how to use
   each of these options.


Add a Graph Definition
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Now we'll add a graph so the user will be able to see the trend of SNMP
variable requests per second over time. This can be done with the following
steps.

1. Click *+* on the *Graph Definitions* pane.

  1. Set *Name* to ``SNMP Rates``
  2. Click *SUBMIT*.

2. Double-click to edit the *SNMP Rates* graph definition.

  1. Set *Units* to ``requests/sec``
  2. Set *Min Y* to ``0``
  3. Click *SUBMIT*.

  .. note::

     Always set the units for your graph. Also set the minimum Y axis and
     maximum Y axis values if you know what the possible limits are for the
     data. This results in graphs that are easier to read.

     The format field should also be tweaked to best present the kind of data
     that is to be graphed. You can find more information on what can be used
     in the format field in the *RRDtool rrdgraph_graph* documentation under
     the *PRINT* section.

3. Select the *SNMP Rates* graph definition.

4. Choose *Manage Graph Points* from the gear menu.

  1. Choose *Data Point* from the *+* menu.
  2. Set *Data Point* to *snmpInTotalReqVars*
  3. Check *Include Related Thresholds*
  4. Click *SUBMIT*

5. Double-click to edit the *snmpInTotalReqVars* graph point.

  1. Set *Name* to ``Variables``
  2. Click *SAVE*.

  .. note::

     The name of a graph point is what is displayed for it in the graph legend.
     You should always choose something short that describes the data and makes
     sense in context of the units chosen above.


You can find many more notes about how to create monitoring templates along
with best practices on graph styling in the *ZenPack Standards Guide*.
