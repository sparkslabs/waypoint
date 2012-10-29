===============
 bbciotservice
===============

----------------------------------
manage bolster as a system service
----------------------------------

:Author: michael.sparks@bbc.co.uk
:Date:   2012-10-24
:Copyright: BBC, All Rights Reserved
:Version: 0.1
:Manual section: 7
:Manual group: System administration

.. TODO: authors and author with name <email>

SYNOPSIS
========

/etc/init.d/bbciotservice COMMAND
  
Supported commands:

* status, start, stop, restart, reload, force-reload, help

DESCRIPTION
===========

bbciotservice stops and starts the BBC IOT service.

OPTIONS
=======

Supports the standard commands:

* status        Is the bbciotservice running?
* start         Start bbciotservice
* stop          Stop bbciotservice
* restart       Stop/Start bbciotservice
* reload        Send a reload signal
* force-reload  Send a force reload signal
* help          Provide help on bbciotservice

SEE ALSO
========

TBD
