==============================================================================
Python Collector Plugin (Data Points)
==============================================================================

We've already created a data source plugin that creates Zenoss events for
weather alerts. Now we want to use the Weather Underground `Conditions` API to
monitor current weather conditions for each location. The purpose of this is to
illustrate that these Python data source plugins can also be used to collect
datapoints.


Create Conditions Data Source Plugin
==============================================================================

Follow these steps to create the `Conditions` data source plugin:

1. Add the following contents to the end of ``$ZP_DIR/dsplugins.py``.

   .. sourcecode: python

      class Conditions(PythonDataSourcePlugin):
      
          """Weather Underground conditions data source plugin."""
      
          @classmethod
          def config_key(cls, datasource, context):
              return (
                  context.device().id,
                  datasource.getCycleTime(context),
                  context.id,
                  'wunderground-conditions',
                  )
      
          @classmethod
          def params(cls, datasource, context):
              return {
                  'api_key': context.zWundergroundAPIKey,
                  'api_link': context.api_link,
                  'location_name': context.title,
                  }
      
          @inlineCallbacks
          def collect(self, config):
              data = self.new_data()
      
              for datasource in config.datasources:
                  try:
                      response = yield getPage(
                          'http://api.wunderground.com/api/{api_key}/conditions{api_link}.json'
                          .format(
                              api_key=datasource.params['api_key'],
                              api_link=datasource.params['api_link']))
      
                      response = json.loads(response)
                  except Exception:
                      LOG.exception(
                          "%s: failed to get conditions data for %s",
                          config.id,
                          datasource.location_name)
      
                      continue
      
                  current_observation = response['current_observation']
                  for datapoint_id in (x.id for x in datasource.points):
                      if datapoint_id not in current_observation:
                          continue
      
                      try:
                          value = current_observation[datapoint_id]
                          if isinstance(value, basestring):
                              value = value.strip(' %')
      
                          value = float(value)
                      except (TypeError, ValueError):
                          # Sometimes values are NA or not available.
                          continue
      
                      dpname = '_'.join((datasource.datasource, datapoint_id))
                      data['values'][datasource.component][dpname] = (value, 'N')
      
              returnValue(data)

   Most of the `Conditions` plugin is almost identical to the `Alerts` plugin
   so I won't repeat what can be read back in that section. The main difference
   starts at the ``current_observation = response['current_observation']`` line
   of the `collect` method.

   It grabs the `current_observation` data from the response then iterates over
   every datapoint configured on the datasource. This is a nice approach
   because it allows for some user-flexibility in what datapoints are captured
   from the `Conditions` API. If the API made `temp_c` and `temp_f` available,
   we could choose to collect `temp_c` just by adding a datapoint by that name.

   The following line is the most important in terms of explaining how to have
   your plugin return datapoint values.

   .. sourcecode: python

      data['values'][datasource.component][dpname] = (value, 'N')

   Basically we just stick ``(value, 'N')`` into the component's datapoint
   dictionary. The ``'N'`` is the timestamp at which the value occurred. If you
   know the time it should be specified as the integer UNIX timestamp. Use
   ``'N'`` if you don't know. This will use the current time.

2. Restart Zenoss.

   After adding a new datasource plugin you must restart Zenoss. If you're
   following the :ref:`running-a-minimal-zenoss` instructions you really only
   need to restart `zenhub`.

That's it. The datasource plugin has been created. Now we just need to do some
Zenoss configuration to allow us to use it.


Add Conditions to Monitoring Template
==============================================================================

To use this new plugin we'll add a new datasource and corresponding graphs to
the existing `Location` monitoring template defined in ``templates.yaml``.

Follow these steps to update the monitoring template:

