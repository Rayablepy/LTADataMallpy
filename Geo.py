from helpers import build_headers, build_url, make_request

class Geospatial:
    def __init__(self,api_key:str,accept:str|None=None)->None:
        self.headers=build_headers(api_key,accept)
        self.url=build_url("GeospatialWholeIsland")
    def get_geo_layer(self,id:str)->dict:
        params={
            "ID":id
        }

        return make_request(self.headers,self.url,params)
