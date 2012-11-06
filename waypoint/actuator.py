"""
This bridges the the waypoint codebase to the actator.
Whenever the component receives a message it sends the character "71"
over the serial port to the client.

"""

import Axon
import time
import os
import serial
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Util.PureTransformer import PureTransformer
from Kamaelia.Util.Console import ConsoleEchoer

import waypoint.core

class SerialSender(Axon.ThreadedComponent.threadedcomponent):
    """ Derived from kamaelia.git/Sketches/MPS/ArduinoRelated/ArdCube.py#SerialIO"""
    serialports = ['/dev/ttyUSB0', '/dev/ttyUSB1', '/dev/ttyUSB2', '/dev/ttyACM0', '/dev/ttyACM1', '/dev/ttyACM2']
    baudrate = 9600
    def main(self):  # FIXME: Shutdown for this component does not play nicely with others

        # Wait for one of the serial ports to come online...
        serialport = None
        havetag = False
        while serialport is None:
            for port in self.serialports:
                if os.path.exists(port):
                    print "FOUND PORT", port
                    serialport = port
            if serialport is None:
                # Throw away any messages sent while we're waiting for the serial port to exist...
                for msg in self.Inbox("inbox"):
                    pass
            time.sleep(0.1)

        ser = serial.Serial(serialport, self.baudrate)
        serialinput = ""
        while not havetag:
            
             serialinput += ser.read()
             if "\n" in serialinput:
                 waypoint.core.system_nodeid = serialinput.strip()
                 havetag = True

        while True:
            for msg in self.Inbox("inbox"):
                ser.write(str(msg))
            time.sleep(0.01)

def Actuator(char_to_send=chr(71)):
    return Pipeline(
              PureTransformer(lambda x: char_to_send),
#              ConsoleEchoer(),
              SerialSender()
           )

if __name__ == "__main__":
     pass
#    SerialSender().run()


