==============================================================================
Exporting a ZenPack
==============================================================================

Now that we've created a ZenPack and added some configuration to it, we need to
export it. Exporting a ZenPack takes all of the object's you've added to your
ZenPack through the web interface and compiles them into an ``objects.xml``
file that gets saved into your ZenPack's source directory in the file system.

Follow these steps to export the NetBotz ZenPack.

#. Navigate to *Advanced* -> *ZenPacks* -> *NetBotz ZenPack* in the web
   interface.

#. Scroll to the bottom of the page to see what objects the ZenPack provides.

   All objects listed in the *ZenPack Provides* section and objects contained
   within them will be exported.

#. Choose *Export ZenPack* from the gear menu in the bottom-left of the screen.

#. Choose to only export and not download then click *OK*.

   You could also choose to download the ZenPack through your web browser.
   However, the downloaded file will be the built *egg* distribution format of
   the ZenPack. This means that it can be installed into other Zenoss systems,
   but is not suitable for further development.


This will export everything under *ZenPack Provides* to a file within your
ZenPack's source called *objects.xml*. No other files in your ZenPack's source
directory are created or modified. You can find this file in the following
path::

    $ZENHOME/ZenPacks/ZenPacks.yourname.NetBotz/ZenPacks/yourname/NetBotz/objects/objects.xml


Each time you add a new object to you ZenPack within the web interface, or
modify an object that's already contained within your ZenPack, you should
export the ZenPack again to update objects.xml. If you're using version control
on your ZenPack's source directory this would be a good time to commit the
resulting change to objects.xml.

.. warning::
   Exporting a ZenPack completely overwrites the *objects.xml* file that
   previously existed within the ZenPack's source directory. For this reason it is
   recommended that the objects.xml file never be modified by hand.
