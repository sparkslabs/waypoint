"""
Code related to a reader profile
"""
from Kamaelia.Util.Backplane import *
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Chassis.PAR import PAR
from bbciot.core import FestivalTagReader
from Kamaelia.Chassis.ConnectedServer import FastRestartServer
from Kamaelia.Util.Console import ConsoleEchoer
from Kamaelia.Internet.TCPClient import TCPClient

def DebugTapProtocol(**args):
    return SubscribeTo("TAGS")

def TagReaderClient(collator_ip="127.0.0.1", collator_port=1600, node_id=1, debug_port=1500):

    # Use the PAR component to allow deferred activation, and to allow the components
    # to be used as a unit.

    return PAR(
                Backplane("TAGS"),

                Pipeline(
                    FestivalTagReader(node_id),
                    PublishTo("TAGS")
                ),

                FastRestartServer(protocol=DebugTapProtocol, port=debug_port),

                # Connect to Collator
                Pipeline(
                    SubscribeTo("TAGS"),
                    TCPClient(collator_ip,collator_port)
                ),

                # For debugging purposes
                Pipeline(
                    SubscribeTo("TAGS"),
                    ConsoleEchoer()
                ),
              )
