import datetime

class GPSGGA(object):
    """description of class"""

    def __init__(self):
        self.DateTime = None
        self.Latitude = None
        self.Longitude = None
        self.Hdop = None
        self.Altitude = None
        self.Fix = None
        self.Cog = None
        self.Spgkm = None
        self.Spgn = None
        self.Sats = None
        self.ValidFix = False

    def __str__(self):
        """stringify the GPS data"""
        time = "{0:<15}{1}".format("Time is:", self.DateTime.strftime("%H:%M:%S")).encode("utf-8")
        date = "{0:<15}{1}".format("Date is:",self.DateTime.strftime("%d/%m/%Y")).encode("utf-8")
        lat = "{0:<15}{1}".format("Latitude is:", self.Latitude.decode("utf-8")).encode("utf-8")
        lon = "{0:<15}{1}".format("Longitude is:", self.Longitude.decode("utf-8")).encode("utf-8")
        hdop = "{0:<15}{1}".format("HDOP is:", self.Hdop.decode("utf-8")).encode("utf-8")
        alt = "{0:<15}{1}".format("Altitude is:", self.Altitude.decode("utf-8")).encode("utf-8")
        fix = "{0:<15}{1}".format("Fix is:", self.Fix.decode("utf-8")).encode("utf-8")
        cog = "{0:<15}{1}".format("COG is:", self.Cog.decode("utf-8")).encode("utf-8")
        spkm = "{0:<15}{1}".format("SPGKm is:", self.Spgkm.decode("utf-8")).encode("utf-8")
        spgn = "{0:<15}{1}".format("SPGN is:", self.Spgn.decode("utf-8")).encode("utf-8")
        sats = "{0:<15}{1}".format("No. Sats are:", self.Sats.decode("utf-8")).encode("utf-8")
        fixValid = "{0:<15}{1}".format("Valid Fix:", self.ValidFix).encode("utf-8")

        gpsString = b"\r\n".join((time, date, lat, lon, hdop, alt, fix, cog, spkm, spgn, sats, fixValid))
        return gpsString.decode("utf-8")

    def __repr__(self):
        """Represent gps data"""
        gpsRepr = b",".join((self.DateTime.strftime("%H:%M:%S").encode("utf-8"), 
                            self.DateTime.strftime("%d/%m/%Y").encode("utf-8"),
                            self.Latitude,
                            self.Longitude,
                            self.Hdop,
                            self.Altitude,
                            self.Fix,
                            self.Cog,
                            self.Spgkm,
                            self.Spgn,
                            self.Sats,
                            self.ValidFix))

        return gpsRepr.decode("utf-8")

if __name__ == "__main__":
    print("This GPSGGA module is not callable")
    input("\n\nPress the enter key to exit.")


