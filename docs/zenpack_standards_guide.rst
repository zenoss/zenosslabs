===============================================================================
ZenPack Standards Guide
===============================================================================

This document describes all requirements and recommendations for ZenPack
development. The intended audience is all Zenoss, Inc. employees who create or
modify ZenPacks including engineering, services and support. The intended
audience also includes any third-parties that create or modify ZenPacks that
are delivered to Zenoss customers by Zenoss, Inc.


Assumptions
===============================================================================

Some assumptions are made in this document regarding access to test facilities.

Product Inclusion
-------------------------------------------------------------------------------

ZenPacks must always be developed with the understanding that the potential
exists for them to become part of the product. Even in cases were ownership of
the ZenPack does not rest with Zenoss this must be observed because ownership
can change in the future. For this reason, special attention must be paid to
document the inclusion of any sensitive company data in ZenPacks.

Access to Test Environment
-------------------------------------------------------------------------------

In cases where the ZenPack developer(s) do not have access to endpoints
necessary for integration and testing work some standard operating procedures
must be suspended.


File Locations
===============================================================================

The location of specific files within a ZenPack's directory structure is
technically mandated in some circumstances, and open to the developer's desires
in others. To make it easier for other developers to more easily get up to
speed with the ZenPack in the future, the following recommendations for file
locations should be used.

* ``ZenPacks.<namespace.PackName>/``
* ``ZenPacks.<namespace.PackName>/ZenPacks/namespace/PackName/``

  * ``analytics/``

    The analytics bundle in .zip format: ``analytics-bundle.zip``

  * ``browser/`` (Note: Pre-ZPL only. See resources/ below)

    * ``configure.zcml``

      All ZCML definitions related to defining browser views or wiring
      browser-only concerns. This ``configure.zcml`` should be included by the
      default ``configure.zcml`` in its parent directory.

    * ``resources/``

      * ``css/`` - All stylesheets loaded by users' browsers.
      * ``img/`` - All images loaded by users' browsers.
      * ``js/`` - All javascript loaded by users' browser.
    |
  * ``resources/`` (Note: ZPL, See browser/ above)

    Any javascript code that modifies views go here.
    Especially note these JS file correlations:

    * ``device.js`` - Modifies the default device page.
    * ``ComponentClass.js`` - Modifies the component ComponentClass page.

    Folders inside ``resources`` have the following properties:

    * ``icon/`` (Note: ZPL)

      All images and icons loaded by the browser.
      Within this folder note the following name correspondence:

      * ``DeviceClass.png``` - Icon used in top left corner.
      * ``ComponentClass.png``` - Icon used in Impact diagrams for component.

  * ``datasources/``

    All datasources plugin files. Ensure your datasource has a descriptive name
    that closely correlates to the plugin name.

  * ``lib/``

    Any third-party modules included with the ZenPack should be located in this
    directory. In the case of pure-Python modules they can be located directly
    here. In the case of binary modules the build process must install them
    here. See the section of License Compliance below for more information on
    how to properly handle third-party content.

  * ``libexec/``

    Any scripts intended to be run by the zencommand daemon must be located in
    this directory.

  * ``migrate/``

    All migration code.

  * ``modeler/``

    All modeling plugins.

  * ``objects/``

    There should only ever be a single file called objects.xml in this
    directory. While the ZenPack installation code will load objects from any
    file in this directory with a ``.xml`` extension, the ZenPack export code
    will dump all objects back to ``objects.xml`` so creating other files only
    creates future confusion between installation and export.

  * ``parsers/``

    All custom parsers.

  * ``patches/``

    All monkeypatches. Note: your patches/__init__.py must specify patch
    loading.

  * ``protocols/``

    AMQP schema: Javascript code is read into the AMQP protocol to modify
    queues and exchanges.

  * ``services/``

    Custom collector services plugins.

  * ``service-definition/`` (Note: 5.X+)

    Service definitions for 5.X services containers.

  * ``skins/``

    All TAL template skins in .pt format. These change the UI look.

  * ``tests/``

    All unit tests.
 
  * ``facades.py``

    All facades (classes implementing ``Products.Zuul.interfaces.IFacade``)
    should be defined in this file. In ZenPacks where this single file becomes
    hard to maintain, a facades/ directory should be created containing
    individual files named for the group of facades they contain.

  * ``info.py``

    All info adapters (classes implementing ``Products.Zuul.interfaces.IInfo``)
    should be defined in this file. In ZenPacks where this single file becomes
    hard to maintain, an ``info/`` directory should be created containing
    individual files named for the group of info adapters they contain.

  * ``interfaces.py``

    All interfaces (classes extending ``zope.interface.Interface``) should be
    defined in this file. In ZenPacks where this single file becomes hard to
    maintain, an ``interfaces/`` directory should be created containing
    individual files named for the group of interfaces they contain.

  * ``routers.py``

    All routers (classes extending ``Products.ZenUtils.Ext.DirectRouter``)
    should be defined in this file. In ZenPacks where this single file becomes
    hard to maintain, a ``routers/`` directory should be created containing
    individual files named for the group of routers they contain.


