==============================================================================
Python Collector Plugin (Modeling)
==============================================================================

The final capability of Python data source plugins is to make changes to the
Zenoss model. This allows a data source to make changes to the model in the
same way that `zenmodeler` does. Having this capability in a data source allows
modeling more frequently than the normal 12 hour `zenmodeler` interval.

To demonstrate this through an exercise, we'll extend the existing `Conditions`
plugin to capture the what the `Conditions` API calls *weather* which is some
text that looks like "Scattered Clouds" or "Sunny". We'll then show this value
for each location in the web interface.


Add


Add Modeling to Conditions Data Source Plugin
==============================================================================

Follow these steps to add modeling to the `Conditions` data source plugin:

1. Edit ``$ZP_DIR/__init__.py``.

   Add the following `weather` property to the `WundergroundLocation` class
   between the existing `timezone` and `api_link` properties.

   .. sourcecode:: python

      'weather': {
          'label': 'Weather',
          'order': 4.2,
      },


2. Edit ``$ZP_DIR/dsplugins.py``.

   Add the following needed import to the top of ``dsplugins.py``.

   .. sourcecode:: python

      from Products.DataCollector.plugins.DataMaps import ObjectMap

   Add the following code to the `Conditions` class' `collect` method right
   above the ``returnValue(data)`` line indented one level further. The
   ``returnValue(data)`` line is included in the following update to show
   where the new code should be placed.

   .. sourcecode:: python

             data['maps'].append(
                 ObjectMap({
                     'relname': 'wundergroundLocations',
                     'modname': 'ZenPacks.training.WeatherUnderground.WundergroundLocation',
                     'id': datasource.component,
                     'weather': current_observation['weather'],
                     }))

         returnValue(data)  # existing line

   The `maps` concept here is exactly the same as it is in modeler plugins.
   ``data['maps']`` can contain anything that a modeler plugin's `process`
   method can return.

2. Don't update the `Location` monitoring template.

   We're adding capability to a datasource that's already configured. No
   updates are required to the monitoring template.

3. Restart Zenoss.

   If we had only updated the `collect` method of the `Conditions` plugin we
   would only need to restart `zenpython`. However, because we added the new
   `weather` property to the `WundergroundLocation` class, we must restart
   nearly everything, so it's simpler to restart everything.


Test Modeling Current Weather
==============================================================================

Follow these steps to test weather condition monitoring:

1. Run the following command to collect from `wunderground.com`.

   .. sourcecode:: bash

      zenpython run -v10 --device=wunderground.com

   There will be a lot of output from this command, but we're looking for the
   following line which indicates that our maps were applied::

       DEBUG zen.python: Applying 1 datamaps to wunderground.com

2. Navigate to the `Locations` on the `wunderground.com` device and verify that
   each location shows something in its `Weather` column.
