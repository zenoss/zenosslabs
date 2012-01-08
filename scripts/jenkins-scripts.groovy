/*
 * Schedule builds for up to 10 jobs that have never been built.
 */
import hudson.model.*

count = 0

println("Scheduling build for 10 unbuilt jobs:")

for (item in Hudson.instance.items) {
    if (item.getLastBuild() == null && item.isBuildable() && !item.isBuilding() && !item.isInQueue()) {
        println("  - " + item.name)

        cause = new Cause.RemoteCause("damsel", "initial build script")
        item.scheduleBuild(cause)

        count++
    }

    if (count >= 9) {
        break;
    }
}

/*
 * Schedule builds for all jobs that have never been built.
 */
import hudson.model.*

println("Scheduling build for all unbuilt jobs:")

for (item in Hudson.instance.items) {
    if (item.getLastBuild() == null && item.isBuildable() && !item.isBuilding() && !item.isInQueue()) {
        println("  - " + item.name)

        cause = new Cause.RemoteCause("damsel", "initial build script")
        item.scheduleBuild(cause)
    }
}

/*
 * Schedule builds for all discovery jobs.
 */
import hudson.model.*

println("Scheduling build for all discovery jobs:")

for (item in Hudson.instance.items) {
    if (item.name.startsWith('Discovery')) {
        println("  - " + item.name)

        cause = new Cause.RemoteCause("damsel", "batch discovery build")
        item.scheduleBuild(cause)
    }
}

/*
 * Schedule builds for all ZenPack jobs.
 */
import hudson.model.*

println("Scheduling build for all ZenPack jobs:")

for (item in Hudson.instance.items) {
    if (item.name.startsWith('ZenPacks.')) {
        println("  - " + item.name)

        cause = new Cause.RemoteCause("damsel", "batch ZenPack build")
        item.scheduleBuild(cause)
    }
}
