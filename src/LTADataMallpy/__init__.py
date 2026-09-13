from .helpers import build_headers
from .subclasses import Traffic, Transport
from .Geo import Geospatial


class DataMall:
    def __init__(self, api_key: str, accept: str | None = None) -> None:
        if not api_key:
            raise ValueError("API key is missing. Set an API key for the LTA Data Mall API.")
        self.api_key = api_key
        self.headers = build_headers(api_key, accept)
        self.transport = Transport(api_key, accept)
        self.traffic = Traffic(api_key, accept)
        self.geospatial = Geospatial(api_key, accept)