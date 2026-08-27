import httpx
#base api url
base_url="https://datamall2.mytransport.sg/ltaodataservice/"
#helpers
def build_headers(api_key:str,accept:str|None=None) -> dict[str,str]:
    headers:dict[str,str]={"AccountKey":api_key}
    if accept:
        headers["accept"]=accept
    return headers
def build_url(endpoint:str) -> str:
    return base_url+endpoint
#request logic
def make_request(headers,url,params=None):
    r=httpx.get(url,headers=headers,params=params)
    if r.status_code in (404,401,403):
        raise PermissionError("Invalid API key. Check your LTA data mall API key")
    elif r.status_code==500:
        raise RuntimeError("LTA backend server encountered an error when processing request.")
    elif r.status_code==429:
        raise httpx.HTTPError("Rate limit frequency exceeded, please back off your request frequency")
    r.raise_for_status()
    return r.json()

class DataMall:
    def __init__(self,api_key:str,accept:str|None=None) -> None:
        if not api_key:
            raise ValueError("API key is missing. Set an API key for the LTA Data Mall API.")
        self.api_key=api_key
        self.headers=build_headers(api_key,accept)
