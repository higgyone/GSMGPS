import serial
import GGAParser
import GSM
from time import sleep

""" To turn on telit hold down button for 1 second """

TimeoutNormal = 1
TimeoutLong = 10

def Switch862Off():
    if(ser.isOpen()):
        "the module will shutdown after a maximum of 6 seconds"
        ser.timeout = 7
        SendCommand("AT#SHDN\r")
        print("Shutdown sent")
        ser.close()

def SendCommand(command):
    ans = None
    if(ser.isOpen()):
        ser.write(command.encode())
        ser.flush()
        ans = ser.read(1000)
        ser.flush()
        print (ans.strip())
        return ans.strip()

    return ans

""" Telit on 19200, set timeout to 1 second as no EOL character """
ser = serial.Serial(
   port = 'COM5',
   baudrate = 19200,
   bytesize = serial.EIGHTBITS,
   parity = serial.PARITY_NONE,
   stopbits = serial.STOPBITS_ONE,
   timeout = TimeoutNormal
)

"Auto baud to let the modem know the baud rate"
SendCommand("AT\r")

"Fix baud to 19200 now they can communicate"
SendCommand("AT+IPR=19200\r")

"Enable extended error result codes for SIM checking =1 is normal & =2 is verbose"
SendCommand("AT+CMEE=2\r")

"Query SIM presence and status"
SendCommand("AT+CPIN?\r")

"""Query RSSI and quality. Answer is <rssi>, <ber> with result 99 = not detected. 
rssi higher number the better, ber only for voice quality, dont worry about it"""
SendCommand("AT+CSQ\r")

#for i in range(0,10): 
"Query network status... repeat this until CREG: 0,1 or CREG:1,1 which means mobile registered on its home network"
SendCommand("AT+CREG?\r")

"Query network operator ID... this requires a few seconds. First network is one connected to"
""" Not using this takes too long 
ser.timeout = TimeoutLong
SendCommand("AT+COPS=?\r")
ser.timeout = TimeoutNormal 
"""

"Set SMS type 0=PDU, 1=text. Use 1 as on PDU need to craft entire PDU"
SendCommand("AT+CMGF=1\r")

"""Check SMS service centre number... must have one or no SMS
result is <number>,<type> note this is in SIM and persistant set by network... only needs checking once
type is  145 - international or 129 - national """
SendCommand("AT+CSCA?\r")

sms = GSM.GSM()
sms.gsm_SendMessageToPhone(ser, "0xxxxxxxxx","hello world")

#@TODO: need to do something to read incomming text messages if required
#AT+CMGR=<index> gets the sms. need to log index from unsolicited message 
"""
#delete text messages as they arrive after reading AT+CMGD=<index>

"Get GSM modem current time (not GPS)"
#SendCommand("AT+CCLK?\r")
"""
"""**********************GPS SECTION*********************************"""

"Get the GPS on/off status: 1 is on 0 is off. 1 is default after startup"
SendCommand("AT$GPSP?\r")

"""reset GPS. 0=hardware reset, 1=cold start, 2= warmstart, 3= hotstart
Just in case needed later"""
#SendCommand("AT$GPSR=0\r")

"Get antenna voltage (/1000)"
SendCommand("AT$GPSAV?\r")

"Get antenna current"
SendCommand("AT$GPSAI?\r")

"""

gpsParser = GGAParser.GgaGpsParser()

for i in range(0,10):
    "get GPS GGA sentence"
    gpsData = SendCommand("AT$GPSACP\r")
    gpsParser.ParseString(gpsData)
    sleep(2)
#Parse GGA reponse...
"""

#Switch862Off()



