from dotenv import load_dotenv
load_dotenv()
from main import base_url
import httpx
import os
key=os.getenv("LTADATAMALL_API_KEY")
class Bus:
    def __init__(self,api_key:str):
        self.api_key=api_key
        self.arrival=BusArrival(api_key)
        self.services=BusServices(api_key)
        self.routes=BusRoutes(api_key)

class BusArrival:
    def __init__(self,api_key:str):
        self.url=base_url+"v3/BusArrival"
        self.headers={"AccountKey":api_key}
    def get_bus_arrival(self,stopcode:str,serviceno=None):
        params={
            "BusStopCode":stopcode
        }
        if serviceno:
            params["ServiceNo"]=serviceno
        r=httpx.get(self.url,headers=self.headers,params=params).json()
        return r

class BusServices:
    def __init__(self,api_key:str):
        self.url=base_url+"BusServices"
        self.headers={"AccountKey":api_key}
    def get_bus_services(self,serviceno=None):
        if serviceno:
            params={
                "ServiceNo":serviceno
            }
            r=httpx.get(self.url,headers=self.headers,params=params).json()
            return r
        else:
            r=httpx.get(self.url,headers=self.headers).json()
            return r

class BusRoutes:
    def __init__(self,api_key:str):
        self.url=base_url+"BusRoutes"
        self.headers={"AccountKey":api_key}
    def get_bus_routes(self):
        return httpx.get(self.url,headers=self.headers)
bus=Bus(api_key=key)

print(bus.routes.get_bus_routes())
