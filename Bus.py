
from main import build_headers, DataMall, build_url, make_request
import os

class Bus(DataMall):
    def __init__(self,api_key:str,accept:str|None=None) -> None:
        super().__init__(api_key,accept)
        self.headers=build_headers(api_key,accept)
        self.arrival=BusArrival(self.headers)
        self.services=BusServices(self.headers)
        self.routes=BusRoutes(self.headers)
        self.stops=BusStops(self.headers)

class BusArrival:
    def __init__(self,headers:dict[str,str]) -> None:
        self.headers=headers
        self.url=build_url("v3/BusArrival")
    def get_bus_arrival(self,stopcode:str,serviceno:str|None=None) -> dict:
        params={
            "BusStopCode":stopcode
        }
        if serviceno:
            params["ServiceNo"]=serviceno
        return make_request(self.headers,self.url,params)

class BusServices:
    def __init__(self,headers:dict[str,str]) -> None:
        self.headers=headers
        self.url=build_url("BusServices")
    def get_bus_services(self,serviceno:str|None=None) -> dict:
        params=None
        if serviceno:
            params={"ServiceNo":serviceno}
        return make_request(self.headers,self.url,params)

class BusRoutes:
    def __init__(self,headers:dict[str,str]) -> None:
        self.headers=headers
        self.url=build_url("BusRoutes")
    def get_bus_routes(self) -> dict:
        return make_request(self.headers,self.url)

class BusStops:
    def __init__(self,headers:dict[str,str]) -> None:
        self.headers=headers
        self.url=build_url("BusStops")
    def get_bus_stops(self,stopcode:str|None=None) -> dict:
        params=None
        if stopcode:
            params={
                "BusStopCode":stopcode
            }
        return make_request(self.headers,self.url,params)
    def get_pvolume_bus_stop(self,date:str|None=None) -> dict:
        url=build_url("PV/Bus")
        params=None
        if date:
            params={"Date":date}
        return make_request(self.headers,url,params)
    def get_pvolume_od_bus_stop(self,date:str|None=None)->dict:
        url=build_url("PV/ODBus")
        params=None
        if date:
            params={"Date":date}
        return make_request(self.headers,url,params)
