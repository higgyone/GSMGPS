import sys
import time
import serial
import GM862

class GSM(object):
    """Class to switch on and do GSM stuff"""

    "lots of x's as it wont run with certain characters so have been replaced with x"
    gsm = ("@x$xxxxxxx\nxx\rxx?_?????????\x1bxxxx !\"#x%&'()*+,-./0123456789:;<=>?"
           "xABCDEFGHIJKLMNOPQRSTUVWXYZxxxx`xabcdefghijklmnopqrstuvwxyzxxxxx")

    ext = ("````````````````````^```````````````````{}`````\\````````````[~]`"
        "|````````````````````````````````````?``````````````````````````")
   
    def __init__(self, gm862):
        print("The GSM module has been initialised")   
        self.gm862 = gm862 

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

    def SendTextToPhone(self, number, message):
        """method to send a text message to a phone number"""
        try:
            if(self.gm862.serialConnect.isOpen()):
                print("Serial port is open GSM")
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

    def ExtendSimErrorResults(self):
        """Enable extended error result codes for SIM checking =1 is normal & =2 is verbose"""
        print("extend sim error results")
        self.gm862.SendCommand("AT+CMEE=2\r")

    def GetSimPresent(self):
        """Query SIM presence and status"""
        print("get sim present")
        self.gm862.SendCommand("AT+CPIN?\r")

    def GetRssiAndQuality(self):
        """Query RSSI and quality. Answer is <rssi>, <ber> with result 99 = not detected. 
        rssi higher number the better, ber only for voice quality, dont worry about it"""
        print("rssi and quality")
        self.gm862.SendCommand("AT+CSQ\r")

    def QueryNetworkStatus(self):
        """Query network status... repeat this until CREG: 0,1 or CREG:1,1 which means mobile registered on its home network"""
        print("network status")
        self.gm862.SendCommand("AT+CREG?\r")

    def QueryNetworkOperator(self):
        """Query network operator ID... this requires a few seconds. First network is one connected to
        note can take a while"""
        print("network operator")
        self.gm862.SetSerialTimeout(self.gm862.TimeoutLong)
        self.gm862.SendCommand("AT+COPS=?\r")
        self.gm862.SetSerialTimeout(self.gm862.TimeoutNormal)

    def SetSmsPduType(self, type = 1):
        """Set SMS type 0=PDU, 1=text. Use 1 as on PDU need to craft entire PDU"""
        print("set pdu type")
        self.gm862.SendCommand("AT+CMGF=" + str(type) + "\r")

    def CheckServiceNumber(self):
        """Check SMS service centre number... must have one or no SMS
        result is <number>,<type> note this is in SIM and persistant set by network... only needs checking once
        type is  145 - international or 129 - national """
        print("check service number")
        self.gm862.SendCommand("AT+CSCA?\r")


if __name__ == "__main__":
    print("This GSM module is not callable")
    input("\n\nPress the enter key to exit.")



