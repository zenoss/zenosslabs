==============================================================================
Using ZenPackLib (zenpacklib)
==============================================================================

In the :ref:`snmp-device-modeling` and :ref:`snmp-component-modeling` sections
of the :ref:`snmp-index` documentation we covered what could be called the
"long way" to extend the Zenoss object model to add the new `NetBotzDevice`
device type, it's `TemperatureSensor` component type and the relationship
between them. A new library called `zenpacklib` is now available that we use
to make this process easier.

In this case we want to add a new `WundergroundDevice` device type, a
`WundergroundLocation` component type and a relationship between them so we can
add a Weather Underground device such as *wunderground.com* to Zenoss and add
one or more locations where we want to monitor weather conditions. This section
will describe how we do that using `zenpacklib`.


Create the Weather Underground ZenPack
==============================================================================

Since we don't yet have a Weather Underground ZenPack to work with, let's
create that first.

1. Go to the `Advanced` -> `Settings` -> `ZenPacks` in the Zenoss web
   interface.

2. Choose `Create a ZenPack...` from the gear menu above the list of ZenPacks.

3. Name the ZenPack `ZenPacks.training.WeatherUnderground` then click `OK`.


Download zenpacklib
==============================================================================

Creating the ZenPack will create the ZenPack's source directory under
`$ZENHOME/ZenPacks/ZenPacks.training.WeatherUnderground`. Run the following
commands as the zenoss user to make this directory, and it's important
subdirectory more easily accessible:

.. sourcecode:: bash

   export ZP_TOP_DIR=$ZENHOME/ZenPacks/ZenPacks.training.WeatherUnderground
   export ZP_DIR=$ZP_TOP_DIR/ZenPacks/training/WeatherUnderground

Then download the latest `zenpacklib` from GitHub into the ZenPack's main code
directory with the following commands.

.. sourcecode:: bash

   cd $ZP_DIR
   wget https://raw.githubusercontent.com/zenoss/zenpacklib/master/zenpacklib.py


Create the ZenPackSpec
==============================================================================

Once `zenpacklib.py` is in `$ZP_DIR` you can create what is called a
`ZenPackSpec` in the ZenPack's `__init__.py`. This `ZenPackSpec` will define
the specification for the ZenPack. Specifically its name, zProperties, classes
and class relationships.

Replace the contents of `$ZP_DIR/__init__.py` with the following:

.. sourcecode:: python

   # Import zenpacklib from the current directory (zenpacklib.py).
   from . import zenpacklib
   
   
   # Create a ZenPackSpec and name it CFG.
   CFG = zenpacklib.ZenPackSpec(
       name=__name__,
   
       zProperties={
           'DEFAULTS': {'category': 'Weather Underground'},
   
           'zWundergroundAPIKey': {},
   
           'zWundergroundLocations': {
               'type': 'lines',
               'default': ['Austin, TX', 'San Jose, CA', 'Annapolis, MD'],
           },
       },
   
       classes={
           'WundergroundDevice': {
               'base': zenpacklib.Device,
               'label': 'Weather Underground API',
           },
   
           'WundergroundLocation': {
               'base': zenpacklib.Component,
               'label': 'Location',
               'properties': {
                   'country_code': {
                       'label': 'Country Code',
                       'order': 4.0,
                   },
   
                   'timezone': {
                       'label': 'Time Zone',
                       'order': 4.1,
                   },
   
                   'api_link': {
                       'label': 'API Link',
                       'order': 4.9,
                       'grid_display': False,
                   },
               }
           },
       },
   
       class_relationships=zenpacklib.relationships_from_yuml(
           """[WundergroundDevice]++-[WundergroundLocation]"""
           )
   )
   
   # Create the specification.
   CFG.create()

You can see this `ZenPackSpec` defines the following important aspects of our
ZenPack.

1. The `name` is set to ``__name__`` which will evaluate to
   ZenPacks.training.WeatherUnderground. This should always be set in this way
   as it will helpfully figure out the name for you.

2. The `zProperties` contains configuration properties we want the ZenPack to
   add to the Zenoss system when it is installed.

   Note that `DEFAULTS` is not added as configuration property. It is a special
   value that will cause it's properties to be added as the default for all of
   the other listed zProperties. Specifically in this case it will cause the
   `category` of `zWundergroundAPIKey` and `zWundergroundLocations` to be set
   to ``Weather Underground``. This is a convenience to avoid having to
   repeatedly type the category for each added property.

   The `zWundergroundAPIKey` zProperty has an empty dictionary (``{}``). This
   is because we want it to be a `string` type with an empty default value.
   These happen to be the defaults so they don't need to be specified.

   The `zWundergroundLocations` property uses the `lines` type which allows
   the user to specify multiple lines of text. Each line will be turned into
   an element in a list which you can see is also how the default value is
   specified. The idea here is that unless the user configures otherwise, we
   will default to monitoring weather alerts and conditions for Austin, TX, San
   Jose, CA, and Annapolis, MD.

3. The `classes` contains each of the object classes we want the ZenPack to
   add.

   In this case we're adding `WundergroundDevice` which because `base` is set
   to `zenpacklib.Device` will be a subclass or specialization of the standard
   Zenoss device type. We're also adding `WundergroundLocation` which because
   `base` is set to `zenpacklib.Component` will be a subclass of the standard
   component type.

   The `label` for each is simply the human-friendly name that will be used to
   refer to the resulting objects when they're seen in the Zenoss web
   interface.

   The `properties` for `WundergroundLocation` are extra bits of data we want
   to model from the API and show to the user in the web interface. `order`
   will be used to show the properties in the defined order, and setting
   `grid_display` to false for `api_link` will allow it be shown in the details
   panel of the component, but not in the component grid.

4. `class_relationships` uses the `relationships_from_yuml` helper to
   succinctly define a relationship stating `WundergroundDevice` can contain
   many `WundergroundLocation` objects.

5. Finally ``CFG.create()`` create what has been defined in the `ZenPackSpec`.
   Without this call, nothing would happen.


Reinstall the ZenPack
==============================================================================

Because you added new zProperties you must now reinstall the ZenPack. This is
required because new zProperties only get installed into Zenoss when the
ZenPack is installed. Everything else in the `ZenPackSpec` is created each time
Zenoss starts.

Run the following command to reinstall the ZenPack and keep it in development
mode.

.. sourcecode:: bash

   zenpack --link --install $ZP_TOP_DIR
