from .helpers import build_headers, build_url, make_request, make_paginated_request


class Infra:
    def __init__(self,api_key:str,accept:str|None=None)->None:
        self.headers=build_headers(api_key,accept)
    def get_faulty_lights(self)->dict:
        url=build_url("FaultyTrafficLights")
        return make_request(self.headers,url)
    def get_traffic_images(self)->dict:
        url=build_url("Traffic-Imagesv2")
        return make_paginated_request(self.headers,url)
    def get_vms_emas(self)->dict:
        url=build_url("VMS")
        return make_request(self.headers,url)
    def get_ev_charge_points(self,postalcode:str)->dict:
        url=build_url("EVChargingPoints")
        params={"PostalCode":postalcode}
        return make_request(self.headers,url,params)
    def get_ev_charge_points_batch(self)->dict:
        url=build_url("EVCBatch")
        return make_request(self.headers,url)