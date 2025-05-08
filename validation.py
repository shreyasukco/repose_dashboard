import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

class LocationValidator:

    def __init__(self, df):
        self.df = df
        self.geolocator = Nominatim(user_agent="geoapi", timeout=10)

    def is_valid_lat_lon(self, lat, lon):

        try:
            lat = float(lat)
            lon = float(lon)
            return -90 <= lat <= 90 and -180 <= lon <= 180
        except (ValueError, TypeError):
            return False
        
    # def get_location_details(self, lat, lon):

    #     try:
    #         location = self.geolocator.reverse((float(lat), float(lon)), exactly_one=True)
    #         if location and 'address' in location.raw:
    #             addr = location.raw['address']
    #             country = addr.get('country')
    #             state = addr.get('state')
    #             city = addr.get('city') or addr.get('town') or addr.get('village')
    #             pincode = addr.get('postcode')
    #             print(f"Latitude: {lat}, Longitude: {lon} => Country: {country}, State: {state}, City: {city}, Pincode: {pincode}")
    #             return country, state, city, pincode
    #     except (GeocoderTimedOut, ValueError):
    #         pass
    #     return None, None, None, None
    # def get_location_details(self, lat, lon):
        # try:
        #     location = self.geolocator.reverse((float(lat), float(lon)), exactly_one=True)
        #     if location and 'address' in location.raw:
        #         addr = location.raw['address']
        #         country = addr.get('country')
        #         state = addr.get('state')
        #         city = addr.get('city') or addr.get('town') or addr.get('village')
        #         district = addr.get('county') or addr.get('state_district') or addr.get('district')
        #         pincode = addr.get('postcode')
        #         print(f"Latitude: {lat}, Longitude: {lon} => Country: {country}, State: {state}, District: {district}, City: {city}, Pincode: {pincode}")
        #         return country, state, district, city, pincode
        # except (GeocoderTimedOut, ValueError):
        #     pass
        # return None, None, None, None, None
    
    def add_location_validation(self):
        self.df['location_validation'] = self.df.apply(
            lambda row: 'valid' if self.is_valid_lat_lon(row['latitude'], row['longitude']) else 'invalid',
            axis=1)
        # self.df[['country', 'state', 'city', 'pincode']] = self.df.apply(
        #     lambda row: pd.Series(self.get_location_details(row['latitude'], row['longitude']))
        #     if row['location_validation'] == 'valid' else pd.Series([None, None, None, None]),
        #     axis=1
        # )
        return self.df