1. Update ``$ZP_TOP_DIR/templates.yaml`` with the following content. This
   includes what should already be in the file.

   .. sourcecode:: yaml

      /WeatherUnderground/Location:
        description: Weather Underground location monitoring.
        targetPythonClass: ZenPacks.training.WeatherUnderground.WundergroundLocation
      
        datasources:
          alerts:
            type: Python
            plugin_classname: ZenPacks.training.WeatherUnderground.dsplugins.Alerts
            cycletime: "600"
      
          conditions:
            type: Python
            plugin_classname: ZenPacks.training.WeatherUnderground.dsplugins.Conditions
            cycletime: "600"
      
            datapoints:
              temp_c: GAUGE
              feelslike_c: GAUGE
              heat_index_c: GAUGE
              windchill_c: GAUGE
              dewpoint_c: GAUGE
              relative_humidity: GAUGE
              pressure_mb: GAUGE
              precip_1hr_metric: GAUGE
              UV: GAUGE
              wind_kph: GAUGE
              wind_gust_kph: GAUGE
              visibility_km: GAUGE
      
        graphs:
          Temperatures:
            units: degrees C.
      
            graphpoints:
              Temperature:
                dpName: conditions_temp_c
                format: "%7.2lf"
      
              Feels Like:
                dpName: conditions_feelslike_c
                format: "%7.2lf"
      
              Heat Index:
                dpName: conditions_heat_index_c
                format: "%7.2lf"
      
              Wind Chill:
                dpName: conditions_windchilltemp_c
                format: "%7.2lf"
      
              Dewpoint:
                dpName: conditions_dewpoint_c
                format: "%7.2lf"
      
          Relative Humidity:
            units: percent
            miny: 0
            maxy: 100
      
            graphpoints:
              Relative Humidity:
                dpName: conditions_relative_humidity
                format: "%7.2lf%%"
      
          Pressure:
            units: millibars
            miny: 0
      
            graphpoints:
              Pressure:
                dpName: conditions_pressure_mb
                format: "%7.0lf"
      
          Precipitation:
            units: centimeters
            miny: 0
      
            graphpoints:
              1 Hour:
                dpName: conditions_precip_1hr_metric
                format: "%7.2lf"
      
          UV Index:
            units: UV index
            miny: 0
            maxy: 12
      
            graphpoints:
              UV Index:
                dpName: conditions_UV
                format: "%7.0lf"
      
          Wind Speed:
            units: kph
            miny: 0
      
            graphpoints:
              Sustained:
                dpName: conditions_wind_kph
                format: "%7.2lf"
      
              Gust:
                dpName: conditions_wind_gust_kph
                format: "%7.2lf"
      
          Visibility:
            units: kilometers
            miny: 0
      
            graphpoints:
              Visibility:
                dpName: conditions_visibility_km
                format: "%7.2lf"

   Only the first 9 lines previously existed for the `alerts` support. Adding
   the `conditions` datasource with its 12 datapoints and corresponding 9
   graphs accounts for the remaining 104 lines.

2. Run the following commands to create the monitoring template defined in
   ``templates.yaml``.

   .. sourcecode:: bash

      cd $ZP_TOP_DIR
      ./load-templates templates.yaml

3. Navigate to `Advanced` -> `Monitoring Templates` in the web interface to
   verify that the `Location` monitoring template has been updated with the
   `conditions` datasource and corresponding graphs.

4. Export the ZenPack. (:ref:`exporting-a-zenpack`)

   The `/WeatherUnderground` device class is already part of our ZenPack, and
   we put the `Location` monitoring template into that device class. So
   exporting causes the template to be dumped into the ZenPack's
   ``objects.xml`` file.


Test Monitoring Weather Conditions
==============================================================================

Follow these steps to test weather condition monitoring:

1. Run the following command to collect from `wunderground.com`.

   .. sourcecode:: bash

      zenpython run -v10 --device=wunderground.com

   There will be a lot of output from this command, but we're mainly looking
   for at least one datapoint being written. If one works, it's likely that
   they all work. Look for a line similar to the following::

       DEBUG zen.RRDUtil: /opt/zenoss/perf/Devices/wunderground.com/80901.1.99999/conditions_temp_c.rrd: 29.8, @ N
