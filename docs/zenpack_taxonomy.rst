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

Functionality classifies the high-level type of feature(s) provided.
Specifically its type of interaction with the environment outside of the Zenoss
platform. The large majority of ZenPacks can be categorized with a single
functionality type, but some will encompass more than one type of high-level
functionality.


.. _zp_class_functionality_monitoring:

Monitoring
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Monitoring is one or more of status, event and performance collection. The
collection can be through active polling, passive receiving or both. A
monitoring ZenPack provides functionality to perform this collection for a
specific target technology.

Example: :ref:`zp_class_example_apachemonitor`


.. _zp_class_functionality_integration:

Integration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Integration is defined as being any interaction with systems outside of Zenoss
not deemed to be a :ref:`zp_class_functionality_monitoring` interaction.
Examples include pushing or pulling non-monitoring data to or from an external
system, or causing action in a remote system or allowing a remote system to
cause action within Zenoss.

Example: :ref:`zp_class_example_rancidintegrator`


.. _zp_class_functionality_platform:

Platform Extension
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A Zenoss platform extension is defined as any functionality that doesn't
interact with outside systems. The provided functionality is instead used
directly by users or by other parts of the Zenoss platform, or by other
ZenPacks.

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

Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Built entirely in the web interface. No programming knowledge required.

  :Complexity: 1
  :Skills: Zenoss
  :Example: :ref:`zp_class_example_iismonitor`


.. _zp_class_complexity_scripts:

Scripts
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Scripts can be written in any language and do anything. Since all Zenoss
customizations should be packaged as ZenPacks, they're only included in ZenPacks
as a packaging mechanism. They might not have any direct interaction with the
Zenoss platform.

  :Complexity: 2
  :Skills: Scripting (Any Language)
  :Example: :ref:`zp_class_example_rancidintegrator`


.. _zp_class_complexity_dsplugins:

Command DataSource Plugins
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Command datasource plugins can be written in any language and executed either on
the Zenoss server, or remotely using SSH. Without writing a custom parser (see
next item) they must write to STDOUT using either the Nagios or Cacti output
formats and exit using the appropriate Nagios or cacti exit code.

  :Complexity: 2
  :Skills: Scripting (Any Language)
  :Example: :ref:`zp_class_example_apachemonitor`


.. _zp_class_complexity_events:

Event Class Transforms and Mappings
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Built in the web interface. Basic Python knowledge required.

  :Complexity: 2
  :Skills: Zenoss, Basic Python
  :Example: :ref:`zp_class_example_openstack`


.. _zp_class_complexity_dsparsers:

Command DataSource Parsers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Command datasource parsers must be written in Python and conform to the Zenoss
`CommandParser` API. These parsers must be written to extract extended data from
the output of command datasource plugins (see previous item), or to handle
output that doesn't conform to the Nagios or Cacti output formats.

  :Complexity: 3
  :Skills: Zenoss, Python
  :Example: :ref:`zp_class_example_solarismonitor`


.. _zp_class_complexity_datasources:

DataSource Types
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

TODO: Define complexity / datasources.

  :Complexity: 4
  :Skills: Zenoss, ZCML, Python
  :Example: :ref:`zp_class_example_apachemonitor`


.. _zp_class_complexity_impact:

Impact Adapters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

TODO: Define complexity / impact.

  :Complexity: 4
  :Skills: Zenoss, ZCML, Python
  :Example: :ref:`zp_class_example_zenvmware`


.. _zp_class_complexity_etl:

ETL Adapters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

TODO: Define complexity / etl.

  :Complexity: 4
  :Skills: Zenoss, ZCML, Python
  :Example: :ref:`zp_class_example_zenvmware`


.. _zp_class_complexity_ui:

User Interface
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

TODO: Define complexity / ui.

  :Complexity: 5
  :Skills: Zenoss, ZCML, TAL, Python, JavaScript
  :Example: :ref:`zp_class_example_servicenowintegrator`


.. _zp_class_complexity_modelers:

Modeler Plugins (SNMP, COMMAND or WMI)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

TODO: Define complexity / modelers.

  :Complexity: 6
  :Skills: Zenoss, Python, (SNMP, Scripting or WMI)
  :Example: :ref:`zp_class_example_solarismonitor`


.. _zp_class_complexity_pythonmodelers:

Modeler Plugins (Python)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

TODO: Define complexity / pythonmodelers.

  :Complexity: 7
  :Skills: Zenoss, Python, Twisted
  :Example: :ref:`zp_class_example_openstack`


.. _zp_class_complexity_modelextensions:

Model Extensions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

TODO: Define complexity / modelextensions.

  :Complexity: 8
  :Skills: Zenoss, ZCML, Python, JavaScript
  :Example: :ref:`zp_class_example_openstack`


.. _zp_class_complexity_daemons:

Daemons
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

