import httpx

from .helpers import build_headers, build_url, make_request
from .models import (
    FacilityMaintenance,
    GtfsScheduleDownload,
    LtaResult,
    PassengerVolumeDownload,
    PlatformCrowdDensityForecast,
    PlatformCrowdDensityRealTime,
    TrainServiceAlertsResponse,
)

class Train:
    def __init__(self,api_key:str,accept:str|None,client:httpx.Client)->None:
        self.headers=build_headers(api_key,accept)
        self.client=client
        self.station=TrainStation(self.headers,client)
        self.service=TrainService(self.headers,client)
class TrainStation:
    def __init__(self,headers:dict[str,str],client:httpx.Client) -> None:
        self.headers=headers
        self.client=client
    def get_pvolume_train_station(self,date:str|None=None,origin_destination:bool|None=None)->LtaResult[PassengerVolumeDownload]:
        if origin_destination:
            url = build_url("PV/ODTrain")
        else:
            url=build_url("PV/Train")
        params=None
        if date:
            params={"Date":date}
        return LtaResult[PassengerVolumeDownload].model_validate(make_request(self.client,self.headers,url,params))
    def get_maintenance(self)->LtaResult[FacilityMaintenance]:
        url=build_url("v2/FacilitiesMaintenance")
        return LtaResult[FacilityMaintenance].model_validate(make_request(self.client,self.headers,url))
class TrainService:
    def __init__(self,headers:dict[str,str],client:httpx.Client) -> None:
        self.headers=headers
        self.client=client
    def get_train_service_alerts(self)->TrainServiceAlertsResponse:
        url=build_url("TrainServiceAlerts")
        return TrainServiceAlertsResponse.model_validate(make_request(self.client,self.headers,url))
    def get_crowd_density(self,line:str)->LtaResult[PlatformCrowdDensityRealTime]:
        url=build_url("PCDRealTime")
        params={
            "TrainLine":line
        }
        return LtaResult[PlatformCrowdDensityRealTime].model_validate(make_request(self.client,self.headers,url,params))
    def get_crowd_density_forecast(self,line:str)->LtaResult[PlatformCrowdDensityForecast]:
        url=build_url("PCDForecast")
        params={
            "TrainLine":line
        }
        return LtaResult[PlatformCrowdDensityForecast].model_validate(make_request(self.client,self.headers,url,params))
    def get_gtfs_train_schedule(self)->LtaResult[GtfsScheduleDownload]:
        url=build_url("GTFSScheduleTrain")
        return LtaResult[GtfsScheduleDownload].model_validate(make_request(self.client,self.headers,url))
    def get_gtfs_train_service_real_time(self)->LtaResult[GtfsScheduleDownload]:
        url=build_url("GTFSRealTimeTrainServiceAlerts")
        return LtaResult[GtfsScheduleDownload].model_validate(make_request(self.client,self.headers,url))
    def get_gtfs_train_trip_update(self)->LtaResult[GtfsScheduleDownload]:
        url=build_url("GTFSRealtimeTrainTripUpdates")
        return LtaResult[GtfsScheduleDownload].model_validate(make_request(self.client,self.headers,url))
