from helpers import build_headers, build_url, make_request

class Train:
    def __init__(self,api_key:str,accept:str|None=None)->None:
        self.headers=build_headers(api_key,accept)
        self.station=TrainStation(self.headers)

class TrainStation:
    def __init__(self,headers:dict[str,str]) -> None:
        self.headers=headers
        self.url=build_url("")
    def get_pvolume_od_train_station(self,date:str|None=None)->dict:
        url=build_url("PV/ODTrain")
        params=None
        if date:
            params={"Date":date}
        return make_request(self.headers,url,params)
    def get_pvolume_train_station(self,date:str|None=None)->dict:
        url=build_url("PV/Train")
        params=None
        if date:
            params={"Date":date}
        return make_request(self.headers,url,params)
