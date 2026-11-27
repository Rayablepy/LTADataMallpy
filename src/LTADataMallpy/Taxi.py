import httpx

from .helpers import build_headers, build_url, make_request, make_paginated_request
from .models import LtaResult, TaxiAvailability, TaxiStand


class Taxi:
    def __init__(self,api_key:str,accept:str|None,client:httpx.Client)->None:
        self.headers=build_headers(api_key,accept)
        self.client=client
    def get_taxi_availability(self)->LtaResult[TaxiAvailability]:
        self.url=build_url("Taxi-Availability")
        return LtaResult[TaxiAvailability].model_validate(make_paginated_request(self.client,self.headers,self.url))
    def get_taxi_stands(self)->LtaResult[TaxiStand]:
        self.url=build_url("TaxiStands")
        return LtaResult[TaxiStand].model_validate(make_request(self.client,self.headers,self.url))
