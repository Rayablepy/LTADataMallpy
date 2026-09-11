from helpers import build_headers, build_url, make_request

class ActiveMobility:
    def __init__(self, api_key:str, accept: str| None = None)->None:
        self.headers=build_headers(api_key,accept)
        self.url=build_url("BicycleParkingv2")
    def get_bicycle_parking(self, lat:str, long:str, dist:str|None=None)->dict:
        params={
            "Lat":lat,
            "Long":long,
        }
        if dist:
            params["Dist"]=dist
        return make_request(self.headers,self.url,params)


