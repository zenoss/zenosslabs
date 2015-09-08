===============================================================================
ZenPacks.zenoss.SolarisMonitor
===============================================================================

About
===============================================================================

The SolarisMonitor ZenPack enables Resource Manager to use Secure Shell (SSH)
to monitor Solaris hosts. Resource Manager models and monitors devices placed
in the /Server/SSH/Solaris device class by running commands and parsing the
output. Parsing of command output is performed on the Resource Manager server
(if using a local collector) or on a distributed collector. The account used to
monitor the device does not require root access or special privileges.

In addition to the previously described modeling and monitoring features this
ZenPack also enables Resource Manager to model and monitor Sun Solaris LDOM 
servers. Resource Manager will model devices utilizing the Simple Network
Management Protocol (SNMP) to collect LDOM information when a device resides 
in either the /Server/Solaris or /Server/SSH/Solaris device classes. The
discovered LDOM information will be displayed as components of the LDOM host
server. 

Features
-------------------------------------------------------------------------------

The SolarisMonitor ZenPack provides:

* File system and process monitoring
* Network interfaces and route modeling
* CPU utilization information
* Hardware information (memory, number of CPUs, and model numbers)
* OS information (OS-level, command-style information)
* Pkginfo information (such as installed software)
* LDOM monitoring

Prerequisites
-------------------------------------------------------------------------------

==================  ========================================================
Prerequisite        Restriction
==================  ========================================================
Zenoss Platform     3.1 or greater
Installed ZenPacks  ZenPacks.zenoss.SolarisMonitor
Firewall Acccess    Collector server to 22/tcp and 161/udp of Solaris server
Solaris Releases    OpenSolaris 5.11, Solaris 9 and 10
==================  ========================================================

Limitations
-------------------------------------------------------------------------------

The SolarisMonitor ZenPack does not support monitoring in Solaris Zones or
systems containing Solaris Zones. (Implemented with Solaris 10, Solaris Zones
act as isolated virtual servers within a single operating system instance.)


Usage
===============================================================================

Installation
-------------------------------------------------------------------------------

This ZenPack has no special installation considerations.  Depending on the
version of Zenoss you're installing the ZenPack into, you will need to verify
that you have the correct package (.egg) to install.

* Zenoss 4.1 and later: The ZenPack file must end with ``-py2.7.egg``.
* Zenoss 3.0 - 4.0: The ZenPack file must end with ``-py2.6.egg``.

To install the ZenPack you must copy the ``.egg`` file to your Zenoss master
server and run the following command as the ``zenoss`` user::

    zenpack --install <filename.egg>

After installing you must restart Zenoss by running the following command as
the ``zenoss`` user on your master Zenoss server::

    zenoss restart

If you have distributed collectors you must also update them after installing
the ZenPack.

Configuring
-------------------------------------------------------------------------------

Depending on the version of Solaris you may be able to monitor the server using
either SSH or SNMP. For OpenSolaris and Solaris 10, you can choose to use
either SSH or SNMP monitoring. For Solaris 9, only SSH monitoring is supported.

Configuring SSH Monitoring
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use the following steps to configure Zenoss to monitor your Solaris server(s)
using SSH.

1. Navigate to the ``/Server/SSH/Solaris`` device class' configuration
   properties.
2. Verify that the ``zCommandUsername`` and ``zCommandPassword`` are set to
   valid login credentials.
3. Add your Solaris server(s) to the ``/Server/SSH/Solaris`` device class.

Configuring SNMP Monitoring
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use the following steps to configure Zenoss to monitor your Solaris server(s)
using SNMP.

1. Verify that the snmpd process is running on your Solaris server(s).
2. Navigate to the ``/Server/Solaris`` device class' configuration properties.
3. Verify that your Solaris server(s) SNMP community strings are listed in the
   ``zSnmpCommunities`` property.
4. Add your Solaris server(s) to the ``/Server/Solaris`` device class.

