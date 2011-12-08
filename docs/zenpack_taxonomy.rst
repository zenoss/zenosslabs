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

  :Example: :ref:`zp_class_example_apachemonitor`


.. _zp_class_functionality_integration:

Integration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Integration is defined as being any interaction with systems outside of Zenoss
not deemed to be a :ref:`zp_class_functionality_monitoring` interaction.
Examples include pushing or pulling non-monitoring data to or from an external
system, or causing action in a remote system or allowing a remote system to
cause action within Zenoss.

  :Example: :ref:`zp_class_example_rancidintegrator`


.. _zp_class_functionality_platform:

Platform Extension
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A Zenoss platform extension is defined as any functionality that doesn't
interact with outside systems. The provided functionality is instead used
directly by users or by other parts of the Zenoss platform, or by other
ZenPacks.

  :Example: :ref:`zp_class_example_distributedcollector`


-------------------------------------------------------------------------------


.. _zp_class_supportability:

Supportability
-----------------------------------------------------------------------------

Supportability defines what organization provides usage, troubleshooting, and
defect and enhancement resolution for a ZenPack.


.. _zp_class_supportability_byzenoss:

Supported by Zenoss
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ZenPacks are supported by Zenoss, Inc.


  :Example: :ref:`zp_class_example_databasemonitor`


.. _zp_class_supportability_unsupported:

Not Supported
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ZenPacks are not supported by Zenoss, Inc. Support may be available through
partners, other organizations or the Zenoss community.

  :Example: :ref:`zp_class_example_zenodbc`


-------------------------------------------------------------------------------


.. _zp_class_maintainer:

Maintainer
-------------------------------------------------------------------------------

The maintainer of a ZenPack is the organization or individual that controls the
code repository for a ZenPack and is the gate for all changes including defect
and enhancement resolution. A ZenPack can have multiple maintainers.

.. _zp_class_maintainer_engineering:

Zenoss Engineering
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Maintained by the product engineering organization at Zenoss, Inc.

  :Example: :ref:`zp_class_example_impact`


.. _zp_class_maintainer_labs:

Zenoss Labs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Maintained by the labs organization at Zenoss, Inc.

  :Example: :ref:`zp_class_example_openstack`


.. _zp_class_maintainer_services:

Zenoss Services
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Maintained by the services organization at Zenoss, Inc.

  :Example: :ref:`zp_class_example_servicenowintegrator`


.. _zp_class_maintainer_partner:

Zenoss Partner
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Maintained by a Zenoss, Inc. partner organizations.

  :Example: None


.. _zp_class_maintainer_community:

Zenoss Community
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Maintained by a member of the Zenoss community.

  :Example: :ref:`zp_class_example_zenodbc`


-------------------------------------------------------------------------------


.. _zp_class_availability:

Availability
-------------------------------------------------------------------------------

Who has access, license and permission to use the ZenPack. The subtypes are
mutually exclusive.


.. _zp_class_availability_opensource:

Open Source
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ZenPack source and packages are available as free open source. Designed to
function properly on a Zenoss system with or without commercial-only ZenPacks
installed.

  :Example: :ref:`zp_class_example_apachemonitor`


.. _zp_class_availability_bundled:

Bundled with Zenoss Subscription
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ZenPack packages are available at no extra cost to anyone with a Zenoss
subscription, and installed by default. May have dependencies on
:ref:`zp_class_availability_opensource` ZenPacks or other ZenPacks that are
:ref:`zp_class_availability_bundled`.

  :Example: :ref:`zp_class_example_iismonitor`


.. _zp_class_availability_available:

Available with Zenoss Subscription
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ZenPack packages are available at no extra cost to anyone with a Zenoss
subscription, but are not installed by default. May have dependencies on
:ref:`zp_class_availability_opensource` ZenPacks or other ZenPacks that are
:ref:`zp_class_availability_bundled`.

  :Example: :ref:`zp_class_example_databasemonitor`


.. _zp_class_availability_additionalcost:

Additional Cost with Zenoss Subscription
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ZenPack packages are available at an additional cost on top of an existing
Zenoss subscription. May have dependencies on
:ref:`zp_class_availability_opensource` ZenPacks, ZenPacks that are
:ref:`zp_class_availability_bundled`, or other ZenPacks that are
:ref:`zp_class_availability_additionalcost`.

  :Example: :ref:`zp_class_example_impact`


-------------------------------------------------------------------------------


.. _zp_class_maturity:

Maturity
-------------------------------------------------------------------------------

The level of automated, manual and field testing A ZenPack has. The subtypes are
not mutually exclusive. For instance, a ZenPack could theoretically be untested
and deployed in multiple production environments.


.. _zp_class_maturity_untested:

Untested
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Insufficient automated testing to qualify as
:ref:`zp_class_maturity_autotested`, and insufficient manual testing to qualify
as :ref:`zp_class_maturity_qatested`.

  :Example: :ref:`zp_class_example_zenodbc`


