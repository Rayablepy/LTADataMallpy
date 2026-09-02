from helpers import build_headers, build_url, make_request

class Roads:
    def __init__(self,api_key:str,accept:str|None=None)->None:
        self.headers=build_headers(api_key,accept)
    def get_est_travel_times(self)->dict:
        url = build_url("EstTravelTimes")
        return make_request(self.headers,url)
    def get_carpark_availability(self)->dict:
        url=build_url("CarParkAvailabilityv2")
        return make_request(self.headers,url)
