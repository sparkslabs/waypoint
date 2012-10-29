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

This package currently represents about a days' work in total

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

To be nice to Michael when working on the box :
    sudo apt-get install joe

If not enabled on the box, enable ssh.


INSTALL
=======

Inside the bbciot tarball:
    sudo python setup.py install

Then:
    sudo bbciot.mkdirs

RUNNING A STANDALONE READER
===========================

The touchatad/tikitag readers require root privileges so must be run as follows:
    sudo bbciot_reader


This will only work if a reader is plugged in. It furthermore currently has
a dependency on there also being an arduino plugged.

Assuming the hardware is OK, this will log tagged data to:

    * /var/run/bbciotservice/tagsread.log

The format of that file is "\n" delimited JSON array objects of format:
    * Timestamp (float value)
    * tag id as a decimal integer value
    * Defined reader id

FIXME: Configuration of reader
------------------------------
At present the reader ID is not configurable without modification of the
code. In practice this means modifying /usr/local/bin/bbciot_reader in an obvious way. This will change PDQ. To give an idea of complexity of change,
the entiterty of that file is presented here:

    from bbciot.reader import TagReaderClient

    # All the arguments here should be externally configurable
    TagReaderClient(collator_ip = "127.0.0.1",
                    collator_port = 1600,
                    node_id=1,
                    logfile="/var/run/bbciotservice/tagsread.log",
                    debug_port=1500).run()


It should be obvious where and how this would need changing. This is
as I say however less than ideal


TBD:

Installation as a collator / etc (see docs/todo.txt)





Michael