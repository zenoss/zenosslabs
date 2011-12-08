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

.. _zp_class_functionality:

Functionality
-------------------------------------------------------------------------------

.. _zp_class_functionality_monitoring:

* *Monitoring*

  Example: `ZenPacks.zenoss.ApacheMonitor`_

.. _zp_class_functionality_integration:

* *Integration*

  Example: `ZenPacks.zenoss.RANCIDIntegrator`_

.. _zp_class_functionality_platform:

* *Platform Extension*

  Example: `ZenPacks.zenoss.DistributedCollector`_

.. _zp_class_supportability:

Supportability
-------------------------------------------------------------------------------

* *Supported by Zenoss, Inc.*

  Example: `ZenPacks.zenoss.DatabaseMonitor`_

* *Not Supported*

  Example: `ZenPacks.community.ZenODBC`_

.. _zp_class_author:

Author
-------------------------------------------------------------------------------

* Zenoss Engineering

  Example: `ZenPacks.zenoss.Impact`_

* Zenoss Labs

  Example: `ZenPacks.zenoss.OpenStack`_

* Zenoss Services

  Example: `ZenPacks.zenoss.ServiceNowIntegrator`_

* Zenoss Partner

  Example: None

* Zenoss Community

  Example: `ZenPacks.community.ZenODBC`_

.. _zp_class_availability:

Availability
-------------------------------------------------------------------------------

#. *Open Source*

   Example: `ZenPacks.zenoss.ApacheMonitor`_

#. *Bundled with Zenoss Subscription*

   Example: `ZenPacks.zenoss.IISMonitor`_

#. *Available with Zenoss Subscription*

   Example: `ZenPacks.zenoss.DatabaseMonitor`_

#. *Additional Cost with Zenoss Subscription*

   Example: `ZenPacks.zenoss.Impact`_

.. _zp_class_maturity:

Maturity
-------------------------------------------------------------------------------

#. *Untested*

   Example: None

#. *Fully Tested*

   Example: `ZenPacks.zenoss.SolarisMonitor`_

#. *In Production*

   Example: `ZenPacks.zenoss.ServiceNowIntegrator`_

#. *In Multiple Production Environments*

   Example: `ZenPacks.zenoss.ZenVMware`_

.. _zp_class_complexity:

Complexity
-------------------------------------------------------------------------------

1. *Meta-data Only*

   Built entirely in the web interface. No programming knowledge required.

   Example: `ZenPacks.zenoss.IISMonitor`_

2. *Event Class Transforms and Mappings*

   Built in the web interface. Basic Python knowledge required.

   Example: `ZenPacks.zenoss.OpenStack`_

3. *Command DataSource Plugins*

   Command datasource plugins can be written in any language and executed
   either on the Zenoss server, or remotely using SSH. Without writing a custom
   parser (see next item) they must write to STDOUT using either the Nagios or
   Cacti output formats and exit using the appropriate Nagios or cacti exit
   code.

   Example: `ZenPacks.zenoss.ApacheMonitor`_

4. *Command DataSource Parsers*

   Command datasource parsers must be written in Python and conform to the
   Zenoss `CommandParser` API. These parsers must be written to extract
   extended data from the output of command datasource plugins (see previous
   item), or to handle output that doesn't conform to the Nagios or Cacti
   output formats.

   Example: `ZenPacks.zenoss.SolarisMonitor`_

5. *Custom DataSource Types*

   Example: `ZenPacks.zenoss.ApacheMonitor`_

6. *Web Interface Customizations*

   Example: `ZenPacks.zenoss.ServiceNowIntegrator`_

7. *Impact Adapters*

   Example: `ZenPacks.zenoss.ZenVMware`_

8. *ETL Adapters*

   Example: `ZenPacks.zenoss.ZenVMware`_

9. *Modeler Plugins (SNMP, COMMAND or WMI)*

   Example: `ZenPacks.zenoss.SolarisMonitor`_

10. *Modeler Plugins (Python)*

   Example: `ZenPacks.zenoss.OpenStack`_

11. *Model Extensions*

   Example: `ZenPacks.zenoss.OpenStack`_

12. *Custom Daemons*

   Example: `ZenPacks.zenoss.ZenVMware`_

13. *Custom ZenHub Services*

   Example: `ZenPacks.zenoss.ZenVMware`_

Example ZenPack Classifications
===============================================================================

ZenPacks.zenoss.ApacheMonitor
-------------------------------------------------------------------------------

