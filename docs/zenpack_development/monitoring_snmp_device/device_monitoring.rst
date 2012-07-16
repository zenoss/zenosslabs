==============================================================================
Device Monitoring
==============================================================================

This section will cover monitoring device-level metrics using SNMP. This
requires no code, and you can find instructions for doing it in the normal
Zenoss documentation. However, there are some extra considerations and steps
required to package your configuration in a ZenPack.


What Does "Device-Level" Mean?
==============================================================================

Understanding the difference between working at the *device-level* and
*component-level* can make working with, and developing for, Zenoss much easier
to understand. The Zenoss object model has two primary types of objects that
can be modeled and monitored.

- *Device*

  Devices are what you see on the Zenoss Infrastructure view in the web
  interface. If you see it in the Infrastructure view, it's a *Device*. If you
  don't, it's not. A *Device* has an *id* attribute that makes it unique in the
  system. It will have configuration properties associated with it either
  directly, or acquired from the device class within which it is contained. It
  will also have a *manageIp* attribute that Zenoss uses for modeling and
  monitoring.

  For purposes of this exercise, one of the most important configuration
  properties is zDeviceTemplates. This property controls which monitoring
  templates are bound to a device. Monitoring templates control what datapoints
  are collected, and monitoring templates bound to a device can only collect
  datapoints that only have a single instance per device. Memory utilization
  and load average are good examples. Other examples would be datapoints that
  have been aggregated to a single instance per device such as average CPU
  utilization across all CPU cores.

- *DeviceComponent*

  Device components are what you see if you drill-down into a device in the web
  interface, then choose one of the component types from the left navigation
  pane. Each row in the grid in the top-right pane is a component. Examples
  include things like network interface, file systems, disks and processes.
  These are things that have many instances per device.

  Device components, commonly just called "components", don't have their own
  configuration properties. They only acquire configuration properties through
  the device that contains them. They do not have a *manageIp* because they're
  typically managed through the same IP address and protocol(s) as the device
  that contains them.

  We'll cover how monitoring templates are bound to components in a later
  exercise. Monitoring templates bound to components are used to collect
  datapoints that have many instances per device. Examples include throughput
  on a specific network interface or utilization of a specific file system.


Creating a New Device Class
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

#. Click the *DETAILS* button at the top of the list.
#. Select *Modeler Plugins*.

   The modeler plugins are what model information about the device. We should
   see a list something like the following. This list is being acquired from
   the root (/ or /Devices) device class.

   - zenoss.snmp.NewDeviceMap
   - zenoss.snmp.DeviceMap
   - zenoss.snmp.InterfaceMap
   - zenoss.snmp.RouteMap

   This is a good basic list that uses standard MIB-2 support that works with most SNMP-enabled devices. However, it's unlikely that we care about the routing table on our environmental sensors, so there's no reason to model it.

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


Now that we've setup the NetBotz device class, it's time to add it to our
ZenPack using the following steps. Adding a device class to your ZenPack causes
all settings in that device class to be added to the ZenPack. This includes
modeler plugin configuration, configuration property values.

#. Make sure you've already created the ZenPack.

#. Make sure that you have the NetBotz device class selected in the
   *Infrastructure* view.

#. Choose *Add to ZenPack* from the gear menu in the bottom-left.

#. Select your NetBotz ZenPack then click *SUBMIT*.


Exporting the ZenPack
==============================================================================

Now that we've added our first object to the NetBotz ZenPack, we'll export it
to see how this gets packaged. Follow these steps to export the ZenPack.

#. Navigate to *Advanced* -> *ZenPacks* -> *NetBotz ZenPack* in the web
   interface.

#. Scroll to the bottom of the page to see what objects the ZenPack provides.

#. Choose *Export ZenPack* from the gear menu in the bottom-left of the screen.

#. Choose to only export and not download then click *OK*.


This will export everything under *ZenPack Provides* to a file within your
ZenPack's source called *objects.xml*. You can find this file in the following
path::

    $ZENHOME/ZenPacks/ZenPacks.yourname.NetBotz/ZenPacks/yourname/NetBotz/objects/objects.xml


Each time you add a new object to you ZenPack within the web interface, or
modify an object that's already contained within your ZenPack, you should
export the ZenPack again to update objects.xml. If you're using version control
on your ZenPack's source directory this would be a good time to commit the
resulting change to objects.xml.
