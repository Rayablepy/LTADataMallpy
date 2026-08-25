from dotenv import load_dotenv
load_dotenv()
from main import base_url
import httpx
import os

key=os.getenv("LTADATAMALL_API_KEY")
class Bus:
    def __init__(self,url=None,api_key:str):
        self.url=url
        self.api_key=api_key
        self.headers={"AccountKey":api_key}

class BusArrival(Bus):
    def get_bus_arrival(self,stopcode:str,serviceno=None):
        if not serviceno:
            params={
                "BusStopCode":stopcode
            }
            r=httpx.get(self.url, headers=self.headers, params=params).json()
            return r
        else:
            params={
                "BusStopCode":stopcode,
                "ServiceNo":serviceno
            }
            r=httpx.get(self.url,headers=self.headers,params=params).json()
            return r
arrivals = BusArrival(key)

print(arrivals.get_bus_arrival("83139"))
