.. _using-pythoncollector:

==============================================================================
Using PythonCollector
==============================================================================

The `PythonCollector` ZenPack adds the capability to write high performance
datasources in Python. They will be collected by the `zenpython` daemon that
comes with the `PythonCollector` ZenPack.

I'd recommend reading the `PythonCollector Documentation`_ for more
information.

.. _PythonCollector Documentation: http://wiki.zenoss.org/ZenPack:PythonCollector


Installing PythonCollector
==============================================================================

The first thing we'll need to do is to make sure the `PythonCollector` ZenPack
is installed on our system. If it isn't, follow these instructions to install
it.

1. Download the latest release from the PythonCollector_ page.

2. Run the following command to install the ZenPack:

   .. sourcecode:: bash

      zenpack --install ZenPacks.zenoss.PythonCollector-<version>.egg

3. Restart Zenoss.

.. _PythonCollector: http://wiki.zenoss.org/ZenPack:PythonCollector


Add PythonCollector Dependency
------------------------------------------------------------------------------

Since we're going to be using `PythonCollector` capabilities in our ZenPack we
must now update our ZenPack to define the dependency.

Follow these instructions to define the dependency.

1. Navigate to `Advanced` -> `Settings` -> `ZenPacks`.

2. Click into the `ZenPacks.training.WeatherUnderground` ZenPack.

3. Check `ZenPacks.zenoss.PythonCollector` in the list of dependencies.

4. Click `Save`.

5. Export the ZenPack. (:ref:`exporting-a-zenpack`)
