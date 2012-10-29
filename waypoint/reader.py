"""
Code related to a reader profile
"""
import json

from bbciot.core import FestivalTagReader
from bbciot.core import Logger
from bbciot.analysis import TagStreamEvent
from bbciot.actuator import Actuator
from Kamaelia.Chassis.ConnectedServer import FastRestartServer
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Chassis.PAR import PAR
from Kamaelia.Internet.TCPClient import TCPClient
from Kamaelia.Util.Backplane import *
from Kamaelia.Util.Console import ConsoleEchoer
from Kamaelia.Util.PureTransformer import PureTransformer

def DebugTapProtocol(**args):
    return SubscribeTo("TAGS")

def TagReaderClient(collator_ip="127.0.0.1",
                    collator_port=1600,
                    node_id=1,
                    logfile="tagsread.log",
                    debug_port=1500):

    # Use the PAR component to allow deferred activation, and to allow the components
    # to be used as a unit.

    return PAR(
                Backplane("TAGS"),

                Pipeline(
                    FestivalTagReader(node_id),   # FIXME: Probably don't want json encoding in here
                    PublishTo("TAGS")
                ),

                FastRestartServer(protocol=DebugTapProtocol, port=debug_port),

                # Connect to Collator
                Pipeline(
                    SubscribeTo("TAGS"),
                    TCPClient(collator_ip,collator_port)
                ),
                Pipeline(
                    SubscribeTo("TAGS"),
                    PureTransformer(lambda x: x[:-1]), # Strip trailing /n
                    Logger(logfile=logfile),
                ),

                Pipeline(
                    SubscribeTo("TAGS"),
                    PureTransformer(lambda x: x[:-1]),         # Strip trailing /n
                    PureTransformer(lambda x: json.loads(x) ), # Restore record
                    TagStreamEvent(temporal_separation=0.5),   # Extract tag taps
                    Actuator()
                ),

                # For debugging purposes
                Pipeline(
                    SubscribeTo("TAGS"),
                    ConsoleEchoer()
                ),
              )
