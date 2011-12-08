===============================================================================
ZenPack Taxonomy
===============================================================================

ZenPacks can be used to override almost any functionality of the Zenoss
platform, or to add any new features. This wide-open extensibility is much like
Firefox's add-on system and has the natural result of people building some
surprising things. For this reason it can be difficult to answer the question,
"What is a ZenPack?"

This document will outline the various ways ZenPacks can be classified to make
it easier to find the ZenPack you need, describe a ZenPack that already exists,
and to serve as an example for what is possible.

.. note::
    The sections below are currently under construction. Each section and item
    within will be explained.


ZenPack Classifications
===============================================================================

Every ZenPack will be classified using one of the items listed under each
section. See `Example ZenPack Classifications`_ for examples. The case of
technical complexity is slightly different. A ZenPack's total complexity score
could be the sum of each item it uses.


-------------------------------------------------------------------------------


.. _zp_class_functionality:

Functionality
-----------------------------------------------------------------------------

TODO: Define functionality.


.. _zp_class_functionality_monitoring:

Monitoring
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

TODO: Define functionality / monitoring.

Example: :ref:`zp_class_example_apachemonitor`


.. _zp_class_functionality_integration:

Integration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

TODO: Define functionality / integration.

Example: :ref:`zp_class_example_rancidintegrator`


.. _zp_class_functionality_platform:

Platform Extension
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

TODO: Define functionality / platform.

Example: :ref:`zp_class_example_distributedcollector`


-------------------------------------------------------------------------------


.. _zp_class_supportability:

Supportability
-----------------------------------------------------------------------------

TODO: Define supportability.


.. _zp_class_supportability_byzenoss:

Supported by Zenoss, Inc.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

TODO: Define supportability / byzenoss.

  Example: :ref:`zp_class_example_databasemonitor`


.. _zp_class_supportability_unsupported:

Not Supported
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

TODO: Define supportability / unsupported.

Example: :ref:`zp_class_example_zenodbc`


-------------------------------------------------------------------------------


.. _zp_class_maintainer:

Maintainer
-------------------------------------------------------------------------------

TODO: Define maintainer.

.. _zp_class_maintainer_engineering:

Zenoss Engineering
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

TODO: Define maintainer / engineering.

Example: :ref:`zp_class_example_impact`


.. _zp_class_maintainer_labs:

Zenoss Labs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

TODO: Define maintainer / labs.

Example: :ref:`zp_class_example_openstack`


.. _zp_class_maintainer_services:

Zenoss Services
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

TODO: Define maintainer / services.

Example: :ref:`zp_class_example_servicenowintegrator`


.. _zp_class_maintainer_partner:

Zenoss Partner
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

TODO: Define maintainer / partner.

Example: None


.. _zp_class_maintainer_community:

Zenoss Community
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

TODO: Define maintainer / community.

Example: :ref:`zp_class_example_zenodbc`


-------------------------------------------------------------------------------


.. _zp_class_availability:

Availability
-------------------------------------------------------------------------------

TODO: Define availability.

.. _zp_class_availability_opensource:

Open Source
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

TODO: Define availability / opensource.

Example: :ref:`zp_class_example_apachemonitor`


.. _zp_class_availability_bundled:

Bundled with Zenoss Subscription
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

TODO: Define availability / bundled.

Example: :ref:`zp_class_example_iismonitor`


.. _zp_class_availability_available:

Available with Zenoss Subscription
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

TODO: Define availability / available.

Example: :ref:`zp_class_example_databasemonitor`


.. _zp_class_availability_additionalcost:

Additional Cost with Zenoss Subscription
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

TODO: Define availability / additionalcost.

Example: :ref:`zp_class_example_impact`


-------------------------------------------------------------------------------


.. _zp_class_maturity:

Maturity
-------------------------------------------------------------------------------

TODO: Define maturity.

.. _zp_class_maturity_untested:

Untested
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

TODO: Define maturity / untested.

Example: None

.. _zp_class_maturity_tested:

Tested
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

TODO: Define maturity / tested.

Example: :ref:`zp_class_example_solarismonitor`


.. _zp_class_maturity_production:

Production
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

TODO: Define maturity / production.

Example: :ref:`zp_class_example_zenvmware`


