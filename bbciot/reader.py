"""
Code related to a reader profile
"""
from Kamaelia.Util.Backplane import *
from Kamaelia.Chassis.Pipeline import Pipeline
from bbciot.core import FestivalTagReader
from Kamaelia.Chassis.ConnectedServer import FastRestartServer
from Kamaelia.Util.Console import ConsoleEchoer
from Kamaelia.Internet.TCPClient import TCPClient

def MyProtocol(**args):
    return SubscribeTo("TAGS")

def RunReader(port=1500):
    Backplane("TAGS").activate()

    Pipeline(
        FestivalTagReader(1),
        PublishTo("TAGS")
    ).activate()

    FastRestartServer(protocol=MyProtocol, port=port).activate()

    # For debugging purposes
    Pipeline(
        SubscribeTo("TAGS"),
        ConsoleEchoer()
    ).run()

def TagReaderClient(collator_ip="127.0.0.1", collator_port=1600, debug_port=1600):
    Backplane("TAGS").activate()

    Pipeline(
        FestivalTagReader(1),
        PublishTo("TAGS")
    ).activate()

    FastRestartServer(protocol=MyProtocol, port=debug_port).activate()

    # Connect to Collator
    Pipeline(
        SubscribeTo("TAGS"),
        TCPClient(collator_ip,collator_port)
    ).activate()

    # For debugging purposes
    Pipeline(
        SubscribeTo("TAGS"),
        ConsoleEchoer()
    ).run()
