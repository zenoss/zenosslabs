==============================================================================
Wunderground API
==============================================================================

The Weather Underground provides an API that can be used to get all sorts of
data related to the weather. Before you can use most endpoints on the API you
must first create an account. Fortunately you can get a `Developer` account
with all of the bells and whistles for free by signing up at
http://www.wunderground.com/weather/api. So go sign up and get your API key.
You'll need it for the rest of this exercise.

We'll be using the following APIs for this exercise.

1. AutoComplete_
2. Alerts_
3. Conditions_

.. _AutoComplete: http://www.wunderground.com/weather/api/d/docs?d=autocomplete-api
.. _Alerts: http://www.wunderground.com/weather/api/d/docs?d=data/alerts
.. _Conditions: http://www.wunderground.com/weather/api/d/docs?d=data/conditions


AutoComplete API
==============================================================================

Both the `Alerts` and `Conditions` APIs require that you query for a specific
location. It can be hard to know what the name or code for a location is
without doing some manual research. That's where the `AutoComplete` API comes
in. You can provide a reasonable name for a location and it will return a list
of possible matches along with a unique link for that location.

We'll use the AutoComplete API during modeling so that the Zenoss user can
enter nearly any city or county name then let Zenoss do the work of converting
that into the link that we'll subsequently use to query for weather alerts and
conditions.

Here's an example query for Austin, TX:

	http://autocomplete.wunderground.com/aq?query=Austin%2C%20TX

.. note::
   "Austin%2C%20TX" is the URL encoded version of "Austin, TX". We won't have
   to worry about that when we work with it because our HTTP library
   automatically encodes URLs.

Here's the response to that example query for Austin, TX:

.. sourcecode:: javascript

   {
       "RESULTS": [
           {
               "c": "US",
               "l": "/q/zmw:78701.1.99999",
               "lat": "30.271158",
               "ll": "30.271158 -97.741699",
               "lon": "-97.741699",
               "name": "Austin, Texas",
               "type": "city",
               "tz": "America/Chicago",
               "tzs": "CDT",
               "zmw": "78701.1.99999"
           }
       ]
   }

There are a few things to note about this request and response. The first is
that we didn't need to use our API key. This is because the `AutoComplete` API
doesn't require an API key. The second is that there's only a single result for
Austin, TX. The third is the `l` value which is the unique link to Austin, TX
that we can use when accessing the other API endpoints such as `Alerts` and
`Conditions`.


Alerts API
==============================================================================

The `Alerts` API provides information about severe weather alerts such as
tornado warnings, flood warnings and other special weather statements. We'll be
collecting these alerts to create corresponding Zenoss events. This way
operators can know when severe weather may be impacting areas of concern.

Here's an example query for alerts in Austin, TX:

	http://api.wunderground.com/api/<api_key>/alerts/q/zmw:78701.1.99999.json

.. note::
   Note how the URL ends with /alerts/<link>.json using the `l` link value from
   the `AutoComplete` query for Austin, TX above.

Here's the relevant portion of the response to an alerts query. Of course
Austin doesn't have severe weather so we'll be looking at Des Moines alerts
instead:

.. sourcecode:: javascript

   {
       "alerts": [
           {
               "date": "1:07 PM CDT on June 16, 2014",
               "date_epoch": "1402942020",
               "description": "Severe Thunderstorm Warning",
               "expires": "2:15 PM CDT on June 16, 2014",
               "expires_epoch": "1402946100",
               "message": "\nThe National Weather Service in Des Moines has issued a\n\n* Severe Thunderstorm Warning for...\n southern Crawford County in west central Iowa...\n western Carroll County in west central Iowa...\n northwestern Audubon County in west central Iowa...\n\n* until 215 PM CDT\n\n* at 107 PM CDT...a severe thunderstorm was located 6 miles southwest\n of Earling...or 22 miles southwest of Denison...moving northeast at\n 25 mph.\n\n Hazard...half dollar size hail. \n\n Source...radar indicated. \n\n Impact...damage to vehicles is expected. \n\n* Locations impacted include...\n Denison...Manning...Dunlap...Manilla...Dow City...Arcadia...Vail...\n Templeton...Westside...Halbur...Arion...gray...Buck Grove...\n Aspinwall...Denison Municipal Airport and Manning Municipal\n Airport.\n\nPrecautionary/preparedness actions...\n\nA Tornado Watch remains in effect for the warned area. Tornadoes can\ndevelop quickly from severe thunderstorms. Although a tornado is not\nimmediately likely...if one is spotted...act quickly and move to a\nplace of safety inside a sturdy structure...such as a basement or\nsmall interior room.\n\nFor your protection move to an interior room on the lowest floor of a\nbuilding.\n\nTo report severe weather contact your nearest law enforcement agency.\nThey will send your report to the National Weather Service office in\nDes Moines .\n\n\nA Tornado Watch remains in effect until 800 PM CDT Monday evening for\nnorthwest Iowa.\n\nLat...Lon 4219 9506 4176 9481 4173 9509 4186 9510\n 4186 9564 4192 9567 4195 9568\ntime...Mot...loc 1807z 236deg 24kt 4172 9552 \n\nHail...1.25in\nwind...<50mph\n\n\nRev\n\n\n",
               "phenomena": "SV",
               "significance": "W",
               "type": "WRN",
               "tz_long": "America/Chicago",
               "tz_short": "CDT"
           }
       ]
   }