License Compliance
===============================================================================

All ZenPack content must be compliant with the license of the ZenPack being
developed. If you intend to include a third-party module with a GPL license,
the ZenPack must also carry a GPL license and not include any other code that
would violate the GPL license. Always run third-party module inclusion through
legal to make sure there is no conflict.


Coding Standards
===============================================================================

All code and configuration in ZenPacks should be developed according to the
following public style guides.

* Python

  * PEP 8 -- Style Guide or Python Code
  * PEP 257 -- Docstring Conventions

* ZCML

  * Zope's ZCML Style Guide


Monitoring Template Standards
===============================================================================

Performance templates are one of the easiest places to make a real user
experience difference when new features are added to Zenoss. Spending a very
small amount of time to get the templates right goes a long way towards
improving the overall user experience. For this reason, the following checklist
should be used to determine if your monitoring template is acceptable.

Templates
-------------------------------------------------------------------------------

1. Is the template worthwhile? Should it be removed?
2. Is the template at the correct point in the model?
3. Does the template have a description? Is the description a good one?

Data Sources
-------------------------------------------------------------------------------

1. Can your datasource be named better?

  a. Is it a common metric that is being collected from other devices in
     another way? If so, name yours the same. This makes global reporting much
     easier.
  b. camelCaseNames seem to be the standard. Use them.

2. Never use absolute paths for COMMAND datasource command templates. This will
   end up causing problems on one of the three platforms we deal with. Link
   your plugin into zenPath('libexec') instead.

Data Points
-------------------------------------------------------------------------------

1. Using a COUNTER? You might want to think otherwise.

  a. Unnoticed counter rollovers can result in extremely skewed data.
  b. Using a DERIVE with a minimum of 0 will record unknown instead of wrong
     data.

2. Enter the minimum and/or maximum possible values for the data point if you
   know them.

  a. This again will allow unknown to be recorded instead of bad data.

Data Point Aliases
-------------------------------------------------------------------------------

1. Include the unit in the alias name if it is in any way not obvious. For
   example, use ``cpu_percent`` instead of ``cpu_usage``.

2. Use an RPN to calculate the base unit if the data point isn't already
   collected that way. For example, use ``1024,*`` to convert a data point
   collected in KBytes to bytes.

Thresholds
-------------------------------------------------------------------------------

1. Don't include a number in your threshold's name.

  a. This makes people have to recreate the threshold if they want to change
     it.

Graph Definitions
-------------------------------------------------------------------------------

1. Have you entered the units? Do it!

  a. This will become the y-axis label and should be all lowercase.
  b. Always use the base units. Never kbps or MBs. bps or bytes are better.

2. Do you know the minimum/maximum allowable values? Enter them!

  a. Common scenarios include percentage graphing with minimum 0 and maximum
     100.

3. Think about the order of your graph points. Does it make sense?