-------------------------------------------------------------------------------


.. _zp_class_complexity:

Complexity
-------------------------------------------------------------------------------

TODO: Define complexity.

.. _zp_class_complexity_configuration:

Configuration (1)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Built entirely in the web interface. No programming knowledge required.

Example: :ref:`zp_class_example_iismonitor`


.. _zp_class_complexity_events:

Event Class Transforms and Mappings (2)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Built in the web interface. Basic Python knowledge required.

Example: :ref:`zp_class_example_openstack`


.. _zp_class_complexity_dsplugins:

Command DataSource Plugins (3)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Command datasource plugins can be written in any language and executed either on
the Zenoss server, or remotely using SSH. Without writing a custom parser (see
next item) they must write to STDOUT using either the Nagios or Cacti output
formats and exit using the appropriate Nagios or cacti exit code.

Example: :ref:`zp_class_example_apachemonitor`


.. _zp_class_complexity_dsparsers:

Command DataSource Parsers (4)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Command datasource parsers must be written in Python and conform to the Zenoss
`CommandParser` API. These parsers must be written to extract extended data from
the output of command datasource plugins (see previous item), or to handle
output that doesn't conform to the Nagios or Cacti output formats.

Example: :ref:`zp_class_example_solarismonitor`


.. _zp_class_complexity_datasources:

DataSource Types (5)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

TODO: Define complexity / datasources.

Example: :ref:`zp_class_example_apachemonitor`


.. _zp_class_complexity_ui:

User Interface (6)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

TODO: Define complexity / ui.

Example: :ref:`zp_class_example_servicenowintegrator`


.. _zp_class_complexity_impact:

Impact Adapters (7)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

TODO: Define complexity / impact.

Example: :ref:`zp_class_example_zenvmware`


.. _zp_class_complexity_etl:

ETL Adapters (8)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

TODO: Define complexity / etl.

Example: :ref:`zp_class_example_zenvmware`


.. _zp_class_complexity_modelers:

Modeler Plugins (SNMP, COMMAND or WMI) (9)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

TODO: Define complexity / modelers.

Example: :ref:`zp_class_example_solarismonitor`


.. _zp_class_complexity_pythonmodelers:

Modeler Plugins (Python) (10)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

TODO: Define complexity / pythonmodlers.

Example: :ref:`zp_class_example_openstack`


.. _zp_class_complexity_modelextensions:

Model Extensions (11)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

TODO: Define complexity / modelextensions.

Example: :ref:`zp_class_example_openstack`


.. _zp_class_complexity_daemons:

Daemons (12)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

TODO: Define complexity / daemons.

Example: :ref:`zp_class_example_zenvmware`


.. _zp_class_complexity_zenhubservices:

ZenHub Services (13)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

TODO: Define complexity / zenhubservices.

Example: :ref:`zp_class_example_zenvmware`


Example ZenPack Classifications
===============================================================================

.. _zp_class_example_apachemonitor:

ZenPacks.zenoss.ApacheMonitor
-------------------------------------------------------------------------------

=============================== ===============================================
Classification                  Value
=============================== ===============================================
:ref:`zp_class_functionality`   :ref:`zp_class_functionality_monitoring`
:ref:`zp_class_supportability`  :ref:`zp_class_supportability_byzenoss`
:ref:`zp_class_maintainer`      :ref:`zp_class_maintainer_engineering`
:ref:`zp_class_availability`    :ref:`zp_class_availability_opensource`
:ref:`zp_class_maturity`        :ref:`zp_class_maturity_production`
:ref:`zp_class_complexity`      `6` (:ref:`zp_class_complexity_configuration` + :ref:`zp_class_complexity_datasources`)
=============================== ===============================================


.. _zp_class_example_iismonitor:

ZenPacks.zenoss.IISMonitor
-------------------------------------------------------------------------------

=============================== ===============================================
Classification                  Value
=============================== ===============================================
:ref:`zp_class_functionality`   
:ref:`zp_class_supportability`  
:ref:`zp_class_maintainer`          
:ref:`zp_class_availability`    
:ref:`zp_class_maturity`        
:ref:`zp_class_complexity`      
=============================== ===============================================


