"""

Currently called the front end processor, this actually
collates data from tag readers for use by whole event analysis

"""
from Kamaelia.Util.Backplane import *
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Internet.TCPClient import TCPClient
from Kamaelia.Util.Console import ConsoleEchoer
from bbciot.core import LineSplitter
from Kamaelia.Util.PureTransformer import PureTransformer
from Kamaelia.File.Writing import SimpleFileWriter

from Kamaelia.Chassis.ConnectedServer import FastRestartServer

def MyProtocol(**args):
    return Pipeline(
            LineSplitter(),
            PublishTo("TAGEVENTS")
           )


def RunCollator(readers=None, listenport=1600):

    Backplane("TAGEVENTS").activate()

    Pipeline(
        SubscribeTo("TAGEVENTS"),
        ConsoleEchoer()
    ).activate()

    FastRestartServer(protocol=MyProtocol, port=listenport).activate()

    Pipeline(
        SubscribeTo("TAGEVENTS"),
        PureTransformer(lambda x: x+"\n"), # line splitter swallows \n's
        SimpleFileWriter("tagevents.log")
    ).run()