.. _zp_class_maturity_autotested:

Automatically Tested
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Standard automated testing passes plus a minimum of 90% unit test code coverage
with all tests passing.

  :Example: :ref:`zp_class_example_solarismonitor`


.. _zp_class_maturity_qatested:

Q.A. Tested
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Tested, and passed, by the quality assurance group of Zenoss, Inc.

  :Example: :ref:`zp_class_example_solarismonitor`


.. _zp_class_maturity_production:

Production
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In use with no significant issues in more than one production Zenoss deployment.

  :Example: :ref:`zp_class_example_zenvmware`


-------------------------------------------------------------------------------


.. _zp_class_complexity:

Complexity
-------------------------------------------------------------------------------

Defined by the technical difficulty of implementing specific types of
functionality within the ZenPack. The subtypes are not mutually exclusive, and
most ZenPacks will implement multiple types of functionality as defined below. A
rough total complexity score could be created for each ZenPack by summing the
complexity score of all implemented subtypes.


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

When a new datasource is added in the web interface you must choose the type.
Creating a DataSource type in a ZenPack is a way to add new types to this list.
The `ApacheMonitor` ZenPack listed as the example below adds the ability to
collect performance metrics from an Apache httpd server using `mod_status`.

New DataSource types are written in Python and must subclass ``RRDDataSource``
or one of its existing subclasses. Additionally an API adapter must also be
written in Python to define the user interface to the datasource properties.

  :Complexity: 4
  :Skills: Zenoss, ZCML, Python
  :Example: :ref:`zp_class_example_apachemonitor`


.. _zp_class_complexity_impact:

Impact Adapters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

There are three types of impact adapters. All are written in Python and added to
the system configuration through ZCML directives.

The first is a state provider. These implement the ``IStateProvider`` interface
and allow manipulation of how a given node type's state within the impact graph
is calculated.

The second is a relations provider. These implement the
``IRelationshipDataProvider`` interface and allow manipulation of what other
nodes a given node type impacts, and what other nodes impact it.

The third is a triggers provider. These implement the ``INodeTriggers``
interface and allow manipulation of the default impact policies set on a given
type of node.

  :Complexity: 5
  :Skills: Zenoss, ZCML, Python
  :Example: :ref:`zp_class_example_zenvmware`


.. _zp_class_complexity_etl:

ETL Adapters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ETL is used to export model, performance and event data from a Zenoss instance
to a Zenoss Analytics instance. However, ETL adapters only need to be written to
manipulate the *model* data that is exported. There are two types of ETL
adapters. They're both written in Python and added to the system configuration
through ZCML directives.

The first type is a reportable. These implement the ``IReportable`` interface
and allow precise control over which properties of an object type are exported,
and how they're named and manipulated for export.

The second type is a reportable factory. These implement the
``IReportableFactory`` interface and all manipulation of which objects are
considered for export. By default all devices and components are considered for
extraction so a reportable factory is usually only used when fine-grained
control over the relationships between these objects is needed.

  :Complexity: 4
  :Skills: Zenoss, ZCML, Python
  :Example: :ref:`zp_class_example_zenvmware`


.. _zp_class_complexity_ui:

User Interface
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Modifications to the existing user interface, or entirely new sections of user
interface. The difficulty of these changes varies considerably. See the `Skills`
field below for the range of skills that could be required to make these kinds
of changes.

The `ServiceNowIntegrator` example given below adds a new button to the event
console that pops up a new dialog box with some custom options available. Only
ZCML and JavaScript were required for this type of change.

TAL is usually only required when editing or creating old-style pages that
aren't entirely built using ExtJS.

  :Complexity: 5
  :Skills: Zenoss, ZCML, TAL, JavaScript, ExtJS
  :Example: :ref:`zp_class_example_servicenowintegrator`


.. _zp_class_complexity_modelers:

Modeler Plugins - SNMP, COMMAND, WMI
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Modeler plugins provide the mapping between data collected from the environment
and the Zenoss model. In the case where the data can be collected using SNMP,
COMMAND (run a command remotely via SSH) or WMI, there is existing
infrastructure to make these tasks easier. However, the modeler plugins are
still written in Python.

If collecting using SNMP the ``SnmpPlugin`` class can be extended to do the hard
parts of SNMP gets or walks for you. If collecting by running a command on a
remote system via SSH, the ``CommandPlugin`` class can be extended to do the
hard parts of SSH and output parsing for you. If collecting from a Windows
system using WMI, the ``WmiPlugin`` class can be extended to do the hard parts
of WQL querying for you.

The only significant logic that must be implemented in these cases is turning
the returned data structures into ``ObjectMap`` and ``RelationshipMap`` objects
to apply to the Zenoss model.

  :Complexity: 6
  :Skills: Zenoss, Python, (SNMP, Scripting or WMI)
  :Example: :ref:`zp_class_example_solarismonitor`


