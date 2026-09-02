from helpers import build_headers, build_url, make_request

class Infra:
    def __init__(self,api_key:str,accept:str|None=None)->None:
        self.headers=build_headers(api_key,accept)
    def get_faulty_lights(self)->dict:
        url=build_url("FaultyTrafficLights")
        return make_request(self.headers,url)