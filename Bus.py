from dotenv import load_dotenv
load_dotenv()
from main import base_url, make_request
import httpx
import os
class Bus:
    def __init__(self,api_key:str):
        if not api_key:
            raise ValueError("API key is missing. Set an API key for the LTA Data Mall API.")
        self.api_key=api_key
        self.headers={"AccountKey":api_key}
        self.arrival=BusArrival(api_key)
        self.services=BusServices(api_key)
        self.routes=BusRoutes(api_key)
        self.stops=BusStops(api_key)

class BaseEndpoint:
    def __init__(self,api_key:str,endpoint:str,accept:str|None=None):
        if accept:
            self.headers={"AccountKey":api_key,
                            "accept":accept}
        else:
            self.headers={
                "AccountKey":api_key,
            }
        self.url=base_url+endpoint

class BusArrival(BaseEndpoint):
    def __init__(self,api_key:str):
        super().__init__(api_key,"v3/BusArrival")
    def get_bus_arrival(self,stopcode:str,serviceno:str | None=None):
        params={
            "BusStopCode":stopcode
        }
        if serviceno:
            params["ServiceNo"]=serviceno
        return make_request(self.headers,self.url,params)

class BusServices:
    def __init__(self,api_key:str):
        self.url=base_url+"BusServices"
        self.headers={"AccountKey":api_key}
    def get_bus_services(self,serviceno:str | None =None):
        params=None
        if serviceno:
            params={"ServiceNo":serviceno}
        return make_request(self.headers,self.url,params)

class BusRoutes:
    def __init__(self,api_key:str):
        self.url=base_url+"BusRoutes"
        self.headers={"AccountKey":api_key}
    def get_bus_routes(self):
        return make_request(self.headers,self.url)

class BusStops:
    def __init__(self,api_key:str):
        self.url=base_url+"BusStops"
        self.headers={"AccountKey":api_key}
    def get_bus_stops(self,stopcode:str | None=None):
        params = None
        if stopcode:
            params={
                "BusStopCode":stopcode
            }
        return make_request(self.headers,self.url,params)
    def get_pvolume_bus_stop(self):


key=os.getenv("LTADATAMALL_API_KEY")

bus=Bus(api_key=key)

print(bus.stops.get_bus_stops("01012"))