.. _zp_class_example_distributedcollector:

ZenPacks.zenoss.DistributedCollector
-------------------------------------------------------------------------------

=============================== ===============================================
Classification                  Value
=============================== ===============================================
:ref:`zp_class_functionality`   
:ref:`zp_class_supportability`  
:ref:`zp_class_maintainer`          
:ref:`zp_class_availability`    
:ref:`zp_class_maturity`        
:ref:`zp_class_complexity`      
=============================== ===============================================


.. _zp_class_example_rancidintegrator:

ZenPacks.zenoss.RANCIDIntegrator
-------------------------------------------------------------------------------

=============================== ===============================================
Classification                  Value
=============================== ===============================================
:ref:`zp_class_functionality`   
:ref:`zp_class_supportability`  
:ref:`zp_class_maintainer`          
:ref:`zp_class_availability`    
:ref:`zp_class_maturity`        
:ref:`zp_class_complexity`      
=============================== ===============================================


.. _zp_class_example_databasemonitor:

ZenPacks.zenoss.DatabaseMonitor
-------------------------------------------------------------------------------

=============================== ===============================================
Classification                  Value
=============================== ===============================================
:ref:`zp_class_functionality`   
:ref:`zp_class_supportability`  
:ref:`zp_class_maintainer`          
:ref:`zp_class_availability`    
:ref:`zp_class_maturity`        
:ref:`zp_class_complexity`      
=============================== ===============================================


.. _zp_class_example_zenvmware:

ZenPacks.zenoss.ZenVMware
-------------------------------------------------------------------------------

=============================== ===============================================
Classification                  Value
=============================== ===============================================
:ref:`zp_class_functionality`   
:ref:`zp_class_supportability`  
:ref:`zp_class_maintainer`          
:ref:`zp_class_availability`    
:ref:`zp_class_maturity`        
:ref:`zp_class_complexity`      
=============================== ===============================================


.. _zp_class_example_solarismonitor:

ZenPacks.zenoss.SolarisMonitor
-------------------------------------------------------------------------------

=============================== ===============================================
Classification                  Value
=============================== ===============================================
:ref:`zp_class_functionality`   
:ref:`zp_class_supportability`  
:ref:`zp_class_maintainer`          
:ref:`zp_class_availability`    
:ref:`zp_class_maturity`        
:ref:`zp_class_complexity`      
=============================== ===============================================


.. _zp_class_example_impact:

ZenPacks.zenoss.Impact
-------------------------------------------------------------------------------

=============================== ===============================================
Classification                  Value
=============================== ===============================================
:ref:`zp_class_functionality`   
:ref:`zp_class_supportability`  
:ref:`zp_class_maintainer`          
:ref:`zp_class_availability`    
:ref:`zp_class_maturity`        
:ref:`zp_class_complexity`      
=============================== ===============================================


.. _zp_class_example_openstack:

ZenPacks.zenoss.OpenStack
-------------------------------------------------------------------------------

=============================== ===============================================
Classification                  Value
=============================== ===============================================
:ref:`zp_class_functionality`   
:ref:`zp_class_supportability`  
:ref:`zp_class_maintainer`          
:ref:`zp_class_availability`    
:ref:`zp_class_maturity`        
:ref:`zp_class_complexity`      
=============================== ===============================================


.. _zp_class_example_servicenowintegrator:

ZenPacks.zenoss.ServiceNowIntegrator
-------------------------------------------------------------------------------

=============================== ===============================================
Classification                  Value
=============================== ===============================================
:ref:`zp_class_functionality`   
:ref:`zp_class_supportability`  
:ref:`zp_class_maintainer`          
:ref:`zp_class_availability`    
:ref:`zp_class_maturity`        
:ref:`zp_class_complexity`      
=============================== ===============================================


.. _zp_class_example_zenodbc:

ZenPacks.community.ZenODBC
-------------------------------------------------------------------------------

=============================== ===============================================
Classification                  Value
=============================== ===============================================
:ref:`zp_class_functionality`   
:ref:`zp_class_supportability`  
:ref:`zp_class_maintainer`          
:ref:`zp_class_availability`    
:ref:`zp_class_maturity`        
:ref:`zp_class_complexity`      
=============================== ===============================================
