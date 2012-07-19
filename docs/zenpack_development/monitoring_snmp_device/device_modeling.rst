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
*$ZP_DIR_TOP* and *$ZP_DIR* environment variables have been set as follows::

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

.. todo:: Break point. Pick up here when returning.
