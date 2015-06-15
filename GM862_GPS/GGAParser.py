import datetime
import GPSGGA

class GgaGpsParser(object):
    """Parse a GGA string"""

    def __init__(self):
        print("A gga parser has been objectified")


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
        print("List length = " + str(len(ggaList)))
        if(len(ggaList) == 3):
            if(ggaList[2] == b"OK"):
                if(ggaList[0].startswith(b"AT$GPSACP")):
                    ggaValues = ggaList[1].split(b',')
                    if(len(ggaValues) == 11):
                        #gpsData = GPSGGA.GPSGGA()
                        dateTime = "{}-{}".format(ggaValues[9].decode("utf-8"), (ggaValues[0].lstrip(b"$GPSACP: ")).decode("utf-8"))
                        dt = datetime.datetime.strptime(dateTime, "%y%m%d-%H%M%S.%f")
                        print(dateTime)
                        print(str("{0:<15}{1}".format("Time is:", ggaValues[0].lstrip(b"$GPSACP: "))))
                        print("{0:<15}{1}".format("Latitude is:", ggaValues[1]))
                        print("{0:<15}{1}".format("Longitude is:", ggaValues[2]))
                        print("{0:<15}{1}".format("HDOP is:", ggaValues[3]))
                        print("{0:<15}{1}".format("Altitude is:", ggaValues[4]))
                        print("{0:<15}{1}".format("Fix is:", ggaValues[5]))
                        print("{0:<15}{1}".format("COG is:", ggaValues[6]))
                        print("{0:<15}{1}".format("SPGKm is:", ggaValues[7]))
                        print("{0:<15}{1}".format("SPGN is:", ggaValues[8]))
                        print("{0:<15}{1}".format("Date is:", ggaValues[9]))
                        print("{0:<15}{1}".format("No. Sats are:", ggaValues[10]))
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