It's easy to imagine turning this alert into a Zenoss event. We'll see how to
do this a bit later. The `Alerts` API documentation has a link to a document
that describes what the `phenomena`, `significance`, and `type` values
represent.


Conditions API
==============================================================================

The `Conditions` API provides information about current weather conditions for
a given location. The `Conditions` API is used in exactly the same way as the
`Alerts` API, and accepts the same *link* to specify the location. There's a
lot of numeric data that would be useful to graph and threshold as Zenoss
datapoints.

Here's an example query for conditions in Austin, TX:

	http://api.wunderground.com/api/<api_key>/conditions/q/zmw:78701.1.99999.json

Here's the relevant portion of the response to a conditions query:

.. sourcecode:: javascript

   {
       "current_observation": {
           "UV": "1",
           "dewpoint_c": 11,
           "dewpoint_f": 51,
           "dewpoint_string": "51 F (11 C)",
           "display_location": {
               "city": "San Francisco",
               "country": "US",
               "country_iso3166": "US",
               "elevation": "47.00000000",
               "full": "San Francisco, CA",
               "latitude": "37.77500916",
               "longitude": "-122.41825867",
               "magic": "1",
               "state": "CA",
               "state_name": "California",
               "wmo": "99999",
               "zip": "94101"
           },
           "estimated": {},
           "feelslike_c": "13.9",
           "feelslike_f": "57.0",
           "feelslike_string": "57.0 F (13.9 C)",
           "forecast_url": "http://www.wunderground.com/US/CA/San_Francisco.html",
           "heat_index_c": "NA",
           "heat_index_f": "NA",
           "heat_index_string": "NA",
           "history_url": "http://www.wunderground.com/weatherstation/WXDailyHistory.asp?ID=KCASANFR58",
           "icon": "partlycloudy",
           "icon_url": "http://icons.wxug.com/i/c/k/partlycloudy.gif",
           "image": {
               "link": "http://www.wunderground.com",
               "title": "Weather Underground",
               "url": "http://icons.wxug.com/graphics/wu2/logo_130x80.png"
           },
           "local_epoch": "1402931138",
           "local_time_rfc822": "Mon, 16 Jun 2014 08:05:38 -0700",
           "local_tz_long": "America/Los_Angeles",
           "local_tz_offset": "-0700",
           "local_tz_short": "PDT",
           "nowcast": "",
           "ob_url": "http://www.wunderground.com/cgi-bin/findweather/getForecast?query=37.773285,-122.417725",
           "observation_epoch": "1402931132",
           "observation_location": {
               "city": "SOMA - Near Van Ness, San Francisco",
               "country": "US",
               "country_iso3166": "US",
               "elevation": "49 ft",
               "full": "SOMA - Near Van Ness, San Francisco, California",
               "latitude": "37.773285",
               "longitude": "-122.417725",
               "state": "California"
           },
           "observation_time": "Last Updated on June 16, 8:05 AM PDT",
           "observation_time_rfc822": "Mon, 16 Jun 2014 08:05:32 -0700",
           "precip_1hr_in": "0.00",
           "precip_1hr_metric": " 0",
           "precip_1hr_string": "0.00 in ( 0 mm)",
           "precip_today_in": "0.00",
           "precip_today_metric": "0",
           "precip_today_string": "0.00 in (0 mm)",
           "pressure_in": "29.89",
           "pressure_mb": "1012",
           "pressure_trend": "+",
           "relative_humidity": "81%",
           "solarradiation": "--",
           "station_id": "KCASANFR58",
           "temp_c": 13.9,
           "temp_f": 57.0,
           "temperature_string": "57.0 F (13.9 C)",
           "visibility_km": "16.1",
           "visibility_mi": "10.0",
           "weather": "Scattered Clouds",
           "wind_degrees": 238,
           "wind_dir": "WSW",
           "wind_gust_kph": 0,
           "wind_gust_mph": 0,
           "wind_kph": 4.8,
           "wind_mph": 3.0,
           "wind_string": "From the WSW at 3.0 MPH",
           "windchill_c": "NA",
           "windchill_f": "NA",
           "windchill_string": "NA"
       }
   }
