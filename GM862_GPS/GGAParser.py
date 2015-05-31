#Class to parse a GGA GPS string

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


if __name__ == "__main__":
    print("This module is not callable")
    input("\n\nPress the enter key to exit.")


