"""

An analyser takes logged events from the data archive, processes them and triggers the actuator to do something.

This is essentially an overall analyser which performs aggregate analysis. (eg total number of tag taps)

We need an aggregation function to be implemented.  

This MUST provide an aggregation over the entire ‘event’ or ‘festival’ period of the number of tags scanned.

And if development time permits, SHOULD be able to provide the above on a sliding time window basis (i.e. the total number of tags scanned within the last x minutes from  the time of the query) AND provide this function on a zone (tag reader) by zone basis.
The above to be co-located with the FEP.
 
That a reduced form of aggregator should be co-located with each tag reader and provide an output to indicate that a tag has been scanned.  There should be considerable code re-use between this function and the more fully functioned aggregator described above.

To develop the system as demonstrated into a standalone tag reader solution in which each tag reader is able to gather local activity data, drive an actuator for user feedback but that these are not integrated thereby forcing any aggregation or post event analysis to be performed off line.


"""

import json
import os
import time
import Axon
from Kamaelia.Chassis.Pipeline import Pipeline

def slurp(filename):
    f = open(filename)
    contents = f.read()
    f.close()
    return contents

class FileWatcher(Axon.ThreadedComponent.threadedcomponent):
    watchfile = "/var/run/bbciotservice/collated_tag_events.log"
    def main(self):
        lastchange = 0
        while True:
            stat = os.stat(self.watchfile)
            if stat.st_mtime > lastchange:
                self.send(("changed", self.watchfile), "outbox")
            time.sleep(0.01)

class GotShutdownMessage(Exception):
    pass


class FileSlurper(Axon.ThreadedComponent.threadedcomponent):
    slurpfile = "/var/run/bbciotservice/collated_tag_events.log"
    def main(self):
        while True:
            for _ in self.Inbox("inbox"):
                raw_file = slurp(self.slurpfile)
                json_records = raw_file.rstrip().split("\n")
                json_events = [ json.loads(x) for x in json_records]
                self.send(json_events, "outbox")
            time.sleep(0.01)


class UniqueTags(Axon.Component.component):
    def main(self):
        try:
            while True:
                for tagevents in self.Inbox():
                    seen_tags = set()
                    for tagevent in tagevents:
                        conninfo, timestamp, noderec = tagevent
                        _node_timestamp, tagid, nodeid = noderec
                        seen_tags.add(tagid)
                    self.send(seen_tags, "outbox")

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

class Uniq(Axon.Component.component):
    def main(self):
        try:
            last = None
            while True:
                for message in self.Inbox():
                    if message != last:
                        last = message
                        self.send(last, "outbox")

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


# This is inefficient, but has a primary / initial aim of "just working"
def AllTimeAggregateAnalyser(logfile):
    return Pipeline(
                FileWatcher(watchfile=logfile), # Wait for file to change
                FileSlurper(slurpfile=logfile), # When it does, read it
                UniqueTags(),                   # Then isolate unique tags inside
                Uniq()                          # Remove duplicate events
           )
