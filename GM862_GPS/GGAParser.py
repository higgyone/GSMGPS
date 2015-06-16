import datetime
import GPSGGA
import GM862

class GgaGpsParser(object):
    """Parse a GGA string"""

    def __init__(self, gm862):
        print("A gga parser has been objectified")
        self.gm862 = gm862


    def ParseString(self, ggaString):
        if(ggaString.startswith( b"AT$GPSACP")):
            ggaStrip=ggaString.lstrip(b"\r\r\nAT$GPSACP:")
            ggaValues = ggaStrip.split(b',')
            print(str("{0:<15}{1}".format("Time is:", ggaValues[0].strip())))
            print("{0:<15}{1}".format("Latitude is:",ggaValues[1].strip()))
            print("{0:<15}{1}".format("Longitude is:",ggaValues[2].strip()))
            print("{0:<15}{1}".format("HDOP is:",ggaValues[3].strip()))
            print("{0:<15}{1}".format("Altitude is:",ggaValues[4].strip()))
            print("{0:<15}{1}".format("Fix is:",ggaValues[5].strip()))
            print("{0:<15}{1}".format("COG is:",ggaValues[6].strip()))
            print("{0:<15}{1}".format("SPGKm is:",ggaValues[7].strip()))
            print("{0:<15}{1}".format("SPGN is:",ggaValues[8].strip()))
            print("{0:<15}{1}".format("Date is:",ggaValues[9].strip()))
            print("{0:<15}{1}".format("No. Sats are:",ggaValues[10].rstrip(b'\r\n\r\nOK')))

    def ParseGpsList(self, ggaList):
        """parse a list of gga data"""
        print("List length = " + str(len(ggaList)))
        if(len(ggaList) == 3):
            if(ggaList[2] == b"OK"):
                if(ggaList[0].startswith(b"AT$GPSACP")):
                    ggaValues = ggaList[1].split(b',')
                    if(len(ggaValues) == 11):
                        gpsData = GPSGGA.GPSGGA()
                        time = ggaValues[0].lstrip(b"$GPSACP: ")
                        dateTime = "{}-{}".format(ggaValues[9].decode("utf-8"), time.decode("utf-8"))
                        dt = datetime.datetime.strptime(dateTime, "%y%m%d-%H%M%S.%f")
                        gpsData.DateTime = dt
                        gpsData.Latitude = ggaValues[1]
                        gpsData.Longitude = ggaValues[2]
                        gpsData.Hdop = ggaValues[3]
                        gpsData.Altitude = ggaValues[4]
                        gpsData.Fix = ggaValues[5]
                        gpsData.Cog = ggaValues[6]
                        gpsData.Spgkm = ggaValues[7]
                        gpsData.Spgn = ggaValues[8]
                        gpsData.Sats = ggaValues[10]

                        """if no latitude value or 0 sats then not a valid fix"""
                        if ggaValues[10] == b"00" or not ggaValues[1]:
                            self.gm862.State_Posfix = False
                        else:
                            self.gm862.State_Posfix = True

                        gpsData.ValidFix = self.gm862.State_Posfix

                        print(gpsData)                       
                    else:
                        print(str(len(ggaValues)) + " found in gps data, should be 10 Values")
                else:
                    print("GPS data does not start with \"AT$GPSACP\" cannot parse it")
            else:
                print("No \"OK\" response from get GPS data requrest")
        else:
            print("GPS data request response not valid")

if __name__ == "__main__":
    print("This GPS Parser module is not callable")
    input("\n\nPress the enter key to exit.")