Configuring LDOM Monitoring
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For OpenSolaris and Solaris 10 servers you will also get support for monitoring
LDOMs if they're used on the server. However, this monitoring is always
performed using SNMP. If you're already monitoring your Solaris server using
SNMP there is no additional configuration required to monitor its LDOMs. If you
configured Zenoss to monitor your Solaris server using SSH you should take the
following steps to monitor LDOMs.

1. Verify that the snmpd process is running on your Solaris server(s).
2. Navigate to the ``/Server/SSH/Solaris`` device class' configuration
   properties.
3. Verify that your Solaris server(s) SNMP community strings are listed in the
   ``zSnmpCommunities`` property.
4. Remodel your Solaris server(s) if they're already in the system. Otherwise
   add them to the ``/Server/SSH/Solaris`` device class.

Removal
-------------------------------------------------------------------------------

**Use caution when removing this ZenPack**

* Will **permanently** remove devices located in ``/Server/SSH/Solaris`` device
  class.
* Will **permanently** remove LDOM modeled components for devices located in 
  ``/Server/Solaris``.
* Will **permanently** remove associated monitored data for LDOM components.
* Will **permanently** remove the ``/Server/SSH/Solaris`` device class.

To remove this ZenPack you must run the following command as the ``zenoss``
user on your master Zenoss server::

    zenpack --remove ZenPacks.zenoss.SolarisMonitor

You must then restart the master Zenoss server by running the following command
as the ``zenoss`` user::

    zenoss restart

Troubleshooting
-------------------------------------------------------------------------------

Resolving CHANNEL_OPEN_FAILURE Issues
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The zencommand daemon's log file (``$ZENHOME/collector/zencommand.log``) may
show messages stating::

    ERROR zen.SshClient CHANNEL_OPEN_FAILURE: Authentication failure WARNING:zen.SshClient:Open of command failed (error code 1): open failed

If the sshd daemon's log file on the remote device is examined, it may report
that the MAX_SESSIONS number of connections has been exceeded and that it is
denying the connection request. In the OpenSSH daemons, this MAX_SESSIONS
number is a compile-time option and cannot be reset in a configuration file.

To work around this sshd daemon limitation, use the configuration property
zSshConcurrentSessions to control the number of connections created by
zencommand to the remote device:

1. Navigate to the device or device class in the Resource Manager interface.
    * If applying changes to a device class:
        a. Select the class in the devices hierarchy.
        b. Click Details.
        c. Select Configuration Properties.
    * If applying changes to a device:
        a. Click the device in the device list.
        b. Select Configuration Properties.
2. Set the ``zSshConcurrentSessions`` property. Try 10 first, and 2 if that
   doesn't resolve the problem.

Resolving Command Timeout Issues
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The zencommand daemon's log file ($ZENHOME/collector/zencommand.log) may show
messages stating::

    WARNING:zen.zencommand:Command timed out on device device_name: command

If this occurs, it usually indicates that the remote device has taken too long
to return results from the commands. To increase the amount of time to allow
devices to return results, change the configuration property
``zCommandCommandTimeout`` to a larger value.

1. Navigate to the device or device class in the Resource Manager interface.
    * If applying changes to a device class:
        a. Select the class in the devices hierarchy.
        b. Click Details.
        c. Select Configuration Properties.
    * If applying changes to a device:
        a. Click the device in the device list.
        b. Select Configuration Properties.
2. Increase the ``zCommandCommandTimeout`` property incrementally to a maximum
   of 240 until the timeout is resolved.


Appendixes
===============================================================================

Appendix A: Installed Items
-------------------------------------------------------------------------------

