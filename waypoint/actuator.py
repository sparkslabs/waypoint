"""
This bridges the the bbciot codebase to the actator.
Whenever the component receives a message it sends the character "71"
over the serial port to the client.

"""

import Axon
import time
import serial
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Util.PureTransformer import PureTransformer

class SerialSender(Axon.ThreadedComponent.threadedcomponent):
    """ Derived from kamaelia.git/Sketches/MPS/ArduinoRelated/ArdCube.py#SerialIO"""
    serialport = '/dev/ttyUSB0'
    baudrate = 9600
    def main(self):  # FIXME: Shutdown for this component does not play nicely with others
        ser = serial.Serial(self.serialport, self.baudrate)
        while True:
            for msg in self.Inbox("inbox"):
                ser.write(str(msg))
            time.sleep(0.01)

def Actuator(char_to_send=chr(71)):
    return Pipeline(
              PureTransformer(lambda x: char_to_send),
              SerialSender()
           )
