name "BuildMaster"
description "What we're currently deploying to our build master."

run_list(
    "recipe[zenosslabs::jenkins-master]",
    "recipe[zenosslabs::zenpacks-www-server]"
)
