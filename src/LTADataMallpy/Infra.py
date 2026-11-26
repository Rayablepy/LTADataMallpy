import httpx

from .helpers import build_headers, build_url, make_request, make_paginated_request
from .models import (
    EvBatchDownload,
    EvChargingResponse,
    FaultyTrafficLight,
    LtaResult,
    TrafficCamera,
    VmsMessage,
)


class Infra:
    def __init__(self,api_key:str,accept:str|None,client:httpx.Client)->None:
        self.headers=build_headers(api_key,accept)
        self.client=client
    def get_faulty_lights(self)->LtaResult[FaultyTrafficLight]:
        url=build_url("FaultyTrafficLights")
        return LtaResult[FaultyTrafficLight].model_validate(make_request(self.client,self.headers,url))
    def get_traffic_images(self)->LtaResult[TrafficCamera]:
        url=build_url("Traffic-Imagesv2")
        return LtaResult[TrafficCamera].model_validate(make_paginated_request(self.client,self.headers,url))
    def get_vms_emas(self)->LtaResult[VmsMessage]:
        url=build_url("VMS")
        return LtaResult[VmsMessage].model_validate(make_request(self.client,self.headers,url))
    def get_ev_charge_points(self,postalcode:str)->EvChargingResponse:
        url=build_url("EVChargingPoints")
        params={"PostalCode":postalcode}
        return EvChargingResponse.model_validate(make_request(self.client,self.headers,url,params))
    def get_ev_charge_points_batch(self)->LtaResult[EvBatchDownload]:
        url=build_url("EVCBatch")
        return LtaResult[EvBatchDownload].model_validate(make_request(self.client,self.headers,url))