===================  ===================  ===================================
Type                 Name                 Location
===================  ===================  ===================================
Device Class         /SSH/Solaris         /Devices/Server
Modeler Plugin       df_ag                zenoss.cmd.solaris
Modeler Plugin       kstat                zenoss.cmd.solaris
Modeler Plugin       memory               zenoss.cmd.solaris
Modeler Plugin       netstat_an           zenoss.cmd.solaris
Modeler Plugin       netstat_r_vn         zenoss.cmd.solaris
Modeler Plugin       pkginfo              zenoss.cmd.solaris
Modeler Plugin       process              zenoss.cmd.solaris
Modeler Plugin       uname_a              zenoss.cmd.solaris
Modeler Plugin       hostid               zenoss.snmp.solaris
Modeler Plugin       ldommap              zenoss.snmp.solaris
Monitoring Template  Device               /Server/SSH/Solaris
Monitoring Template  FileSystem           /Server/SSH/Solaris
Monitoring Template  OSProcess            /Server/SSH/Solaris
Monitoring Template  ethernetCsmacd       /Server/SSH/Solaris
Monitoring Template  LDOM                 /Server
Monitoring Template  LDOMVcpu             /Server
Monitoring Template  LDOMVds              /Server
Event Class          /Status/LDOM         /
Event Class          /Status/LDOM/vCPU    /
Event Mapping        ldomStateChange      /Change
Event Mapping        ldomVCpuChange       /Change
Event Mapping        ldomVccChange        /Change
Event Mapping        ldomVconsChange      /Change
Event Mapping        ldomVdiskChange      /Change
Event Mapping        ldomVdsChange        /Change
Event Mapping        ldomVmemChange       /Change
Event Mapping        ldomVnetChange       /Change
Event Mapping        ldomVswChange        /Change
Event Mapping        ldomCreate           /Change/Add
Event Mapping        ldomDestroy          /Change/Remove
MIB                  SUN-LDOM-MIB         /
===================  ===================  ===================================

Monitoring Templates
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Device** *(/Server/SSH/Solaris)*

- *Data Points*

  - cpu_ssCpuIdle
  - cpu_ssCpuInterrupt
  - cpu_ssCpuSystem
  - cpu_ssCpuUser
  - io_read
  - io_written
  - percent_memory_percentMemUsed
  - percent_swap_percentSwapUsed
  - uptime_laLoadInt1
  - uptime_laLoadInt5
  - uptime_laLoadInt15
  - uptime_sysUpTime

- *Thresholds*

  - CPU Utilization
  - high load

- *Graphs*

  - Load Average
  - CPU Utilization
  - Memory Utilization
  - IO
  
**FileSystem** *(/Server/SSH/Solaris)*

- *Data Points*

  - disk_availBlocks
  - disk_availNodes
  - disk_percentInodesUsed
  - disk_totalBlocks
  - disk_totalInodes
  - disk_usedBlocks
  - disk_usedInodes

- *Thresholds*

  - high_disk_usage

- *Graphs*

  - Utilization
  - Inode Utilization

**OSProcess** *(/Server/SSH/Solaris)*
- *Data Points*

  - ps_count
  - ps_cpu
  - ps_mem

- *Graphs*

  - CPU Utilization
  - Memory
  - Process Count

**ethernetCsmacd** *(/Server/SSH/Solaris)*
- *Data Points*

  - intf_ifInErrors
  - intf_ifInPackets
  - intf_ifOutErrors
  - intf_ifOutPackets
  - intf_octets_ifInOctets
  - intf_octets_ifOutOctets

- *Thresholds*

  - Utilization 75 perc

- *Graphs*

  - Throughput
  - Packets

**LDOM** *(/Server)*

- *Data Sources*

  - ldomOperState
 
- *Thresholds*

  - operational state

**LDOMVcpu** *(/Server)*

- *Data Sources*

  - ldomVcpuOperationalStatus
  - ldomVcpuUtilPercent

- *Threshold*

  - operational status

- *Graph Definition*

  - CPU Utilization

**LDOMVds** *(/Server)*

- *Data Source*

  - ldomVdsNumofAvailVolume
  - ldomVdsNumofUsedVolume

- *Graph Definition*

  - Volumes

Appendix B: Required Daemons
-------------------------------------------------------------------------------

In addition to the core platform daemons the following optional daemons are
required for this ZenPack to fully function.

* zenperfsnmp
* zencommand