.. _zp_class_complexity_pythonmodelers:

Modeler Plugins - Python
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

See :ref:`zp_class_complexity_modelextensions` above for what modeler plugins
are. Python modeler plugins only differ in that you extend the ``PythonPlugin``
class, and must implement the collection logic in addition to the processing
logic.

The ``collect`` method implementation may return data normally, or it may return
a Twisted ``deferred`` to take advantage of the asynchronous modeling engine. It
is recommended to use the deferred approach whenever possible to avoid blocking
the `zenmodeler` daemon while the ``collect`` method executes.

  :Complexity: 7
  :Skills: Zenoss, Python, Twisted
  :Example: :ref:`zp_class_example_openstack`


.. _zp_class_complexity_modelextensions:

Model Extensions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When the standard model of the Zenoss platform doesn't cover an object or
property you need in your ZenPack, the model can be extended. Existing model
classes such as Device, FileSystem or IpInterface can be extended, and entirely
new types of components can be created.

The typical requirements for extended the model include at least the following
steps.

1. Create a Python class
2. Create an API interface and adapter
3. Wire up the API with ZCML
4. Write JavaScript to tailor the display of your component
5. Write a :ref:`modeler plugin <zp_class_complexity_modelers>`

  :Complexity: 8
  :Skills: Zenoss, ZCML, Python, JavaScript
  :Example: :ref:`zp_class_example_openstack`


.. _zp_class_complexity_daemons:

Daemons
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A new daemon must be written only if none of the existing daemons can perform
the task required by your ZenPack. The ``zencommand`` daemon is the usual last
resort for custom collection requirements if none of the more specialized
daemons will work. See :ref:`zp_class_complexity_dsplugins` and
:ref:`zp_class_complexity_dsparsers` for what can be done by ``zencommand``.

There is a common collector framework that should be used to perform much of the
typical daemon functionality such as configuration and scheduling in a
consistent way. To use this you should create a ``CollectorDaemon`` object,
configure it with a class that implements the ``ICollectorPreferences``
interface and create a task class that implements the ``IScheduledTask``
interface.

In almost all cases you will also need to create a ZenHub service to build the
configuration for your new daemon. This service should subclass ``HubService``
or one of its existing more specialized subclasses.

  :Complexity: 9
  :Skills: Zenoss, Python, Twisted
  :Example: :ref:`zp_class_example_zenvmware`


.. _zp_class_complexity_platform:

Platform Extension
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Platform extensions are any implementations added to a ZenPack that doesn't fall
into any of the previously-defined complexity subtypes. Due to the flexibility
of ZenPacks, these could be almost anything.

The `DistributedCollector` example given below falls into this category because
it extends the simple flat collector structure in the core Zenoss platform to be
a tiered hub and collector structure. It also adds extensive hub and collector
management capabilities.

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
:ref:`zp_class_maturity`        | :ref:`zp_class_maturity_qatested`
                                | :ref:`zp_class_maturity_production`
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
:ref:`zp_class_maturity`        | :ref:`zp_class_maturity_autotested`
                                | :ref:`zp_class_maturity_qatested`
                                | :ref:`zp_class_maturity_production`
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
:ref:`zp_class_maturity`        | :ref:`zp_class_maturity_autotested`
                                | :ref:`zp_class_maturity_qatested`
                                | :ref:`zp_class_maturity_production`
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
:ref:`zp_class_maturity`        | :ref:`zp_class_maturity_untested`
                                | :ref:`zp_class_maturity_production`
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
:ref:`zp_class_maturity`        | :ref:`zp_class_maturity_qatested`
                                | :ref:`zp_class_maturity_production`
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
:ref:`zp_class_maturity`        | :ref:`zp_class_maturity_qatested`
                                | :ref:`zp_class_maturity_production`
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
:ref:`zp_class_maturity`        | :ref:`zp_class_maturity_autotested`
                                | :ref:`zp_class_maturity_qatested`
                                | :ref:`zp_class_maturity_production`
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
:ref:`zp_class_maturity`        | :ref:`zp_class_maturity_autotested`
                                | :ref:`zp_class_maturity_qatested`
                                | :ref:`zp_class_maturity_production`
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
:ref:`zp_class_maturity`        | :ref:`zp_class_maturity_untested`
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
:ref:`zp_class_maturity`        | :ref:`zp_class_maturity_untested`
                                | :ref:`zp_class_maturity_production`
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
:ref:`zp_class_maturity`        | :ref:`zp_class_maturity_untested`
                                | :ref:`zp_class_maturity_production`
:ref:`zp_class_complexity`      | :ref:`zp_class_complexity_datasources`
                                | :ref:`zp_class_complexity_pythonmodelers`
=============================== ===============================================
