import serial
import GGAParser
import GSM
import GM862
import GPS
from time import sleep

""" To turn on telit hold down button for 1 second """

gm862 = GM862.GM862()

intialised = gm862.InitialiseSerial()
#gm862.SendCommand("ATZ")

if(intialised):
    print("Module initialised: " + str(gm862.State_Initialized))

    gsm = GSM.GSM(gm862)
    gsm.InitialiseGSM()

    """
    if(gm862.State_Registered):
        gsm.SendTextToPhone("0xxxxxxxxxx", "Registered on network")
    """
    gps = GPS.GPS(gm862)
    gps.InitialiseGPS()
    print("GPS power: " + str(gps.IsGpsOn()))
    print("GPS antenna voltage: " + str(gps.GetAntennaVoltage()))
    print("GPS antenna current: " + str(gps.GetAntennaCurrent()))

    for i in range(0,10):
        "get GPS GGA sentence"
        gps.GetGpsData()
        sleep(2)
else:
    print("Falied to initialise")



#@TODO: need to do something to read incomming text messages if required
#AT+CMGR=<index> gets the sms. need to log index from unsolicited message 
"""
#delete text messages as they arrive after reading AT+CMGD=<index>
"""



