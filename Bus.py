from dotenv import load_dotenv
load_dotenv()
from main import base_url
import httpx
import os

def make_request(headers,url,params=None):
    r=httpx.get(url,headers=headers,params=params)
    if r.status_code in (404,401,403):
        raise PermissionError("Invalid API key. Check your LTA data mall API key")
    elif r.status_code==500:
        raise RuntimeError("LTA backend server encountered an error when processing request.")
    elif r.status_code==429:
        raise 
    r.raise_for_status()
    return r.json()

class Bus:
    def __init__(self,api_key:str):
        if not api_key:
            raise ValueError("API key is missing. Set an API key for the LTA Data Mall API.")
        self.api_key=api_key
        self.headers={"AccountKey":api_key}
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
        return make_request(self.headers,self.url,params)

class BusServices:
    def __init__(self,api_key:str):
        self.url=base_url+"BusServices"
        self.headers={"AccountKey":api_key}
    def get_bus_services(self,serviceno=None):
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

key=os.getenv("LTADATAMALL_API_KEY")

bus=Bus(api_key=key)

print(bus.routes.get_bus_routes())
