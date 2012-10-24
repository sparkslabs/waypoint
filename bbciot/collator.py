"""

Currently called the front end processor, this actually
collates data from tag readers for use by whole event analysis

"""
from Kamaelia.Util.Backplane import *
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Chassis.PAR import PAR
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


def Collator(readers=None, listenport=1600):
    return PAR (
                Backplane("TAGEVENTS"),

                Pipeline(
                    SubscribeTo("TAGEVENTS"),
                    ConsoleEchoer()
                ),

                FastRestartServer(protocol=MyProtocol, port=listenport),

                Pipeline(
                    SubscribeTo("TAGEVENTS"),
                    PureTransformer(lambda x: x+"\n"), # line splitter swallows \n's
                    SimpleFileWriter("tagevents.log")
                )
               )
