=============================================================================
Development Environment
=============================================================================

The process of developing a ZenPack can be made much faster and less
frustrating by starting with a good development environment. The following
development environment setup is only a set of recommendations. If you already
have tools or techniques that you're more comfortable with or you consider
superior, you should use them.


Installing Zenoss
=============================================================================

To best develop and deploy ZenPacks into a production environment, I recommend
having three Zenoss systems: development, staging and production.


Development Zenoss System
-----------------------------------------------------------------------------

Your development Zenoss system should not be shared with others, and should be
as minimal an installation as possible. This will allow for problems to be
diagnosed, fixed and tested as quickly as possible.

I recommend installing Zenoss from the single zenoss-x.y.z RPM on Red Hat
Enterprise Linux or CentOS. The Zenoss installation instructions will
ordinarily have you install a zenoss-core-zenpacks RPM, and a zenoss-
enterprise-zenpacks RPM for commercial Zenoss customers. To keep the system as
small as possible, these should not be installed into your ZenPack development
system.


Staging Zenoss System
-----------------------------------------------------------------------------

The staging Zenoss system should be shared by all ZenPack developers. After a
ZenPack has been successfully tested in the development system should it be
installed into the staging environment.

This system should mimic the production system as closely as possible. It
should be installed in the same way as the production system, and should have
the same base set of ZenPacks installed. The purpose of the staging system is
to do final integration testing before ZenPacks are installed into the
production system.


Production Zenoss System
-----------------------------------------------------------------------------

New ZenPacks and updates to existing ZenPacks should only be deployed into the
production system after they've been successfully tested in the development
and staging systems.


Running a Minimal Zenoss
=============================================================================

Often times ZenPack development is done within virtual machines, or spare
hardware that doesn't have the same resources as a production Zenoss system.
Additionally, during development you will need to restart Zenoss far more
frequently than in a production setup. For these reasons you will want to run
as little of Zenoss as necessary.

After installing your Zenoss development system, run the following commands to
reduce your Zenoss deployment to the minimum typical processes::

    su - zenoss
    zenoss stop

    cat > $ZENHOME/etc/daemons.txt << EOF
    zeneventserver
    zopectl
    zeneventd
    zenhub
    zenjobs
    EOF

    touch $ZENHOME/etc/DAEMONS_TXT_ONLY

    zenoss start


See the following notes for more information on what these commands are doing.

#. The ``su - zenoss`` command is an important one that you'll be using very
   frequently. This command switches from the *root* user to the *zenoss* user.
   The hyphen (-) creates what's called a login shell. This means that the
   *zenoss* user's full environment will be loaded. This full environment is
   necessary to run any Zenoss commands.

#. The ``zenoss stop`` command stops all Zenoss processes.

#. The ``cat > ...`` that ends with ``EOF`` on a blank line writes those
   specific daemon names into the ``$ZENHOME/etc/daemons.txt`` file. This
   file contains the names of any daemons *in addition to the default* that
   should be started, stopped and otherwise managed by the ``zenoss`` master
   control script.

#. The ``touch $ZENHOME/etc/DAEMONS_TXT_ONLY`` command will cause the
   ``zenoss`` master control script to only manage daemons listed in the
   aforementioned ``daemons.txt`` file.

#. The ``zenoss start`` command will only start daemons listed in
   ``daemons.txt``.


Running Zenoss in the Foreground
=============================================================================

To take your development and debugging environment to the next level, I
recommend running most Zenoss processes in the foreground with full debug
logging enabled. This allows you to easily see exactly what is happening, and
provides a very quick way, CTRL-C, to stop and start individual processes.
Perhaps the most useful benefit is that you can use the Python debugger to set
breakpoints without having them hang background daemons.

The ``zeneventserver`` process is the only process that I recommend running as
a daemon while developing ZenPacks. This is because there are no changes you
can make while developing a ZenPack that require restarting
``zeneventserver``. There's also no common reason you'd want to see its
debugging output.

You can open multiple SSH sessions to your Zenoss server, or use the GNU
screen or tmux terminal multiplexers to simultaneously run Zenoss processes in
the foreground.

Open five (5) sessions as the ``zenoss`` user on your zenoss server using any
of the aforementioned methods. The sessions should run the following commands
respectively:

#. ``zopectl fg``
#. ``zeneventd run -v10``
#. ``zenhub run -v10 --workers=0``
#. ``zenjobs run -v10 --cycle``
#. nothing: miscellaneous shell work is done here

The ``-v10`` option enables *DEBUG* level logging for the process. The
``--workers=0`` option to zenhub is important to prevent zenhub from spawning
other worker process to do work. If work was performed in a worker process you
may not have foreground visibility to it. The ``--cycle`` option to zenjobs is
necessary to prevent it from executing all current pending jobs then exiting.


Installing ZenPacks
=============================================================================

ZenPacks can be installed either from a packaged .egg file, or from a source
directory. The only situations in which I recommend installing from a packaged
egg is for the ZenPacks that ship with Zenoss and are automatically installed
from their .egg file, and when the source is not available.

There are some important reasons why installing in development mode from a
source directory is preferable. They include:

- The running ZenPack code can be a checkout from version control. This makes
  it easier to audit ZenPack code for changes.

- ZenPacks can be upgraded in-place. Depending on the changes, this can often
  allow for less Zenoss daemons needing to be restarted after upgrading a
  ZenPack.


When a new ZenPack is created in the user interface, it is created in
development mode with the source directory located in $ZENHOME/ZenPacks/. To
install or upgrade an existing ZenPack from it's source directory, the
``--link`` option is used as follows::

    zenpack --link --install $ZENHOME/ZenPacks/ZenPacks.namespace.ZenPackName
