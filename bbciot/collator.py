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


def RunCollator(readers=None):

    if readers == None:
        readers = [ ("127.0.0.1",1500) ]  # Default to testing locally

    Backplane("TAGEVENTS").activate()

    for reader in readers:
       ip, port = reader
       Pipeline(
           TCPClient(ip,port),
           LineSplitter(),
           PublishTo("TAGEVENTS")
       ).activate()

    Pipeline(
        SubscribeTo("TAGEVENTS"),
        ConsoleEchoer()
    ).activate()

    Pipeline(
        SubscribeTo("TAGEVENTS"),
        PureTransformer(lambda x: x+"\n"), # line splitter swallows \n's
        SimpleFileWriter("tagevents.log")
    ).run()
