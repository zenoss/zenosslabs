==============================================================================
SNMP Tools
==============================================================================

To configure Zenoss to monitor a device using SNMP, it is necessary to
understand a bit about SNMP and the specific capabilities of your device. This
section will walk you through using Net-SNMP tools to learn about SNMP and your
device.

The ``netsnmp-utils`` package is a prerequisite to installing Zenoss so you
already have the SNMP tools you need installed on your Zenoss server.


Using SNMPoster
=============================================================================

When developing a ZenPack to monitor an SNMP-enabled device it can often be
useful to simulate the device's SNMP agent. There are many tools out there that
can be used to do this. Some commercial and some free. Out of the free tools I
recommend SNMPoster_ mainly because it can easily be run on your Zenoss
development system, and uses `snmpwalk` output as its input format. This makes
it easy to grab and use data from real devices.

Use the following instructions to setup SNMPoster to simulate the NetBotz
device used throughout this guide. These steps should all be run as the root
user.

1. Install SNMPoster_ according to the instructions on its site.

2. Download and configure the NetBotz agent.

   .. sourcecode:: bash

      mkdir -p /etc/snmposter/agents
      cd /etc/snmposter/agents
      wget https://github.com/cluther/snmposter/raw/master/agents/NetBotz.snmpwalk
      cat > /etc/snmposter/agents.csv << EOF
      /etc/snmposter/agents/NetBotz.snmpwalk,127.0.1.113
      EOF

2. Configure `snmpd` to only listen on 127.0.0.1.

   1. Add the following line to the top of ``/etc/snmp/snmpd.conf``::

      agentaddress 127.0.0.1

   2. Restart `snmpd`:

      .. sourcecode:: bash

         service snmpd restart

3. Start SNMPoster.

   .. sourcecode:: bash

      source /snmposter/bin/activate
      snmposter -f /etc/snmposter/agents.csv

4. Test.

   .. sourcecode:: bash

      snmpwalk -v2c -c public 127.0.1.113 sysDescr

   You should see the following output::

       SNMPv2-MIB::sysDescr.0 = STRING: Linux Netbotz01 2.4.26 #1 Wed Oct 31 18:09:53 CDT 2007 ppc


.. _SNMPoster: https://github.com/cluther/snmposter#readme


Using snmpwalk
==============================================================================

The tool you'll be using most often is called ``snmpwalk``. All SNMP values are
arranged on a tree, and snmpwalk allows you to query for all data under a given
branch of that tree. See the following example that walks all values under the
``system`` branch::

    # snmpwalk -v2c -c public 127.0.1.113 system
    SNMPv2-MIB::sysDescr.0 = STRING: Linux Netbotz01 2.4.26 #1 Wed Oct 31 18:09:53 CDT 2007 ppc
    SNMPv2-MIB::sysObjectID.0 = OID: SNMPv2-SMI::enterprises.5528.100.20.10.2006
    DISMAN-EVENT-MIB::sysUpTimeInstance = Timeticks: (7275488) 20:12:34.88
    SNMPv2-MIB::sysContact.0 = STRING: unknown
    SNMPv2-MIB::sysName.0 = STRING: Netbotz01
    SNMPv2-MIB::sysLocation.0 = STRING: Z1 Rack02 NetBotz01


We can see that this NetBotz device seems to be based on Linux and that we have
some more-or-less useful information about the device's name, location and
administrative contact.

The second line with the ``sysObjectID`` has an unusual value. It's a partially
decoded OID. It isn't decoded enough for us to know what it means. SNMP tools
including Net-SNMP use MIB files to decode these OIDs into human readable
values. In fact, we're only able to read most of the output above because Net-
SNMP has a set of standard MIBs enabled by default.

Let's run that command again, but use the ``-On`` flag to tell snmpwalk not to
decode OIDs::

    # snmpwalk -v2c -c public -On 127.0.1.113 system
    .1.3.6.1.2.1.1.1.0 = STRING: Linux Netbotz01 2.4.26 #1 Wed Oct 31 18:09:53 CDT 2007 ppc
    .1.3.6.1.2.1.1.2.0 = OID: .1.3.6.1.4.1.5528.100.20.10.2006
    .1.3.6.1.2.1.1.3.0 = Timeticks: (7275488) 20:12:34.88
    .1.3.6.1.2.1.1.4.0 = STRING: unknown
    .1.3.6.1.2.1.1.5.0 = STRING: Netbotz01
    .1.3.6.1.2.1.1.6.0 = STRING: Z1 Rack02 NetBotz01


While this data is mostly less valuable than the decoded version above, it's
more useful for a single reason. We can take that
``.1.3.6.1.4.1.5528.100.20.10.2006`` value and search the Internet for it. It's
best to remove the leading ``.``. and search for
``1.3.6.1.4.1.5528.100.20.10.2006`` instead.

This should lead you to the ``NETBOTZV2-MIB`` which will contain the decoding
information we need to learn more about this device. Download
``NETBOTZV2-MIB.mib`` and copy it into the ``/usr/share/snmp/mibs/`` directory
of your Zenoss server.

Now we can run the original snmpwalk command again with the addition of the
``-m all`` option. This option tells Net-SNMP tools to use all MIBs::

    # snmpwalk -v2c -c public -m all 127.0.1.113 system
    SNMPv2-MIB::sysDescr.0 = STRING: Linux Netbotz01 2.4.26 #1 Wed Oct 31 18:09:53 CDT 2007 ppc
    SNMPv2-MIB::sysObjectID.0 = OID: NETBOTZV2-MIB::netBotz420ERack
    DISMAN-EVENT-MIB::sysUpTimeInstance = Timeticks: (7275488) 20:12:34.88
    SNMPv2-MIB::sysContact.0 = STRING: unknown
    SNMPv2-MIB::sysName.0 = STRING: Netbotz01
    SNMPv2-MIB::sysLocation.0 = STRING: Z1 Rack02 NetBotz01


Now we can see that the sysObjectID is NETBOTZV2-MIB::netBotz420ERack. This
gives us a better idea of exactly what kind of device it is. We'll see that as
we look deeper into this device that the NETBOTZV2-MIB will prove more useful.


Default Net-SNMP Options
==============================================================================

The snmpwalk usage showed three primary command line options that we tend to
use most of the time. Net-SNMP allows you to specify these in a configuration
file so you don't have to type them every time. I recommend doing this.

Create ``/etc/snmp/snmp.conf`` and add the following lines::

    defVersion v2c
    defCommunity public
    mibs ALL


These lines add the following equivalent command line options respectively:

- ``-v2c``
- ``-c public``
- ``-m all``

So now we can run this command::

    snmpwalk 127.0.1.113


And get the same results as if we ran::

    snmpwalk -v2c -c public -m all 127.0.1.113


Trust me that this will save you time while developing this ZenPack, and others
in the future.


Decoding and Encoding OIDs
==============================================================================

Often it can be useful to turn numeric OIDs into their human-readable
equivalent, or vice-versa. The ``snmptranslate`` command can be used for this.
See the following examples.

OID to name::

    # snmptranslate .1.3.6.1.4.1.5528.100.20.10.2006
    NETBOTZV2-MIB::netBotz420ERack

Name to OID::

    # snmptranslate -On NETBOTZV2-MIB::netBotz420ERack
    .1.3.6.1.4.1.5528.100.20.10.2006