TODO: Define complexity / daemons.

  :Complexity: 9
  :Skills: Zenoss, Python, Twisted
  :Example: :ref:`zp_class_example_zenvmware`


.. _zp_class_complexity_platform:

Platform Extension
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

TODO: Define complexity / platform extension.

  :Complexity: 10
  :Skills: Zenoss, ZCML, Python, JavaScript, etc.
  :Example: :ref:`zp_class_example_distributedcollector`


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
:ref:`zp_class_complexity`      | :ref:`zp_class_complexity_configuration`
                                | :ref:`zp_class_complexity_dsplugins`
                                | :ref:`zp_class_complexity_datasources`
=============================== ===============================================


.. _zp_class_example_iismonitor:

ZenPacks.zenoss.IISMonitor
-------------------------------------------------------------------------------

=============================== ===============================================
Classification                  Value
=============================== ===============================================
:ref:`zp_class_functionality`   :ref:`zp_class_functionality_monitoring`
:ref:`zp_class_supportability`  :ref:`zp_class_supportability_byzenoss`
:ref:`zp_class_maintainer`      :ref:`zp_class_maintainer_engineering`
:ref:`zp_class_availability`    :ref:`zp_class_availability_bundled`
:ref:`zp_class_maturity`        :ref:`zp_class_maturity_production`
:ref:`zp_class_complexity`      | :ref:`zp_class_complexity_configuration`
=============================== ===============================================


.. _zp_class_example_distributedcollector:

ZenPacks.zenoss.DistributedCollector
-------------------------------------------------------------------------------

=============================== ===============================================
Classification                  Value
=============================== ===============================================
:ref:`zp_class_functionality`   :ref:`zp_class_functionality_platform`
:ref:`zp_class_supportability`  :ref:`zp_class_supportability_byzenoss`
:ref:`zp_class_maintainer`      :ref:`zp_class_maintainer_engineering`
:ref:`zp_class_availability`    :ref:`zp_class_availability_bundled`
:ref:`zp_class_maturity`        :ref:`zp_class_maturity_production`
:ref:`zp_class_complexity`      | :ref:`zp_class_complexity_configuration`
                                | :ref:`zp_class_complexity_ui`
                                | :ref:`zp_class_complexity_platform`
=============================== ===============================================


.. _zp_class_example_rancidintegrator:

ZenPacks.zenoss.RANCIDIntegrator
-------------------------------------------------------------------------------

=============================== ===============================================
Classification                  Value
=============================== ===============================================
:ref:`zp_class_functionality`   :ref:`zp_class_functionality_integration`
:ref:`zp_class_supportability`  :ref:`zp_class_supportability_byzenoss`
:ref:`zp_class_maintainer`      :ref:`zp_class_maintainer_engineering`
:ref:`zp_class_availability`    :ref:`zp_class_availability_bundled`
:ref:`zp_class_maturity`        :ref:`zp_class_maturity_production`
:ref:`zp_class_complexity`      | :ref:`zp_class_complexity_configuration`
                                | :ref:`zp_class_complexity_events`
                                | :ref:`zp_class_complexity_scripts`
=============================== ===============================================


.. _zp_class_example_databasemonitor:

ZenPacks.zenoss.DatabaseMonitor
-------------------------------------------------------------------------------

=============================== ===============================================
Classification                  Value
=============================== ===============================================
:ref:`zp_class_functionality`   :ref:`zp_class_functionality_monitoring`
:ref:`zp_class_supportability`  :ref:`zp_class_supportability_byzenoss`
:ref:`zp_class_maintainer`      :ref:`zp_class_maintainer_engineering`
:ref:`zp_class_availability`    :ref:`zp_class_availability_available`
:ref:`zp_class_maturity`        :ref:`zp_class_maturity_production`
:ref:`zp_class_complexity`      | :ref:`zp_class_complexity_configuration`
                                | :ref:`zp_class_complexity_dsplugins`
                                | :ref:`zp_class_complexity_datasources`
=============================== ===============================================


.. _zp_class_example_zenvmware:

ZenPacks.zenoss.ZenVMware
-------------------------------------------------------------------------------

=============================== ===============================================
Classification                  Value
=============================== ===============================================
:ref:`zp_class_functionality`   :ref:`zp_class_functionality_monitoring`
:ref:`zp_class_supportability`  :ref:`zp_class_supportability_byzenoss`
:ref:`zp_class_maintainer`      :ref:`zp_class_maintainer_engineering`
:ref:`zp_class_availability`    :ref:`zp_class_availability_bundled`
:ref:`zp_class_maturity`        :ref:`zp_class_maturity_production`
:ref:`zp_class_complexity`      | :ref:`zp_class_complexity_configuration`
                                | :ref:`zp_class_complexity_events`
                                | :ref:`zp_class_complexity_datasources`
                                | :ref:`zp_class_complexity_ui`
                                | :ref:`zp_class_complexity_impact`
                                | :ref:`zp_class_complexity_etl`
                                | :ref:`zp_class_complexity_modelextensions`
                                | :ref:`zp_class_complexity_daemons`
