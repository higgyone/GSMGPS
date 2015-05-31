import serial
import GGAParser
import GSM
import GM862
from time import sleep

""" To turn on telit hold down button for 1 second """
"""
TimeoutNormal = 1
TimeoutLong = 10



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
"""
""" Telit on 19200, set timeout to 1 second as no EOL character """
"""
ser = serial.Serial(
   port = 'COM5',
   baudrate = 19200,
   bytesize = serial.EIGHTBITS,
   parity = serial.PARITY_NONE,
   stopbits = serial.STOPBITS_ONE,
   timeout = TimeoutNormal
)
"""

"""

"""
gm862 = GM862.GM862()

gm862.InitialiseSerial()

gsm = GSM.GSM(gm862)
gsm.ExtendSimErrorResults()
gsm.GetSimPresent()
gsm.GetRssiAndQuality()
gsm.QueryNetworkStatus()
#gsm.QueryNetworkOperator()
gsm.SetSmsPduType()
gsm.CheckServiceNumber()


"""

sms = GSM.GSM()
sms.gsm_SendMessageToPhone(ser, "0xxxxxxxxx","hello world")
"""

#@TODO: need to do something to read incomming text messages if required
#AT+CMGR=<index> gets the sms. need to log index from unsolicited message 
"""
#delete text messages as they arrive after reading AT+CMGD=<index>

"Get GSM modem current time (not GPS)"
#SendCommand("AT+CCLK?\r")
"""
"""**********************GPS SECTION*********************************"""
"""
"Get the GPS on/off status: 1 is on 0 is off. 1 is default after startup"
SendCommand("AT$GPSP?\r")
"""

"""reset GPS. 0=hardware reset, 1=cold start, 2= warmstart, 3= hotstart
Just in case needed later"""
#SendCommand("AT$GPSR=0\r")

"""
"Get antenna voltage (/1000)"
SendCommand("AT$GPSAV?\r")

"Get antenna current"
SendCommand("AT$GPSAI?\r")
"""
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



