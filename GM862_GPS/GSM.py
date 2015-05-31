import sys
import time
import serial

class GSM(object):
    """Class to switch on and do GSM stuff"""

    "lots of x's as it wont run with certain characters so have been replaced with x"
    gsm = ("@x$xxxxxxx\nxx\rxx?_?????????\x1bxxxx !\"#x%&'()*+,-./0123456789:;<=>?"
           "xABCDEFGHIJKLMNOPQRSTUVWXYZxxxx`xabcdefghijklmnopqrstuvwxyzxxxxx")

    ext = ("````````````````````^```````````````````{}`````\\````````````[~]`"
        "|````````````````````````````````````?``````````````````````````")

    TimeoutNormal = 1
    TimeoutLong = 10
   
    def __init__(self):
        print("The GSM module has been initialised")
        self.serialConnect = None

    def SerialConnect(self, serPort = 'COM5', baud = 19200, bytes = serial.EIGHTBITS, 
                      par = serial.PARITY_NONE, stop = serial.STOPBITS_ONE, time = GSM.TimeoutNormal):
        """connect to serial port, default com5"""
        try:
            self.serialConnect = serial.Serial(
                                   port = serPort,
                                   baudrate = baud,
                                   bytesize = bytes,
                                   parity = par,
                                   stopbits = stop,
                                   timeout = time)
            print("Serial port open on: " + serPort)
            self.serialBaud = baud
            return True
        except:
            print("Failed to open serial port: ", sys.exc_info()[0])
            return False

    def SerialDisconnect(self):
        """close serial port"""
        if(self.serialConnect.isOpen()):
            self.serialConnect.close()
            print("serial port closed")
        else:
            print("serial port not closed as was not open in the first place")

    def SendCommand(self, command):
        """sends a command to the device"""
        ans = None
        if(self.serialConnect.isOpen()):
            self.serialConnect.write(command.encode())
            ser.flush()
            ans = self.serialConnect.read(1000)
            self.serialConnect.flush()
            print (ans.strip())
            return ans.strip()
        else:
            return ans

    def gsm_encode(self, plaintext):
        """converts string into 7-bit gsm characters for sms"""
        res = bytearray()
        for c in plaintext:
            idx = self.gsm.find(c);
            if idx != -1:
                res.append(idx)
                continue
            idx = self.ext.find(c)
            if idx != -1:
                res.append(27)
                res.append(idx)
        "return the byte array not the hex bytes"
        return res

    def Initialise862SerialSettings(self):
        """initialise the serial connection between 862 and master"""
        if(self.serialConnect.isOpen()):
            "Auto baud to let the modem know the baud rate"
            self.SendCommand("AT\r")

            "Fix baud to self.serialBaud now they can communicate"
            sendBaud = "AT+IPR=" + str(self.serialBaud) + "\r"
            print(sendBaud)
            SendCommand(sendBaud)
        else:
            print("serial port is not open, cannot initialise")
            return False

    
    
    def gsm_SendMessageToPhone(self, number, message):
        """method to send a text message to a phone number"""
        try:
            if(self.serialConnect.isOpen()):
                print("Serial port is open")
                phoneNumberCmd = "AT+CMGS="+number+"\r"
                self.serialConnect.write(phoneNumberCmd.encode())
                self.serialConnect.flush()
                response = serialPort.read(1000)
                self.serialConnect.flush()
                print(response.strip()) 
                """Send SMS. Set phone number, wait for > then send message in IRA format 
                ending with ctrl-z (0x1a) or 0x1b to cancel message send
                wait for > error 331 is network service, cmgs<message ref number> is valid sent result
                dont always get the >... just send anyway"""    
                self.serialConnect.write(self.gsm_encode("Hello world") + b"\x1A")
                self.serialConnect.flush()
                print(serialPort.read(250).strip())
                self.serialConnect.flush()
                time.sleep(1)
            else:
                print("Serial port is not open")
        except:
            print("Error checking serial port open: ", sys.exc_info()[0])


if __name__ == "__main__":
    print("This module is not callable")
    input("\n\nPress the enter key to exit.")



