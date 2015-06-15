import GM862
import GGAParser

class GPS(object):
    """Class to get GPS data"""

    def __init__(self, gm862):
        print("The GPS module has been initialised")   
        self.gm862 = gm862 
        self.gpsParser = GGAParser.GgaGpsParser()


    def InitialiseGPS(self):
        """initialise GPS"""
        if not self.IsGpsOn():
            self.PowerGpsOn()


    def IsGpsOn(self):
        """Get the GPS powered status"""
        status = self.gm862.SendCommand("AT$GPSP?\r")
        if(status[1].endswith(b"1")):
           return True
        else:
           return False

    def PowerGpsOn(self):
        """Power the GPS on"""
        self.gm862.SendCommand("AT$GPSP=1\r")

    def PowerGpsOff(self):
        """Power the GPS off"""
        self.gm862.SendCommand("AT$GPSP=0\r")

    def ResetGps(self, resetType = "0"):
        """Reset GPS 0=hardware reset, 1=cold start, 2= warmstart, 3= hotstart"""
        if(resetType == "0" or resetType == "1" or resetType == "2" or resetType == "3"):
            self.gm862.SendCommand("AT$GPSR=" + resetType + "\r")
        else:
            self.gm862.SendCommand("AT$GPSR=0\r")

    def GetAntennaVoltage(self):
        """return the antenna voltage"""
        return self.gm862.SendCommand("AT$GPSAV?\r")

    def GetAntennaCurrent(self):
        """return the antenna current"""
        return self.gm862.SendCommand("AT$GPSAI?\r")

    def GetGpsData(self):
        """return GPS data"""
        data = self.gm862.SendCommand("AT$GPSACP\r")
        print("GPS string: " + str(data))
        self.ParseGPSData(data)

    def ParseGPSData(self, listGPSData):
        """parse the GPS data"""
        self.gpsParser.ParseGpsList(listGPSData)


if __name__ == "__main__":
    print("This GPS module is not callable")
    input("\n\nPress the enter key to exit.")