=============================== ===============================================
Classification                  Value
=============================== ===============================================
:ref:`zp_class_functionality`   :ref:`Monitoring <zp_class_functionality_monitoring>`
:ref:`zp_class_supportability`  Supported by Zenoss, Inc.
:ref:`zp_class_author`          Zenoss Engineering
:ref:`zp_class_availability`    Open Source
:ref:`zp_class_maturity`        In Multiple Production Environments
:ref:`zp_class_complexity`      6 (1 + 5)
=============================== ===============================================

ZenPacks.zenoss.IISMonitor
-------------------------------------------------------------------------------

=============================== ===============================================
Classification                  Value
=============================== ===============================================
:ref:`zp_class_functionality`   
:ref:`zp_class_supportability`  
:ref:`zp_class_author`          
:ref:`zp_class_availability`    
:ref:`zp_class_maturity`        
:ref:`zp_class_complexity`      
=============================== ===============================================

ZenPacks.zenoss.DistributedCollector
-------------------------------------------------------------------------------

=============================== ===============================================
Classification                  Value
=============================== ===============================================
:ref:`zp_class_functionality`   
:ref:`zp_class_supportability`  
:ref:`zp_class_author`          
:ref:`zp_class_availability`    
:ref:`zp_class_maturity`        
:ref:`zp_class_complexity`      
=============================== ===============================================

ZenPacks.zenoss.RANCIDIntegrator
-------------------------------------------------------------------------------

=============================== ===============================================
Classification                  Value
=============================== ===============================================
:ref:`zp_class_functionality`   
:ref:`zp_class_supportability`  
:ref:`zp_class_author`          
:ref:`zp_class_availability`    
:ref:`zp_class_maturity`        
:ref:`zp_class_complexity`      
=============================== ===============================================

ZenPacks.zenoss.DatabaseMonitor
-------------------------------------------------------------------------------

=============================== ===============================================
Classification                  Value
=============================== ===============================================
:ref:`zp_class_functionality`   
:ref:`zp_class_supportability`  
:ref:`zp_class_author`          
:ref:`zp_class_availability`    
:ref:`zp_class_maturity`        
:ref:`zp_class_complexity`      
=============================== ===============================================

ZenPacks.zenoss.ZenVMware
-------------------------------------------------------------------------------

=============================== ===============================================
Classification                  Value
=============================== ===============================================
:ref:`zp_class_functionality`   
:ref:`zp_class_supportability`  
:ref:`zp_class_author`          
:ref:`zp_class_availability`    
:ref:`zp_class_maturity`        
:ref:`zp_class_complexity`      
=============================== ===============================================

ZenPacks.zenoss.SolarisMonitor
-------------------------------------------------------------------------------

=============================== ===============================================
Classification                  Value
=============================== ===============================================
:ref:`zp_class_functionality`   
:ref:`zp_class_supportability`  
:ref:`zp_class_author`          
:ref:`zp_class_availability`    
:ref:`zp_class_maturity`        
:ref:`zp_class_complexity`      
=============================== ===============================================

ZenPacks.zenoss.Impact
-------------------------------------------------------------------------------

=============================== ===============================================
Classification                  Value
=============================== ===============================================
:ref:`zp_class_functionality`   
:ref:`zp_class_supportability`  
:ref:`zp_class_author`          
:ref:`zp_class_availability`    
:ref:`zp_class_maturity`        
:ref:`zp_class_complexity`      
=============================== ===============================================

ZenPacks.zenoss.OpenStack
-------------------------------------------------------------------------------

=============================== ===============================================
Classification                  Value
=============================== ===============================================
:ref:`zp_class_functionality`   
:ref:`zp_class_supportability`  
:ref:`zp_class_author`          
:ref:`zp_class_availability`    
:ref:`zp_class_maturity`        
:ref:`zp_class_complexity`      
=============================== ===============================================

ZenPacks.zenoss.ServiceNowIntegrator
-------------------------------------------------------------------------------

=============================== ===============================================
Classification                  Value
=============================== ===============================================
:ref:`zp_class_functionality`   
:ref:`zp_class_supportability`  
:ref:`zp_class_author`          
:ref:`zp_class_availability`    
:ref:`zp_class_maturity`        
:ref:`zp_class_complexity`      
=============================== ===============================================

ZenPacks.community.ZenODBC
-------------------------------------------------------------------------------

=============================== ===============================================
Classification                  Value
=============================== ===============================================
:ref:`zp_class_functionality`   
:ref:`zp_class_supportability`  
:ref:`zp_class_author`          
:ref:`zp_class_availability`    
:ref:`zp_class_maturity`        
:ref:`zp_class_complexity`      
=============================== ===============================================