=============================== ===============================================


.. _zp_class_example_solarismonitor:

ZenPacks.zenoss.SolarisMonitor
-------------------------------------------------------------------------------

=============================== ===============================================
Classification                  Value
=============================== ===============================================
:ref:`zp_class_functionality`   :ref:`zp_class_functionality_monitoring`
:ref:`zp_class_supportability`  :ref:`zp_class_supportability_byzenoss`
:ref:`zp_class_maintainer`      :ref:`zp_class_maintainer_engineering`
:ref:`zp_class_availability`    :ref:`zp_class_availability_bundled`
:ref:`zp_class_maturity`        :ref:`zp_class_maturity_production`
:ref:`zp_class_complexity`      | :ref:`zp_class_complexity_configuration`
                                | :ref:`zp_class_complexity_dsplugins`
                                | :ref:`zp_class_complexity_dsparsers`
                                | :ref:`zp_class_complexity_modelers`
=============================== ===============================================


.. _zp_class_example_impact:

ZenPacks.zenoss.Impact
-------------------------------------------------------------------------------

=============================== ===============================================
Classification                  Value
=============================== ===============================================
:ref:`zp_class_functionality`   :ref:`zp_class_functionality_platform`
:ref:`zp_class_supportability`  :ref:`zp_class_supportability_byzenoss`
:ref:`zp_class_maintainer`      :ref:`zp_class_maintainer_engineering`
:ref:`zp_class_availability`    :ref:`zp_class_availability_additionalcost`
:ref:`zp_class_maturity`        :ref:`zp_class_maturity_production`
:ref:`zp_class_complexity`      | :ref:`zp_class_complexity_configuration`
                                | :ref:`zp_class_complexity_ui`
                                | :ref:`zp_class_complexity_impact`
                                | :ref:`zp_class_complexity_daemons`
                                | :ref:`zp_class_complexity_platform`
=============================== ===============================================


.. _zp_class_example_openstack:

ZenPacks.zenoss.OpenStack
-------------------------------------------------------------------------------

=============================== ===============================================
Classification                  Value
=============================== ===============================================
:ref:`zp_class_functionality`   :ref:`zp_class_functionality_monitoring`
:ref:`zp_class_supportability`  :ref:`zp_class_supportability_byzenoss`
:ref:`zp_class_maintainer`      :ref:`zp_class_maintainer_labs`
:ref:`zp_class_availability`    :ref:`zp_class_availability_opensource`
:ref:`zp_class_maturity`        :ref:`zp_class_maturity_production`
:ref:`zp_class_complexity`      | :ref:`zp_class_complexity_configuration`
                                | :ref:`zp_class_complexity_events`
                                | :ref:`zp_class_complexity_dsplugins`
                                | :ref:`zp_class_complexity_dsparsers`
                                | :ref:`zp_class_complexity_ui`
                                | :ref:`zp_class_complexity_impact`
                                | :ref:`zp_class_complexity_pythonmodelers`
                                | :ref:`zp_class_complexity_modelextensions`
=============================== ===============================================


.. _zp_class_example_servicenowintegrator:

ZenPacks.zenoss.ServiceNowIntegrator
-------------------------------------------------------------------------------

=============================== ===============================================
Classification                  Value
=============================== ===============================================
:ref:`zp_class_functionality`   :ref:`zp_class_functionality_integration`
:ref:`zp_class_supportability`  :ref:`zp_class_supportability_byzenoss`
:ref:`zp_class_maintainer`      :ref:`zp_class_maintainer_services`
:ref:`zp_class_availability`    :ref:`zp_class_availability_available`
:ref:`zp_class_maturity`        :ref:`zp_class_maturity_production`
:ref:`zp_class_complexity`      | :ref:`zp_class_complexity_configuration`
                                | :ref:`zp_class_complexity_ui`
                                | :ref:`zp_class_complexity_modelextensions`
                                | :ref:`zp_class_complexity_daemons`
=============================== ===============================================


.. _zp_class_example_zenodbc:

ZenPacks.community.ZenODBC
-------------------------------------------------------------------------------

=============================== ===============================================
Classification                  Value
=============================== ===============================================
:ref:`zp_class_functionality`   :ref:`zp_class_functionality_platform`
:ref:`zp_class_supportability`  :ref:`zp_class_supportability_unsupported`
:ref:`zp_class_maintainer`      :ref:`zp_class_maintainer_community`
:ref:`zp_class_availability`    :ref:`zp_class_availability_opensource`
:ref:`zp_class_maturity`        :ref:`zp_class_maturity_production`
:ref:`zp_class_complexity`      | :ref:`zp_class_complexity_datasources`
                                | :ref:`zp_class_complexity_pythonmodelers`
=============================== ===============================================
