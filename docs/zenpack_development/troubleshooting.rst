==============================================================================
Troubleshooting
==============================================================================


Using the Python Debugger
=============================================================================

One of the most powerful tools when debugging the Python portions of a ZenPack
is the Python debugger (*pdb*). With *pdb* you can set breakpoints in your
code. When the breakpoints are hit, you get a *(pdb)* prompt that has full
access to examine the stack and any local or global variables.

To set a breakpoint in your code you add the following line::

    import pdb; pdb.set_trace()


As with any code change, you must restart the Zenoss process that executes the
code in question.
