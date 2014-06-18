.. _using-yaml-templates:

==============================================================================
Using YAML Templates
==============================================================================

Ordinarily monitoring templates are built within the Zenoss web interface. If
you want one of these templates included with a ZenPack, you simply use the web
interface to add the template to any of the ZenPacks you have in development.

Sometimes you know that you have a lot of monitoring templates to create, or
the monitoring templates have a lot of datasource, datapoints, thresholds and
graphs. It can be tedious and error-prone to add all of these through the
web interface. In these cases it may be preferable to load monitoring templates
from files.

There's a script available called `load-templates` that makes it possible to
load monitoring templates from YAML_ source files.

.. _YAML: http://en.wikipedia.org/wiki/YAML


Download load-templates
==============================================================================

Run the following commands to download the `load-templates` script into your
ZenPack:

.. sourcecode:: bash

   cd $ZP_TOP_DIR
   wget https://raw.githubusercontent.com/zenoss/zenpacklib/master/load-templates
   chmod 755 load-templates

.. note::
   Note that we're putting this script into `$ZP_TOP_DIR`, not `$ZP_DIR`. This
   isn't required, but it's a good practice. Files located in `$ZP_TOP_DIR`
   won't by default be included in your ZenPack once it's built. Since `load-
   templates` is only used by the ZenPack developer, it doesn't need to be
   included in the built ZenPack.

This script requires that the `PyYAML` library be installed on your system. You
can run the following command as the `zenoss` user to install it:

.. sourcecode:: bash

   easy_install PyYAML


Create templates.yaml
==============================================================================

We now want to create the YAML file that can be used to create a monitoring
template that will be bound to our locations and execute our `Alerts` data
source plugin.

Follow these steps to create this monitoring template:

1. Create ``$ZP_TOP_DIR/templates.yaml`` with the following contents.

   .. sourcecode:: yaml

      /WeatherUnderground/Location:
        description: Weather Underground location monitoring.
        targetPythonClass: ZenPacks.training.WeatherUnderground.WundergroundLocation
   
        datasources:
          alerts:
            type: Python
            plugin_classname: ZenPacks.training.WeatherUnderground.dsplugins.Alerts
            cycletime: "600"

   At least some of this should be self-explanatory. The YAML vocabulary has
   been designed to be as intuitive and concise as possible. Let's walk through
   it.

   1. The highest-level element (based on indentation) is
      `/WeatherUnderground/Location`. This means to create a `Location`
      monitoring template in the `/WeatherUnderground` device class.

      .. note::
         Because we're using `zenpacklib` the monitoring template must be
         called ``Location`` because the is the `label` for the
         `WundergroundLocation` class to which we want the template bound.

   2. The `description` is for documentation purposes and should describe the
      purpose of the monitoring template.

   3. The `targetPythonClass` is a hint to what type of object the template is
      meant to be bound to. Currently this is only used to determine if users
      should be allowed to manually bind the template to device classes or
      devices. Providing a valid component type like we've done prevents users
      from making this mistake.

   4. Next we have `datasources` with a single `alerts` datasource defined.

      The `alerts` datasource only has three properties:

      * `type`: This is what makes `zenpython` collect the data.

      * `plugin_classname`: This is the fully-qualified class name for the
        `PythonDataSource` plugin we created that will be responsible for
        collecting the datasource.

      * `cycletime`: The interval in seconds at which this datasource should be
        collected.

2. Run the following commands to create the monitoring template defined in
   ``templates.yaml``.

   .. sourcecode:: bash

      cd $ZP_TOP_DIR
      ./load-templates templates.yaml

3. Navigate to `Advanced` -> `Monitoring Templates` in the web interface to
   verify that the `Location` monitoring template has been created as defined.

4. Export the ZenPack. (:ref:`exporting-a-zenpack`)

   The `/WeatherUnderground` device class is already part of our ZenPack, and
   we put the `Location` monitoring template into that device class. So
   exporting causes the template to be dumped into the ZenPack's
   ``objects.xml`` file.


Test Monitoring Weather Alerts
==============================================================================

Testing this is a bit tricky since we'll have to be monitoring a location that
currently has an active weather alert. Fortunately there's an easy way to find
one of these locations.

Follow these steps to test weather alert monitoring:

1. Go to the following URL for the current severe weather map of the United
   States.

   http://www.wunderground.com/severe.asp

2. Click on one of the colored areas. Orange and red are more exciting. This
   will take you to the text of the warning. It should reference city or county
   names.

3. Update `zWundergroundLocations` on the `wunderground.com` device to add one
   of the cities or counties that has an active weather alert. For example,
   "Buffalo, South Dakota".

4. Remodel the `wunderground.com` device then verify that the new location is
   modeled.

5. Run the following command to collect from `wunderground.com`.

   .. sourcecode:: bash

      zenpython run -v10 --device=wunderground.com

   There will be a lot of output from this command, but we're mainly looking
   for an event to be sent for the weather alert. It will look similar to the
   following output::

       DEBUG zen.zenpython: Queued event (total of 1) {'rcvtime': 1403112635.631883, 'wu-type': u'FIR', 'wu-significance': u'W', 'eventClassKey': 'wu-alert', 'wu-expires': u'8:00 PM MDT on June 18, 2014', 'component': '80901.1.99999', 'monitor': 'localhost', 'agent': 'zenpython', 'summary': u'Fire Weather Warning', 'wu-date': u'3:39 am MDT on June 18, 2014', 'manager': 'zendev.damsel.loc', 'eventKey': 'wu-alert-FIR', 'wu-phenomena': u'FW', 'wu-description': u'Fire Weather Warning', 'device': 'wunderground.com', 'message': u'\n...Red flag warning remains in effect from noon today to 8 PM MDT\nthis evening for gusty winds...low relative humidity and dry fuels for\nfire weather zones 222...226 and 227...\n\n* affected area...fire weather zones 222...226 and 227.\n\n* Winds...southwest 10 to 20 mph with gusts up to 35 mph.\n\n* Relative humidity...as low as 13 percent.\n\n* Impacts...extreme fire behavior will be possible if a fire \n starts. \n\nPrecautionary/preparedness actions...\n\nA red flag warning means that critical fire weather conditions\nare either occurring now...or will shortly. A combination of\nstrong winds...low relative humidity...and warm temperatures can\ncontribute to extreme fire behavior.\n\n\n\n\n', 'device_guid': 'f59e7e4d-be5d-4b86-b005-7357ce58f79c', 'severity': 3}
