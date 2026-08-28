from helpers import build_headers, build_url, make_request

class Taxi:
    def __init__(self,api_key:str,accept:str|None=None)->None:
        self.headers=build_headers(api_key,accept)
    def get_taxi_availability(self)->dict:
        self.url=build_url("Taxi-Availability")
        return make_request(self.headers,self.url)
