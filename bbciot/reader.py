"""
Code related to a reader profile
"""
from Kamaelia.Util.Backplane import *
from Kamaelia.Chassis.Pipeline import Pipeline
from bbciot.core import FestivalTagReader
from Kamaelia.Chassis.ConnectedServer import FastRestartServer
from Kamaelia.Util.Console import ConsoleEchoer

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

