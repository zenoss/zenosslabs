=============================================================================
Prerequisites
=============================================================================

To follow the steps in this guide you will need to have access to the following:

* A Linux server with Zenoss installed on it. This should not be a Zenoss
  server you care about. We will break things. You can download Zenoss from
  the `Zenoss download site`_.

* An SSH client to connect to your Zenoss server. `PuTTY`_ works well for
  Windows, ssh from the command line works well for Mac and Linux.

* This guide.

This guide will provide full examples to create a working ZenPack. However, the
examples and the explanations for them will be much easier to understand with at
least basic skills in the following areas:

* Linux: Ability to move around the file system, manage files and run commands.

* Programming or scripting with Python experience being a plus.

* XML syntax.

* SNMP.

Finally, it is expected that you are familiar with Zenoss from a configuration
perspective.


.. _Zenoss download site: http://community.zenoss.org/community/download
.. _PuTTY: http://www.chiark.greenend.org.uk/~sgtatham/putty/download.html
