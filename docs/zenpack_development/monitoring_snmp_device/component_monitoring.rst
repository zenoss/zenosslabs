==============================================================================
Component Monitoring
==============================================================================

This section covers monitoring component metrics using SNMP. I assume that
you've completed the *Component Modeling* steps and now have temperature
sensor components modeled for the NetBotz device. Currently there will be no
graphs for these temperature sensors.

We will add collection, thresholding and graphing for the temperature monitored
by each sensor.


Find the SNMP OID
==============================================================================

In the *Component Modeling* section we used `smidump` and `snmpwalk` to find
which values would be useful to model, and which would be useful to monitor. We
found `tempSensorValue` to be the best OID to use for monitoring a sensor's
current temperature.

Let's use `snmpwalk` again to see what `tempSensorValue` looks like for all of
the sensors on our NetBotz device.

.. sourcecode:: bash

    snmpwalk 127.0.1.113 NETBOTZV2-MIB::tempSensorValueStr

This gives of the current temperature (in celsius) for each sensor::

    NETBOTZV2-MIB::tempSensorValueStr.21604919 = STRING: 26.500000
    NETBOTZV2-MIB::tempSensorValueStr.1095346743 = STRING: 27.000000
    NETBOTZV2-MIB::tempSensorValueStr.1382714817 = STRING: 22.100000
    NETBOTZV2-MIB::tempSensorValueStr.1382714818 = STRING: 21.100000
    NETBOTZV2-MIB::tempSensorValueStr.1382714819 = STRING: 19.600000
    NETBOTZV2-MIB::tempSensorValueStr.1382714820 = STRING: 19.900000
    NETBOTZV2-MIB::tempSensorValueStr.1382714833 = STRING: 20.500000
    NETBOTZV2-MIB::tempSensorValueStr.1382714834 = STRING: 20.100000
    NETBOTZV2-MIB::tempSensorValueStr.1382714865 = STRING: 19.700000
    NETBOTZV2-MIB::tempSensorValueStr.1382714866 = STRING: 20.500000
    NETBOTZV2-MIB::tempSensorValueStr.1382714867 = STRING: 20.100000
    NETBOTZV2-MIB::tempSensorValueStr.1382714868 = STRING: 20.000000
    NETBOTZV2-MIB::tempSensorValueStr.2169088567 = STRING: 26.600000
    NETBOTZV2-MIB::tempSensorValueStr.3242830391 = STRING: 27.400000

As we go on to add a monitoring template below, we'll need to know what OID to
poll to collect this value. The key to determining this for components with an
`snmpindex` attribute like `TemperatureSensor` has is to find the OID for the
values above and remove the SNMP index from the end of it. Let's use
`snmptranslate` to do this.

.. sourcecode:: bash

    snmptranslate -On NETBOTZV2-MIB::tempSensorValueStr

This results in the following output::

    .1.3.6.1.4.1.5528.100.4.1.1.1.7

This OID (minus the leading .) is what we'll need.


Add a Monitoring Template
==============================================================================

In the *Component Modeling* section we added a `getRRDTemplateName` method to
our `TemperatureSensor` class. We made this method return
*TemperatureSensor*. This means that each temperature sensor will have a
template by this name automatically bound to it.

This makes life easy when adding a monitoring template to be used. All we have
to do is create a monitoring template named *TemperatureSensor* in the
*/NetBotz* device class.

1. Navigate to *Advanced* -> *Monitoring Templates*.

2. Add a template.

   1. Click the *+* in the bottom-left of the template list.
   2. Set *Name* to ``TemperatureSensor``
   3. Set *Template Path* to */NetBotz*
   4. Click *SUBMIT*

3. Add a data source.

   1. Click the *+* at the top of the *Data Sources* panel.
   2. Set *Name* to ``tempSensorValueStr``
   3. Set *Type* to *SNMP*
   4. Click *SUBMIT*
   5. Double-click to edit the *tempSensorValueStr* data source.
   6. Set *OID* to ``1.3.6.1.4.1.5528.100.4.1.1.1.7``
   7. Click *SAVE*

5. Add a threshold.

   1. Click the *+* at the top of the *Thresholds* panel.
   2. Set *Name* to ``high temperature``
   3. Set *Type* to *MinMaxThreshold*
   4. Click *ADD*
   5. Double-click to edit the *high temperature* threshold.
   6. Move the datapoint to the list on the right.
   7. Set *Maximum Value* to ``32``
   8. Set *Event Class* to */Environ*
   9. Click *SAVE*

6. Add a graph.

   1. Click the *+* at the top of the *Graph Definitions* panel.
   2. Set *Name* to ``Temperature``
   3. Click *SUBMIT*
   4. Double-click to edit the *Temperature* graph.
   5. Set *Units* to ``degrees c.``
   6. Click *SUBMIT*

7. Add a graph point.

   1. Click to select the *Temperature* graph.
   2. Choose *Manage Graph Points* from the gear menu.
   3. Choose *Data Point* from the *+* menu.
   4. Choose *tempSensorValueStr* then click *SUBMIT*
   5. Double-click to edit the *tempSensorValueStr* graph point.
   6. Set *Name* to ``Temperature``
   7. Set *Format* to ``%7.2lf``
   8. Click *SAVE* then *SAVE* again.


Test Monitoring Template
------------------------------------------------------------------------------

You can now refer back to the *Test Monitoring Template* section of
*Device Monitoring* for using `zenperfsnmp` to test the data point collection
aspect of your monitoring template.

You can verify that your monitoring template is getting bound to each
temperature sensor properly by navigating to one of the temperature sensors in
the web interface and choosing *Templates* from it's *Display* drop-down box.
Furthermore, you can verify that your *Temperature* graph is shown when
choosing *Graphs* from the temperature sensor's *Display* drop-down.
