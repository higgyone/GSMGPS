import sys
import time
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

    def InitialiseGSM(self):
        self.ExtendSimErrorResults()
        self.GetSimPresent()
        self.GetRssiAndQuality()
        self.QueryNetworkStatus()

        #gsm.QueryNetworkOperator()
        self.SetSmsPduType()
        self.CheckServiceNumber()

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
                self.gm862.serialConnect.write(phoneNumberCmd.encode())
                self.gm862.serialConnect.flush()
                response = self.gm862.serialConnect.read(1000)
                self.gm862.serialConnect.flush()
                print(response.strip()) 
                """Send SMS. Set phone number, wait for > then send message in IRA format 
                ending with ctrl-z (0x1a) or 0x1b to cancel message send
                wait for > error 331 is network service, cmgs<message ref number> is valid sent result
                dont always get the >... just send anyway"""    
                self.gm862.serialConnect.write(self.gsm_encode(message) + b"\x1A")
                self.gm862.serialConnect.flush()
                print(self.gm862.serialConnect.read(250).strip())
                self.gm862.serialConnect.flush()
                time.sleep(1)
            else:
                print("Serial port is not open")
        except:
            print("Error with serial port: ", sys.exc_info()[0])

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
        """Query network status... success is CREG: 0,1; 1,1; 0,5 or 1,5  which means mobile registered on its home (1) or roaming (5) network"""
        connectedToNetwork = False
        print("network status")
        networks = self.gm862.SendCommand("AT+CREG?\r")
        if(len(networks) == 3):
            if(networks[2] == b'OK'):
                if "ERROR" not in str(networks[1]):
                    if(networks[1].endswith(b"5") or networks[1].endswith(b"1")):
                        print("Registered on a network " + str(networks[1]))
                        connectedToNetwork = True
                    else:
                        print("Not registered on a network: " + str(networks[1]))                    
                else:
                    print("Error found: " + str(networks[2]))
            else:
                print("Error sending networks command")
        else:
            print("Error in get network status response")
        
        if(connectedToNetwork):
            self.gm862.State_Registered = True
        else:
            self.gm862.State_Registered = False
        return connectedToNetwork

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

    def GetodemCurrentTime(self):
        """Gets the modems current time and not that of GPS"""
        self.gm862.SendCommand("AT+CCLK?\r")


if __name__ == "__main__":
    print("This GSM module is not callable")
    input("\n\nPress the enter key to exit.")



