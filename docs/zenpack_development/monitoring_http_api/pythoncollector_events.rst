==============================================================================
Python Collector Plugin (Events)
==============================================================================

Now that we have one or more locations modeled on our `wunderground.com`
device, we'll want to start monitoring each location. Using `PythonCollector`
we have the ability to create events, record datapoints and even update the
model. We'll start with an example that creates events from weather alert data.

The idea will be that we'll create events for locations that have outstanding
weather alerts such as tornado warnings. We'll try to capture severity data so
tornado warnings are higher severity events than something like a frost
advisory.


Create Alerts Data Source Plugin
==============================================================================

To make Zenoss able to run the data source plugin we're going to create, we
must first make sure the `PythonCollector` ZenPack is installed, and that our
ZenPack depends on it. See the :ref:`using-pythoncollector` section if you
haven't already done this.

Follow these steps to create the `Alerts` data source plugin:

1. Create ``$ZP_DIR/dsplugins.py`` with the following contents.

   .. sourcecode:: python

      """Monitors current conditions using the Weather Underground API."""
      
      # Logging
      import logging
      LOG = logging.getLogger('zen.WeatherUnderground')
      
      # stdlib Imports
      import json
      import time
      
      # Twisted Imports
      from twisted.internet.defer import inlineCallbacks, returnValue
      from twisted.web.client import getPage
      
      # PythonCollector Imports
      from ZenPacks.zenoss.PythonCollector.datasources.PythonDataSource import (
          PythonDataSourcePlugin,
          )
      
      
      class Alerts(PythonDataSourcePlugin):
      
          """Weather Underground alerts data source plugin."""
      
          @classmethod
          def config_key(cls, datasource, context):
              return (
                  context.device().id,
                  datasource.getCycleTime(context),
                  context.id,
                  'wunderground-alerts',
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
                          'http://api.wunderground.com/api/{api_key}/alerts{api_link}.json'
                          .format(
                              api_key=datasource.params['api_key'],
                              api_link=datasource.params['api_link']))
      
                      response = json.loads(response)
                  except Exception:
                      LOG.exception(
                          "%s: failed to get alerts data for %s",
                          config.id,
                          datasource.location_name)
      
                      continue
      
                  for alert in response['alerts']:
                      severity = None
      
                      if int(alert['expires_epoch']) <= time.time():
                          severity = 0
                      elif alert['significance'] in ('W', 'A'):
                          severity = 3
                      else:
                          severity = 2
      
                      data['events'].append({
                          'device': config.id,
                          'component': datasource.component,
                          'severity': severity,
                          'eventKey': 'wu-alert-{}'.format(alert['type']),
                          'eventClassKey': 'wu-alert',
      
                          'summary': alert['description'],
                          'message': alert['message'],
      
                          'wu-description': alert['description'],
                          'wu-date': alert['date'],
                          'wu-expires': alert['expires'],
                          'wu-phenomena': alert['phenomena'],
                          'wu-significance': alert['significance'],
                          'wu-type': alert['type'],
                          })
      
              returnValue(data)

   Let's walk through this code to explain what is being done.

   1. Logging

      The first thing we do is import `logging` and create `LOG` as our logger.
      It's important that the name of the logger in the ``logging.getLogger()``
      begins with ``zen.``. You will not see your logs otherwise.

      The stdlib and Twisted imports are almost identical to what we used in
      the modeler plugin, and they're used for the same purposes.

      Finally we import `PythonDataSourcePlugin` from the `PythonCollector`
      ZenPack. This is the class our data source plugin will extend, and
      basically allows us to write code that will be executed by the
      `zenpython` collector daemon.

   2. `Alerts` Class

      Unlike our modeler plugin, there's no need to make the plugin class' name
      the same as the filename. As we'll see later when we're setting up the
      monitoring template that will use this plugin, there's no specific
      name for the file or the class required because we configure where to
      find the plugin in the datasource configuration within the monitoring
      template.

   3. `config_key` Class Method

      The `config_key` method must have the ``@classmethod`` decorator. It is
      passed `datasource`, and `context`. The `datasource` argument will be
      the actual datasource that the user configures in the monitoring
      templates section of the web interface. It has properties such as
      `eventClass`, `severity`, and as you can see a `getCycleTime()` method
      that returns the interval at which it should be polled. The `context`
      argument will be the object to which the monitoring template and
      datasource is bound. In our case this will be a location object such as
      Austin, TX.

      The purpose of the `config_key` method is to split monitoring
      configuration into tasks that will be executed by the zenpython daemon.
      The zenpython daemon will create one task for each unique value returned
      from `config_key`. It should be used to optimize the way data is
      collected. In some cases it is possible to make a single query to an API
      to get back data for many components. In these cases it would be wise to
      remove ``context.id`` from the config_key so we get one task for all
      components.

      In our case, the Weather Underground API must be queried once per
      location so it makes more sense to put ``context.id`` in the config_key
      so we get one task per location.

      The value returned by `config_key` will be used when `zenpython` logs. So
      adding something like `wunderground-alerts` to the end makes it easy to
      see logs related to collecting alerts in the log file.

      The `config_key` method will only be executed by `zenhub`. So you must
      restart `zenhub` if you make changes to the `config_key` method. This
      also means that if there's an exception in the `config_key` method it
      will appear in the `zenhub` log, not `zenpython`.

   4. `params` Class Method

      The `params` method must have the ``@classmethod`` decorator. It is
      passed the same `datasource` and `context` arguments as `config_key`.

      The purpose of the `params` method is to copy information from the Zenoss
      database into the `config.datasources[*]` that will be passed as an
      argument to the `collect` method. Since the `collect` method is run by
      `zenpython` it won't have direct access to the database, so it relies
      on the `params` method to provide it with any information it will need
      to collect.

      In our case you can see that we're copying the context's
      `zWundergroundAPIKey`, `api_link` and `title` properties. All of these
      will be used in the `collect` method.

      Just like the `config_key` method, `params` will only be executed by
      `zenhub`. So be sure to restart `zenhub` if you make changes, and look
      in the `zenhub` log for errors.

   5. `collect` Method

      The `collect` method does all of the real work. It will be called once
      per cycletime. It gets passed a `config` argument which for the most part
      has two useful properties: `config.id` and `config.datasources`.
      `config.id` will be the device's id, and `config.datasources` is a list
      of the datasources that need to be collected.

      You'll see in the collect method that each datasource in
      `config.datasources` has some useful properties. `datasource.component`
      will be the id of the component against which the datasource is run, or
      blank in the case of a device-level monitoring template.
      `datasource.params` contains whatever the `params` method returned.

      Within the body of the collect method we see that we create a new `data`
      variable using ``data = self.new_data()``. `data` is a place where we
      stick all of the collected events, values and maps. `data` looks like the
      following:

      .. sourcecode:: python

         data = {
             'events': [],
             'values': defaultdict(<type 'dict'>, {}),
             'maps': [],
         }

      Next we iterate over every configured datasource. For each one we make
      a call to Weather Underground's `Alerts` API, then iterate over each
      alert in the response creating an event for each.

      The following standard fields are being set for every event. You should
      read Zenoss' event management documentation if the purpose of any of
      these fields is not clear. I highly recommend setting all of these fields
      to an appropriate value for any event you send into Zenoss to improve the
      ability of Zenoss and Zenoss' operators to manage the events.

      * `device`: Mandatory. The device id related to the event.
      * `component`: Optional. The component id related to the event.
      * `severity`: Mandatory. The severity for the event.
      * `eventKey`: Optional. A further uniqueness key for the event. Used for de-duplication and clearing.
      * `eventClassKey`: Optional. An identifier for the *type* of event. Used during event class mapping.
      * `summary`: Mandatory: A (hopefully) short summary of the event. Truncated to 128 characters.
      * `message`: Optional: A longer text description of the event. Not truncated.
      
      You will also see many `wu-*` fields being added to the event. Zenoss
      allows arbitrary fields on events so it can be a good practice to add any
      further information you get about the event in this way. It can make
      understanding and troubleshooting the resulting event easier.

      Finally we return data with all of events we appended to it. `zenpython`
      will take care of getting the events sent from this point.

2. Restart Zenoss.

   After adding a new datasource plugin you must restart Zenoss. If you're
   following the :ref:`running-a-minimal-zenoss` instructions you really only
   need to restart `zenhub`.

That's it. The datasource plugin has been created. Now we just need to do some
Zenoss configuration to allow us to use it.


Configure Monitoring Templates
==============================================================================

Rather than use the web interface to manually
:ref:`add-snmp-component-monitoring-template`, we'll jump to the next section
on :ref:`using-yaml-templates` to show how we can describe a monitoring
template using YAML_.

.. _YAML: http://en.wikipedia.org/wiki/YAML
