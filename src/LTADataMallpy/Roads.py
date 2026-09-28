from .helpers import build_headers, build_url, make_request, make_paginated_request
from .models import (
    CarParkAvailability,
    EstimatedTravelTime,
    LtaResult,
    PubFloodAlert,
    RoadOpening,
    RoadWork,
    TrafficFlowDownload,
    TrafficIncident,
    TrafficSpeedBand,
)


class Roads:
    def __init__(self,api_key:str,accept:str|None=None)->None:
        self.headers=build_headers(api_key,accept)
    def get_est_travel_times(self)->LtaResult[EstimatedTravelTime]:
        url = build_url("EstTravelTimes")
        return LtaResult[EstimatedTravelTime].model_validate(make_request(self.headers,url))
    def get_carpark_availability(self)->LtaResult[CarParkAvailability]:
        url=build_url("CarParkAvailabilityv2")
        return LtaResult[CarParkAvailability].model_validate(make_paginated_request(self.headers,url))
    def get_road_openings(self)->LtaResult[RoadOpening]:
        url=build_url("RoadOpenings")
        return LtaResult[RoadOpening].model_validate(make_request(self.headers,url))
    def get_road_works(self)->LtaResult[RoadWork]:
        url=build_url("RoadWorks")
        return LtaResult[RoadWork].model_validate(make_paginated_request(self.headers,url))
    def get_traffic_incidents(self)->LtaResult[TrafficIncident]:
        url=build_url("TrafficIncidents")
        return LtaResult[TrafficIncident].model_validate(make_request(self.headers,url))
    def get_traffic_speed_bands(self)->LtaResult[TrafficSpeedBand]:
        url=build_url("v4/TrafficSpeedBands")
        return LtaResult[TrafficSpeedBand].model_validate(make_request(self.headers,url))
    def get_traffic_flows(self)->LtaResult[TrafficFlowDownload]:
        url=build_url("TrafficFlow")
        return LtaResult[TrafficFlowDownload].model_validate(make_request(self.headers,url))
    def get_flood_alerts(self)->LtaResult[PubFloodAlert]:
        url=build_url("PubFloodAlerts")
        return LtaResult[PubFloodAlert].model_validate(make_request(self.headers,url))