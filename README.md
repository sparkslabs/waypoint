Waypoint
========

A toolset for recording trails between waypoints by tagging tags against readers.

This is a package that is aimed at getting a codebase suitable for
running a basic IOT enhanced event.

The aim of this package is as follows:
    * You should have installed a working Ubuntu 12.04 box
    * You should be able to install this package
    * You should be able to configure running profiles in /etc/waypointservice
        * Dependent on these profiles, when this box starts up it should
          start up a process that configures the process as tag reader node
          or as an collation node, or both.
        * This should be able to happen without human interaction - except
          for initial configuration

Currently the package does most of these points, except for configuration.
Installation of the debian package for this codebase will result in a waypointservice
that starts up at boot, and allows for plug and play with both readers and actuators.


DEPENDENCIES / Installation thereof
===================================
Requirements required for this to work:
    sudo apt-get install git
    sudo apt-get install python-dev
    sudo apt-get install swig
    sudo apt-get install cython
    sudo apt-get install libusb-dev
    sudo apt-get install python-serial


Kamaelia + Axon:
    git clone https://github.com/sparkslabs/kamaelia.git
    cd kamaelia
    cd Code/Python/Axon
    sudo python setup.py install
    cd ../Kamaelia
    sudo python setup.py install


python-rfidtag:

    git clone https://github.com/sparkslabs/python-rfidtag.git
    cd cd python-rfidtag
    sudo python setup.py install

If not enabled on the box, enable ssh - this simplifies managing an installation.


INSTALL
=======

The preferred installation approach is to install the dependencies and
then install the debian package.

Manual installation
-------------------

Inside the waypoint tarball:
    sudo python setup.py install

Then:
    sudo waypoint.mkdirs

    
RUNNING A STANDALONE READER
===========================

The touchatad/tikitag readers require root privileges so must be run as follows:
    sudo waypoint_reader


This will only work if a reader is plugged in. It furthermore currently has
a dependency on there also being an arduino plugged.

Assuming the hardware is OK, this will log tagged data to:

    * /var/log/waypointservice/tagsread.log

The format of that file is "\n" delimited JSON array objects of format:
    * Timestamp (float value)
    * tag id as a decimal integer value
    * Defined reader id

Configuration of reader
-----------------------
At present the reader ID is not configurable without modification of the
code. In practice this means modifying /usr/[local/]bin/waypoint_reader
in a hopefully obvious way. This will change shortly. To give an idea of
complexity of change, the entirety of that file is presented here:

    from waypoint.reader import TagReaderClient

    # All the arguments here should be externally configurable
    TagReaderClient(collator_ip = "127.0.0.1",
                    collator_port = 1600,
                    node_id=1,
                    logfile="/var/log/waypointservice/tagsread.log",
                    debug_port=1500).run()


It should be obvious from the above and how this would need changing.

TBD:
    
Installation as a collator / etc (see docs/todo.txt)

Configuration
=============

Configuration is based on a cascading/inheriting approach. While this make
look more complex than some schemes, its specifically designed to simplify
maintance and configuration.

Most of the nodes in a waypoint system will be tag readers. Some will be
collators. Others may have as yet to be defined roles for sensing and
control.


Michael