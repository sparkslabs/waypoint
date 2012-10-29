"""

Currently called the front end processor, this actually
collates data from tag readers for use by whole event analysis

"""
import json
import time
from Kamaelia.Util.Backplane import *
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Chassis.PAR import PAR
from Kamaelia.Internet.TCPClient import TCPClient
from Kamaelia.Util.Console import ConsoleEchoer
from bbciot.core import LineSplitter
from Kamaelia.Util.PureTransformer import PureTransformer
from Kamaelia.File.Writing import SimpleFileWriter
from bbciot.core import Logger

from Kamaelia.Chassis.ConnectedServer import FastRestartServer


def IncomingNodeEventsProtocol(**conninfo):
    return Pipeline(
            LineSplitter(),
            PureTransformer(lambda x: json.loads(x)), # Deserialise
            PureTransformer(lambda x: [conninfo, time.time(), x]), # Tag with connection info
            PublishTo("TAGEVENTS")
           )


def Collator(listenport=1600, logfile="collated_tag_events.log"):
    return PAR (
                Backplane("TAGEVENTS"),

                Pipeline(
                    SubscribeTo("TAGEVENTS"),
                    PureTransformer(lambda x: json.dumps(x)+"\n"), # \n delimited JSON records
                    ConsoleEchoer()
                ),

                FastRestartServer(protocol=IncomingNodeEventsProtocol, port=listenport),

                Pipeline(
                    SubscribeTo("TAGEVENTS"),
                    PureTransformer(lambda x: json.dumps(x)), # JSON records
                    Logger(logfile=logfile) # Logger adds \n to delimit records
                )
               )