4. Are there other templates that show similar data to yours?

  a. If so, you should try hard to mimic their appearance to create a
     consistent experience.

Graph Points
-------------------------------------------------------------------------------

1. Have you changed the legend? Do it!

2. Adjust the format so that it makes sense.

  a. %5.2lf%s is good for values you want RRDTool to auto-scale.
  b. %6.2lf%% is good for percentages.
  c. %4.0lf is good for four digit numbers with no decimal precision or
     scaling.

3. Should you be using areas or lines?

  a. Lines are good for most values.
  b. Areas are good for things that can be thought of as a volume or quantity.

4. Does stacking the values to present a visual aggregate makes sense?


ETL Standards
===============================================================================

ETL is an acronym for `Extract, Transform, Load`. When writing ETL adapters
you're defining how Zenoss model data is extracted and transformed into the
`Zenoss Analytics` schema. The following guidelines should be used to keep
reporting consistent.

1. The ``reportProperties`` implementation in ``IReportable`` adapters must
   include the units in the name if not immediately obvious. For example, use
   ``cpu_used_percent`` instead of ``cpu_used``.


Documentation
===============================================================================

ZenPacks must be documented according to the
:doc:`zenpack_documentation_template` template. The
:doc:`zenpack_documentation_example` documentation can be used as an example
of a ZenPack that has been documented using this template.

Code Documentation
-------------------------------------------------------------------------------

Python code must be documented in docstrings in the locations specified in
PEP-8 and according to the style of PEP-257. Links to these standards can be
found in the `Coding Standards`_ section. Inline code comments should also be
used when the code isn't obvious.

Testing
===============================================================================

The following types of testing must be performed. All test results should be
recorded in the ZenPack's test result matrix. The matrix will have the ZenPack
version on one axis and the Zenoss version on the other axis. At the
intersection will be the result of unit testing, internal integration testing
and live integration testing.

Unit Tests
-------------------------------------------------------------------------------

Unit tests must be written for all public interfaces of ZenPack-specific code.
Unit tests will be the only mechanism for automated regression testing in some
cases, and the primary source in all others.

Internal Integration Testing
-------------------------------------------------------------------------------

ZenPacks must be tested internally using the packaged .egg that is will be
delivered to the customer. The test server must be the exact same version of
Zenoss being used by the customer. The test environment must match the
customer's environment as closely as possible. The only exception to internal
integration testing is cases where it is not possible to replicate the test
environment internally.

Live Integration Testing
-------------------------------------------------------------------------------

ZenPacks must be tested in their live deployment environment. A development or
staging instance of Zenoss that matches the production environment as closely
as possible should be used.


Versioning
===============================================================================

The first feature-complete ZenPack delivered to a customer should be version
1.0.0. Subsequent versions must increment the micro version if they contain
only bugfixes or tweaks (i.e. 1.0.1.) Subsequent versions must increment the
minor version if the contain new features (i.e. 1.1.0.)

A ZenPack's version must be incremented each time it is delivered to a customer
if there has been any change to it whatsoever.


Reviews
===============================================================================

Peer review is a strong mechanism to catch potential issues before integration
testing is performed. To that end the following reviews must be performed.

Design Review
-------------------------------------------------------------------------------

The initial design of a ZenPack must be peer reviewed before coding begins.

Code Review
-------------------------------------------------------------------------------

All code, including updates, must be peer reviewed before being committed to
the mainline development branch or any stable release branch.


Packaging & Delivery
===============================================================================

All ZenPacks must be delivered in their packaged .egg format. If arrangements
have been made for the customer to also get the source for the ZenPack it
should be provided in addition to the packaged egg as a tarball of the
development directory.

ZenPacks must be built using the same environment that the customer will be
installing them into. If the customer is installing into multiple environments
a separate egg should be built and delivered for each environment. In this
context the same environment is defined as the following.

* Exact same version of Zenoss
* Same major version of operating system
* Same architecture (i.e. i386 or x86_64)

All files including documentation must be delivered to customers in a ZenDesk
ticket.
