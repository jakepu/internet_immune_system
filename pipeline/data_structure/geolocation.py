from datetime import datetime
from datetime import timedelta
from datetime import timezone

class Geolocation:
    def __init__(self, parsedObj):
        self.dict = parsedObj.data
        self.last_update = parsedObj.timestamp

    def getData(self, ip_address):
        #ip_address needs to be a string
        #data format is a list in the order of [city, country, latitude, longitude]
        return data[ip_address] 

