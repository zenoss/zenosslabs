==============================================================================
Monitoring an HTTP API
==============================================================================

The following sections will describe an efficient approach to monitoring data
via a HTTP API. We'll start by using zenpacklib to more easily extend the
Zenoss object model. Then we'll use a Python modeler plugin to fill out the
object model. Then we'll use PythonCollector to monitor for events, datapoints
and even to update the model.

For purposes of this guide we'll be building a ZenPack that monitors the
weather using The Weather Channel's Weather Underground API.

.. note::
   It is recommended that you have already finished the :ref:`snmp-index`
   section as it provides much more detail and troubleshooting advice. This
   exercise builds on that experience.

Exercises:

.. toctree::
   :maxdepth: 2

   wunderground_api
   using_zenpacklib
   python_modeler_plugin
   using_pythoncollector
   pythoncollector_events
   using_yaml_templates
   pythoncollector_datapoints
   pythoncollector_maps
