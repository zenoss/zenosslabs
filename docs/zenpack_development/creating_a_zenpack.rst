=============================================================================
Creating a ZenPack
=============================================================================

The actual creation of a new ZenPack is very simple, and done through the
Zenoss web interface. However, there some considerations related to the
ZenPack's name and version that should be considered at creation time. Once a
ZenPack is in use by you and potentially others renaming or changing the
version scheme can be more painful.

Follow these steps to create a new ZenPack:

#. Login to the Zenoss web interface as a user with the global *Manager* role.
#. Navigate to the *Advanced* section.
#. Choose *ZenPacks* from the left navigation.
#. Choose *Create a ZenPack* from the gear menu next to *Loaded ZenPacks*.
#. Name the ZenPack according to the `Naming a ZenPack`_ documentation.
#. Click *OK*.
#. Set *Version* according to the `ZenPack Versioning`_ documentation.
#. Set *Author* to *Your Name <your_email@example.com>*.
#. Set *Dependencies* according to the `ZenPack Dependencies`_ documentation.
#. Click *Save*.

After setting the version, author and dependencies for your ZenPack you should
export it so the changes get written to the ZenPack's source on the file
system.

#. Choose *Export ZenPack* from the gear menu in the bottom-left corner of the
   screen from the ZenPack's detail page.

#. Leave *Export to $ZENHOME/exports* selected then click *OK*.

Naming a ZenPack
=============================================================================

ZenPacks exist within the *ZenPacks* namespace. Zenoss requires at least one
additional level of namespace before the name of the ZenPack to guard against
different Zenoss developers creating ZenPacks by the same name. See the
following ZenPack name as an example:

*ZenPacks.zenoss.Memcached*

- *ZenPacks* is mandatory.

- *zenoss* is your definable namespace. *zenoss* is reserved for Zenoss, Inc.
  If you're creating a ZenPack that you aim to publish as open source into
  the Zenoss community as the standard ZenPack for performing some function,
  the *community* namespace is recommended. Otherwise your company name or
  username should be used.

- *Memcached* is the name of the ZenPack and should describe what the ZenPack
  is for in the shortest way possible. The most common functionality to
  provide with a ZenPack is to monitoring something. For this reason a name
  like Memcached is acceptable over MemcachedMonitor.


It's also possible to use additional namespaces. It will mainly just create
more typing for the developer, so it isn't often used. An example of why you
might want to do this is if you want to create many ZenPacks around the same
target system. A fictitious example of this would be AWS (Amazon Web Services)
monitoring.

- *ZenPacks.community.AWS.EC2*
- *ZenPacks.community.AWS.S3*
- *ZenPacks.community.AWS.RDS*


ZenPack Versioning
=============================================================================

ZenPacks should be thought of as standalone software packages and versioned as
such. A three part version number is recommended. For example, X.Y.Z
(*major*.*minor*.*patch*).

Follow these simple rules to maintain a proper version of your ZenPack:

- 0.7.0: First version you're playing with that others should still be very
  frightened of. (a.k.a alpha)

- 0.9.0: First version that you feel is consumable by others. (a.k.a. beta)

- 1.0.0: First stable version that has been thoroughly tested. Ideally by
  people other than the original developer, and in environments other than
  that of the original author.

For versions prior to 1.0.0, any bug fixes, enhancements or API breakages
should result in the *patch* number being incremented.

For versions subsequent to 1.0.0, the following rules should be followed:

- Bug fixes result in the *patch* number being incremented.

- New features that are backward-compatible result in the *minor* number
  being incremented and the *patch* number being reset to 0 even if bug fixes
  are also included.

- New features are *not* backward-compatible result in the *major* number
  being incremented and the *minor* and *patch* numbers being reset to 0 even
  if backwards-compatible features or bug fixes are also included.

I recommend `Semantic Versioning`_ for a reference on good software versioning
practices.


.. _Semantic Versioning: http://semver.org/


ZenPack Dependencies
=============================================================================

You can specify dependencies for your ZenPack. There are two major dependency
types. Dependency on the supported version of the Zenoss platform, and
dependencies on other ZenPacks.

For ZenPacks installed in developer mode, you can view and edit dependencies
by going to *Advanced* -> *ZenPacks* -> *Your ZenPack* in the web interface.
Under the *Dependencies* section you'll have a row for *Zenoss* and a row for
every other ZenPack that's installed in the system.

If you don't plan to test your ZenPack on prior versions of Zenoss, I
recommend always setting the *Versions(s)* field for the Zenoss row to be
``>=CURRENT_ZENOSS_MINOR_VERSION`` where *CURRENT_ZENOSS_MINOR_VERSION* would
be something like 3.2 or 4.2. This will prevent your ZenPack from being
installed on earlier versions of Zenoss.

If your ZenPack depends on functionality provided by other ZenPacks, you can
choose to simply put a check mark in the *Required* field for each of those
ZenPacks and not specify version. This only enforces that some version of that
ZenPack must be installed. To create a version-specific dependency, you would
enter a ``>=VERSION`` or ``==VERSION`` in the *Versions(s)* field for each
ZenPack dependency.

For more information on what comparisons can be used in the *Version(s)* field
you can reference the Python `Requirements Parsing`_
documentation.


.. _Requirements Parsing: http://pythonhosted.org/setuptools/pkg_resources.html#requirements-parsing
