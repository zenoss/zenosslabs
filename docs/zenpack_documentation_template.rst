===============================================================================
ZenPack.example.Name
===============================================================================

About
===============================================================================

Introduction to the ZenPack and any potentially foreign concepts such as the
target that is being monitored or integrated with.

Features
-------------------------------------------------------------------------------

High-level overview of the ZenPack's features and functionality. Focus on the
value proposition. Target audience would be people trying to understand Zenoss'
capabilities, not Zenoss administrators.

Prerequisites
-------------------------------------------------------------------------------

Requirements and dependencies that must be satisfied. This section should cover
the following at a minimum and where applicable.

  * Minimum required Zenoss version
  * Maximum supported Zenoss version if known
  * ZenPack dependencies (with specific versions if known)
  * Other installation dependencies if known (e.g. operating system packages)
  * Supported versions of the monitoring or integration target

Limitations
-------------------------------------------------------------------------------

Note any shortcomings that the user might otherwise be left curious about. This
section is optional.

Usage
===============================================================================

The target audience for the entire Usage section is a Zenoss administrator.

Installing
-------------------------------------------------------------------------------

Standard installation steps plus any other installation steps or notes specific
to this ZenPack.

Using
-------------------------------------------------------------------------------

One or more ad-hoc usage related sections. This (or these) sections will likely
contain the bulk of the ZenPack's custom documentation. The section(s) will not
necessarily be called ``Using``.

Removing
-------------------------------------------------------------------------------

Standard ZenPack removal steps plus any removal steps or notes specific to this
ZenPack. Be especially careful to cover anything that will result in data loss
such as removal of device classes and their contained devices.

Troubleshooting
-------------------------------------------------------------------------------

Document common problems users of the ZenPack may run into such as what happens
in the result of authentication failures or other configuration mistakes.

Appendix
===============================================================================

The two examples appendixes below will very commonly be used. Additional
reference material can be made available in additional appendixes. The
``Appendixes`` section can only be omitted if the ZenPack installs no items as
described below, and requires no non-platform daemons as described below.

Appendex A: Installed Items
-------------------------------------------------------------------------------

Detail the items installed by the ZenPack. Items include the following.

  * Device Classes
  * Configuration Properties
  * Modeler Plugins
  * Command Parsers
  * Monitoring Templates
  * Process Classes
  * IP Service Classes
  * Windows Service Classes
  * Event Classes
  * Event Mappings
  * MIBs
  * Reports

Appendex B: Related Daemons
-------------------------------------------------------------------------------

Detail the daemons outside of the core platform required to take advantage of
all of the ZenPack's functionality. The core platform daemons listed below
*should not* be explicitly listed.

  * ``zeoctl``
  * ``zeneventserver``
  * ``zeneventd``
  * ``zenhub``
  * ``zenjobs``
  * ``zendisc``
  * ``zenmodeler``
  * ``zenimpactserver``
  * ``zenimpactgraph``
  * ``zenimpactstate``
  * ``zenjserver``

Daemons such as the following, plus any daemons delivered with the ZenPack
*should* be listed.

  * ``zencommand``
  * ``zenperfsnmp``
  * ``zenprocess``
