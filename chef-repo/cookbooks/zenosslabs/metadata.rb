maintainer       "Zenoss, Inc."
maintainer_email "labs@zenoss.com"
license          "All Rights Reserved"
description      "Installs/Configures ZenPack Build & Test Infrastructure"
long_description IO.read(File.join(File.dirname(__FILE__), 'README.rdoc')   )
version          "0.0.1"

depends "selinux"
depends "git"
depends "java"
depends "sudo"
