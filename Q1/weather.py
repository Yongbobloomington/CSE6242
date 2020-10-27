import http.client
import json
import csv

class  WHEATHERUtils:

    # ctor
    def __init__(self, api_key:str):
        self.api_key = api_key

    # takes latitude and longitude, returns wheather forecast
    def get_wheather_forecast_for_geocode(self, latitude:float, longitude:float)->list:
        
        # host
        host = 'api.weather.com'
        # con
        connection = http.client.HTTPSConnection(host)
        # path
        part1 = "/v3/wx/forecast/daily/7day?format=json&apiKey="
        part2 = "&geocode="
        part3 = "&language=en-US&units=m"
        key = self.api_key
        path = part1 + key + part2 + str(longitude) + "," + str(latitude) + part3
        # http get
        connection.request("GET", path)
        # http response
        response = connection.getresponse()
        # raw data
        wheather_forecast_raw = response.read().decode('utf-8')
        # json
        wheather_forecast_json = json.loads(wheather_forecast_raw)
        
        # clean data
        dayOfWeek = wheather_forecast_json['dayOfWeek']
        temperatureMin = wheather_forecast_json['temperatureMin']
        temperatureMax = wheather_forecast_json['temperatureMax']
        narrative = wheather_forecast_json['narrative']
        daypart = wheather_forecast_json['daypart']
        daypart0 = daypart[0]
        dayOrNight = daypart0['dayOrNight']
        daypartName = daypart0['daypartName']
        daypartNarrative = daypart0['narrative']
        precipChance = daypart0['precipChance']
        precipType = daypart0['precipType']
        qpfSnow = daypart0['qpfSnow']
        snowRange = daypart0['snowRange']
        relativeHumidity = daypart0['relativeHumidity']
        temperatureHeatIndex = daypart0['temperatureHeatIndex']
        thunderCategory = daypart0['thunderCategory']
        uvIndex = daypart0['uvIndex']

        # build wheather_forecast for geocode X,Y
        wheather_forecast = []
        
        dictionary = {'dayOfWeek': dayOfWeek, 'temperatureMin': temperatureMin,
        'temperatureMax': temperatureMax, 'narrative': narrative, 'dayOrNight': dayOrNight, 
        'daypartName': daypartName, 'daypartNarrative': daypartNarrative, 'precipType': precipType,
        'precipChance': precipChance, 'qpfSnow': qpfSnow, 'snowRange': snowRange, 'relativeHumidity': relativeHumidity,
        'temperatureHeatIndex': temperatureHeatIndex, 'thunderCategory': thunderCategory, 'uvIndex': uvIndex}
            
        wheather_forecast.append(dictionary)

        return wheather_forecast


class  GEOCODERUtils:

    # ctor
    def __init__(self):
        self.loc = ""

    # takes location - full address or Zip code, returns latitude and longitude
    def get_geocode_for_location(self, location:str)->list:

       # host
        host = 'geocoding.geo.census.gov'
        # con
        connection = http.client.HTTPSConnection(host)
        # path
        part1 = "/geocoder/locations/address?"
        street = "4600+Silver+Hill+Rd"
        city = "Suitland+Hill+Rd"
        state = "MD"
        zipcode = "20746"
        part2 = "street=" + street + "&city=" + city + "&state=" + state + "&zip=" + zipcode
        part3 = "&benchmark=Public_AR_Census2010&format=json"
        path = "/geocoder/locations/address?street=4600+Silver+Hill+Rd&city=Suitland&state=MD&zip=20746&benchmark=Public_AR_Census2010&format=json"
        # http get
        connection.request("GET", path)
        # http response
        response = connection.getresponse()
        # raw data
        geocode_raw = response.read().decode('utf-8')
        # json
        geocode_json = json.loads(geocode_raw)
        
        # clean data
        #geocode = []
        # geocode
        result = geocode_json["result"]
        address = result["addressMatches"]
        address = address[0]
        coordinates = address["coordinates"]
        # lat,long
        geocode = {"latitude": coordinates["x"], "longitude": coordinates["y"]}
        # append
        #geocode.append(lat_lng) 
        # return
        return geocode


class EVENT:

    # ctor
    def __init__(self):
        self.location = ""
        self.description = ""
        self.type = ""


def return_event_location(event:EVENT )->str:

    location = event.Location
    return location


if __name__ == "__main__":

    # list
    events_list = []

    # create 100 fictive events with their location
    i = 1
    while i < 5:
        new_event = EVENT()
        new_event.location = "805 E Jefferson St, Rockville, MD 20852"
        events_list.append(new_event)
        i += 1 
   
    all_Wheather_Results = []

    # loop through events
    for event in events_list:
        # new GEOCODERUtils
        geocoder_utils = GEOCODERUtils()
        # geocode
        geocode = geocoder_utils.get_geocode_for_location(event.location)
        # latitude and longitude
        X = geocode["latitude"]
        Y = geocode["longitude"]

        # new WHEATHERUtils
        wheather_utils = WHEATHERUtils(api_key='8bb0f88d18b74604b0f88d18b74604bb')
        # get wheather forecast
        wheather_forecast = wheather_utils.get_wheather_forecast_for_geocode(X, Y)
        
        all_Wheather_Results.append(wheather_forecast)

    #display wheather for all 100 events
    for item in all_Wheather_Results: 
        print ("******************************************************************************************")
        print ("******************************************************************************************")
        weather = item[0]
        for w in weather:
            print(w, weather[w])
            print('\n')

