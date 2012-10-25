"""
Core code
"""

import Axon
from rfidtag import *    
import time
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Util.PureTransformer import PureTransformer
import json

class TagReader(Axon.ThreadedComponent.threadedcomponent):
    delay = 0.01
    def main(self):
        rfidtag_init()
        rfidtag_config(5000,0)

        while True:
            num = rfidtag_seek()
            if num == 1:
                tag =  rfidtag_getID1() 
                self.send(tag, "outbox")
            time.sleep(self.delay)
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

class Logger(Axon.Component.component):
    logfile = "test.log"
    def logline(self, line):
        try:
            x = open(self.logfile,"a")
        except IOError:
            x = open(self.logfile,"w")
        x.write(line+"\n")
        x.flush()
        x.close()


    def main(self):
        try:
            while True:
                for message in self.Inbox():
                    self.logline(message)
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




















