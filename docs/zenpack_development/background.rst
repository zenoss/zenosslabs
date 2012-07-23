==============================================================================
Background Information
==============================================================================

The section contains high-level background concepts and other information that
will make the subsequent sections easier to understand. I recommend that you
read and understand everything here.


Device vs. DeviceComponent
==============================================================================

Understanding the difference between a Zenoss *Device* and *DeviceComponent*
(often referred to as simply *component*) is useful for the Zenoss user, but
critical to the ZenPack developer. The Zenoss object model has these two
primary types of objects that can be modeled and monitored.

*Device*
  Devices are what you see on the Zenoss Infrastructure view in the web
  interface. If you see it in the Infrastructure view, it's a device. If you
  don't, it's not. A device has an *id* attribute that makes it unique in the
  system. It will have configuration properties associated with it either
  directly, or acquired from the device class within which it is contained. It
  will also have a *manageIp* attribute that Zenoss uses for modeling and
  monitoring.

  Devices are contained within a single device class such as */Server/Linux* or
  */Network/Ping*. Devices and device classes have a lot in common. They both
  have configuration properties (a.k.a zProperties) and can contain monitoring
  templates.

  Configuration properties and monitoring templates are defined in a
  hierarchical fashion with the most specific copy being used. Take the
  following example of the *zCommandUsername* configuration property.

  Where *zCommandUsername* is set:

  * / = ""
  * /Server = "root"
  * /Server/Linux/AWS = "ec2-user"
  * server1 in /Server/Linux/AWS device class = "joeuser"

  In this case, the zCommandUsername used for server1 would be "joeuser"
  because it is most specific to server1. If *zCommandUsername* has not been
  set directly on the device, "ec2-user" would be used instead.

  Monitoring templates work the same way. If a device has the *Device*
  monitoring template bound to it, it will first check to see if there's a
  local copy of that monitoring template contained within the device. If there
  isn't, the device class path will be walked back to / until a monitoring
  template named *Device* is found.

*DeviceComponent*
  Device components are what you see if you drill-down into a device in the web
  interface, then choose one of the component types from the left navigation
  pane. Each row in the grid in the top-right pane is a component. Examples
  include things like network interface, file systems, disks and processes.
  These are things that have many instances per device.

  Device components, commonly just called "components", don't have their own
  configuration properties. They only acquire configuration properties through
  the device that contains them. They do not have a *manageIp* because they're
  typically managed through the same IP address and protocol(s) as the device
  that contains them.


Template Binding
==============================================================================

How monitoring templates get bound is different for devices and device classes
than it is for components.

A device or device class can easily have many monitoring templates bound to
it. This is controlled by selecting *Bind Templates* from the gear menu of a
device or device class. You will be presented with an available list of
templates that could be bound on the left, and the list of templates that are
currently bound on the right. You will only see monitoring templates that are
appropriate to be bound directly to devices.

.. note::
   Using the *Bind Templates* dialog is really just setting the
   *zDeviceTemplates* configuration property in a more friendly way. You can
   directly modify *zDeviceTemplates* to achieve the same result.


.. _relationship-types:

Relationship Types
==============================================================================

The Zenoss model uses relationships between objects in the database in much the
same way that a relational database does. Here are examples of some of the
relationships working behind the scenes in a standard Zenoss installation.

- `DeviceClass` **has many** `Device`
- `Device` **has one** `OperatingSystem`
- `OperatingSystem` **has one** `ProductClass`
- `OperatingSystem` **has many** `FileSystem`
- `OperatingSystem` **has many** `IpInterface`
- `IpInterface` **has many** `IpAddress`
- `IpNetwork` **has many** `IpAddress`

ZenPacks can contribute new types of objects and new relationships to the
system. For example, `ZenPacks.zenoss.RabbitMQ` adds the following object
types and relationships.

- `Device` **has many** `RabbitMQNode`
- `RabbitMQNode` **has many** `RabitMQVHost`
- `RabbitMQVHost` **has many** `RabbitMQExchange`
- `RabbitMQVHost` **has many** `RabbitMQueue`

There are some important details you must understand to create new
relationships.

- There are *containing* and *non-containing* relationships.

  The idea of containment comes from Zenoss' database being a tree of objects.
  Every object in the database must be attached in some way to another
  persistent object, and only one other persistent object.

  In the case of a *containing* relationship you're saying that this is the
  relationship that attaches the member objects to the object model and
  therefore is how they get persisted. Removing an object from its *containing*
  relationship is the same thing as deleting the object from the database
  entirely. Any *non-containing* relationships it might have will be cleaned
  up.

  Of the above example standard relationships, the following are implemented as
  *containing* relationships.

  - `DeviceClass` **has many** `Device`
  - `Device` **has one** `OperatingSystem`
  - `OperatingSystem` **has many** `FileSystem`
  - `OperatingSystem` **has many** `IpInterface`
  - `IpNetwork` **has many** `IpAddress`

  On the other hand, a *non-containing* relationship has nothing to do with
  persistence. *Non-containing* relationships are used to create logical
  linkages from one object to another.

  Of the above example standard relationships, the following are implemented as
  *non-containing* relationships.

  - `OperatingSystem` **has one** `ProductClass`
  - `IpInterface` **has many** `IpAddress`

- All relationships must be bi-directional and explicitly defined on both sides
  of the relationship.

  In the `RabbitMQNode` **has many** `RabitMQVHost` example above this means
  that `RabbitMQNode` must declare that it has a `ToManyCont` relationship to
  `RabbitMQVHost`, and `RabbitMQVHost` must declare that it has a `ToOne`
  relationship to `RabbitMQNode`.


Relationship Classes
------------------------------------------------------------------------------

Relationships between object types (Python classes) are objects themselves. You
use the following classes from the `Products.ZenRelations.RelSchema` module to
define them.

- `ToMany`
- `ToManyCont`
- `ToOne`
- `ToOneCont`

Only the following pairs of relationships are valid because of the requirement
that relationships be defined bi-directionally.

- `ToMany` <-> `ToOne` (non-containing many-to-one)
- `ToMany` <-> `ToMany` (non-containing many-to-many)
- `ToManyCont` <-> `ToOne` (containing many-to-one)
- `ToOneCont` <-> `ToOne` (containing one-to-one)
