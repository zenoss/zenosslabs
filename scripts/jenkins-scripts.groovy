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
