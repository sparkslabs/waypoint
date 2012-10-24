#!/usr/bin/python

import Axon
from rfidtag import *

from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Util.Console import ConsoleEchoer
import time, sys
from Kamaelia.Util.Backplane import *
from Kamaelia.Chassis.ConnectedServer import FastRestartServer
from Kamaelia.Util.PureTransformer import PureTransformer  #  CHANGE: EXTRA (missed import)
import json                                                #  CHANGE: EXTRA (missed import)
from Kamaelia.Internet.TCPClient import TCPClient          #  CHANGE: EXTRA (missed import)
from Kamaelia.File.Writing import SimpleFileWriter         #  CHANGE: EXTRA (missed import)

class TagReader(Axon.ThreadedComponent.threadedcomponent):
    def main(self):
        rfidtag_init()
        rfidtag_config(5000,0)

        while True:
            num = rfidtag_seek()
            if num == 1:
                tag =  rfidtag_getID1() 
                print "Tag: ", tag
                self.send(tag, "outbox")
            time.sleep(0.01)
        rfidtag_close()

def FestivalTagReader(nodeid):
    return Pipeline( 
                     TagReader(),
                     PureTransformer(lambda tagid: [time.time(), tagid, nodeid]),
                     PureTransformer(lambda x: json.dumps(x)+"\n") # CHANGE: Added \n
                   )
class GotShutdownMessage(Exception):
    pass

class LineSplitter(Axon.Component.component):  # CHANGE: EXTRA
    def main(self):
        try:
            buffer = ""
            while True:
                for message in self.Inbox():
                    buffer += message
                while "\n" in buffer:
                    x = buffer.find("\n")
                    msg = buffer[:x]
                    buffer = buffer[x+1:]
                    self.send(msg,"outbox")
                if self.dataReady("control"):
                    raise GotShutdownMessage()
                if not self.anyReady():
                    self.pause()
                    yield 1

        except GotShutdownMessage:
            self.send(self.recv("control"), "signal")
            yield 1
            return
            
        self.send(Axon.Ipc.producerFinished(), "signal")
        yield 1

def MyProtocol(**args):
    return SubscribeTo("TAGS")

print sys.argv
if "reader" in sys.argv[0]: # CHANGE: handle case sys.argv == ./reader
    Backplane("TAGS").activate()

    Pipeline(
        FestivalTagReader(1),
        PublishTo("TAGS")
    ).activate()

    FastRestartServer(protocol=MyProtocol, port=1500).activate()

    Pipeline(
        SubscribeTo("TAGS"),
        ConsoleEchoer()
    ).run()

if "FEP" in sys.argv[0]: # CHANGE: handle case sys.argv == ./FEP
#    readers = [ ("192.168.2.100",1500),("192.168.2.101",1500),("192.168.2.102",1500) ] # CHANGE for testing with one node
    readers = [ ("192.168.2.4",1500) ]  # CHANGE for testing with one node

    Backplane("TAGEVENTS").activate()

    for reader in readers:
       ip, port = reader
       Pipeline(
           TCPClient(ip,port),
           LineSplitter(),                     # CHANGE: EXTRA
           PublishTo("TAGEVENTS")
       ).activate()

    Pipeline(  # CHANGE: Debugging on the FEP - see what data we're recieving
        SubscribeTo("TAGEVENTS"),
        ConsoleEchoer()
    ).activate()

    Pipeline(
        SubscribeTo("TAGEVENTS"),
        PureTransformer(lambda x: x+"\n"), # CHANGE: Related to line splitter (which swallows the \n)
        SimpleFileWriter("tagevents.log")
    ).run()
