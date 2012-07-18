==============================================================================
SNMP Device Modeling
==============================================================================

This section will cover creation of a custom *Device* subclass and modeling of
device attributes.


Create a Device Subclass
==============================================================================

A *Device* subclass should not be confused with a *device class*. In the
previous section we created the /NetBotz device class from the web interface.
Creating a *Device* subclass means to extend the actual Python class of a
*Device* object. You'd do this to add new attributes, methods or relationships
to special device types.

.. todo:: Break point. Pickup here when returning.