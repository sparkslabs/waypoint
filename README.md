BBC IOT
========

This is a package that is aimed at getting a codebase suitable for
running a basic IOT enhanced event.

It is derived from the sparkslabs/sketches package here:
    https://github.com/sparkslabs/sketches
    
And also derived from the 20 minute hack that works towards the same.

The aim of this package is as follows:
    * You should have installed a working Ubuntu 12.04 box
    * You should be able to install this package
    * You should be able to configure running profiles in /etc/bbciotservice
        * Dependent on these profiles, when this box starts up it should
          start up a process that configures the process as tag reader node
          or as an collation node, or both.
        * This should be able to happen without human interaction - except
          for initial configuration

This is not going to happen overnight, so the aim will be to have as usable
a system at each stage as fast as possible.


Michael