from ActiveMobility import ActiveMobility
from Bus import Bus
from Infra import Infra
from Roads import Roads
from Taxi import Taxi
from Train import Train
from helpers import build_headers

class DataMall:
    def __init__(self,api_key:str,accept:str|None=None) -> None:
        if not api_key:
            raise ValueError("API key is missing. Set an API key for the LTA Data Mall API.")
        self.api_key=api_key
        self.headers=build_headers(api_key,accept)
        self.transport=Transport(api_key,accept)
        self.traffic=Traffic(api_key,accept)
class Transport:
    def __init__(self, api_key:str,accept:str|None=None) -> None:
        if not api_key:
            raise ValueError("API key is missing. Set an API key for the LTA Data Mall API.")
        self.api_key=api_key
        self.headers=build_headers(api_key,accept)

        self.bus=Bus(api_key,accept)
        self.train=Train(api_key,accept)
        self.taxi=Taxi(api_key,accept)
        self.active_mobility=ActiveMobility(api_key,accept)

class Traffic:
    def __init__(self, api_key:str,accept:str|None=None) -> None:
        if not api_key:
            raise ValueError("API key is missing. Set an API key for the LTA Data Mall API.")
        self.api_key=api_key
        self.headers=build_headers(api_key,accept)

        self.roads=Roads(api_key,accept)
        self.infra=Infra(api_key,accept)
