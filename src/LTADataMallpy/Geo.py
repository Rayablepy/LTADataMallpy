from .helpers import build_headers, build_url, make_request
from .models import GeospatialLayerDownload, LtaResult

class Geospatial:
    def __init__(self,api_key:str,accept:str|None=None)->None:
        self.headers=build_headers(api_key,accept)
        self.url=build_url("GeospatialWholeIsland")
    def get_geo_layer(self,id:str)->LtaResult[GeospatialLayerDownload]:
        params={
            "ID":id
        }

        return LtaResult[GeospatialLayerDownload].model_validate(make_request(self.headers,self.url,params))