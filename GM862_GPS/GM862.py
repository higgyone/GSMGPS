import serial
import sys
import string

class GM862(object):
    """Class to initialise and talk to GM862 module"""
    
    TimeoutNormal = 1
    TimeoutLong = 10

    def __init__(self):
        """constructor"""
        print("The GM862 module has been initialised")
        self.serialConnect = None
        self.State_On = False
        self.StateInitialized = False
        self.State_Registered = False
        self.State_Posfix = False

    def SerialConnection(self, serPort = 'COM5', baud = 19200, bytes = serial.EIGHTBITS, 
                      par = serial.PARITY_NONE, stop = serial.STOPBITS_ONE):
        """connect to serial port, default COM5"""
        try:
            self.serialConnect = serial.Serial(
                                   port = serPort,
                                   baudrate = baud,
                                   bytesize = bytes,
                                   parity = par,
                                   stopbits = stop,
                                   timeout = self.TimeoutNormal)
            print("Serial port open on: " + serPort)
            self.serialBaud = baud
            return True
        except:
            print("Failed to open serial port: ", sys.exc_info()[0])
            return False

    def SerialDisconnection(self):
        """close serial port"""
        if(self.serialConnect.isOpen()):
            self.serialConnect.close()
            print("serial port closed")
        else:
            print("serial port not closed as was not open in the first place")
        self.State_Initialized = False

    def SetSerialTimeout(self, timeout):
        """set the timeout of the serial connection"""
        self.serialConnect.timeout = timeout

    def SendCommand(self, command, readBytes = 1000):
        """sends a command to the device"""
        response = None
        if(self.serialConnect.isOpen()):
            self.serialConnect.write(command.encode())
            self.serialConnect.flush()
            response = self.serialConnect.read(readBytes)
            self.serialConnect.flush()
            response = response.strip()
            responseList = response.split(b'\n')
            for i in range (len(responseList)):
                responseList[i] = responseList[i].strip()
            responseList = list(filter(None, responseList))
            print(str(responseList))
            return responseList
        else:
            return response

    def InitialiseSerial(self, serPort = 'COM5', baud = 19200, bytes = serial.EIGHTBITS, 
                      par = serial.PARITY_NONE, stop = serial.STOPBITS_ONE):
        """initialise the serial connection between 862 and master"""
        self.SerialConnection(serPort, baud, bytes, par, stop)

        if(self.serialConnect.isOpen()):
            "Auto baud to let the modem know the baud rate"
            print("autobaud")
            result = self.SendCommand("AT\r")

            """no response from unit check"""
            if not result:
                print("Failed to connect over serial... Switch Unit On")
                return False

            "Fix baud to self.serialBaud now they can communicate"
            print("setting baud rate")
            self.SendCommand("AT+IPR=" + str(self.serialBaud) + "\r")

            self.State_Initialized = True
            return True
        else:
            print("serial port is not open, cannot initialise")
            self.State_Initialized = False
            return False

    def Switch862Off(self):
        """switch module off"""
        if(self.serialConnect.isOpen()):
            "the module will shutdown after a maximum of 6 seconds"
            self.serialConnect.timeout = GM862.TimeoutLong
            print("shutting down")
            SendCommand("AT#SHDN\r")
            print("Shutdown sent")
            self.SerialDisconnect()
        else:
            print("serial port was not open in the first place")

if __name__ == "__main__":
    print("This GM862 module is not callable")
    input("\n\nPress the enter key to exit.")
