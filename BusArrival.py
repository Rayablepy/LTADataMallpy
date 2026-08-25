from dotenv import load_dotenv
load_dotenv()
from main import base_url
import httpx
import os
base_url="https://datamall2.mytransport.sg/ltaodataservice/"
key=os.getenv("LTADATAMALL_API_KEY")
class Bus:
    def __init__(self,api_key:str,url=None):
        self.url=url
        self.api_key=api_key
        self.headers={"AccountKey":api_key}

class BusArrival(Bus):
    def __init__(self,api_key:str):
        super().__init__(api_key=api_key)
        self.url=base_url+"v3/BusArrival"
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
main=BusArrival(api_key=key)

print(main.get_bus_arrival("83139"))
