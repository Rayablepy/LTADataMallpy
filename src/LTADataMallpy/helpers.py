import httpx
import time
base_url="https://datamall2.mytransport.sg/ltaodataservice/"

def build_headers(api_key:str,accept:str|None=None) -> dict[str,str]:
    headers:dict[str,str]={"AccountKey":api_key}
    if accept:
        headers["accept"]=accept
    return headers

def build_url(endpoint:str) -> str:
    return base_url+endpoint

_client = None
def create_client() -> httpx.Client:
    global _client
    if _client is None:
        _client = httpx.Client(timeout=30.0)
    return _client

#may be open to exports
def close_client() -> None:
    global _client
    if _client is not None:
        _client.close()
        _client = None

#Custom exceptions, open to updates
class DataMallPermissionError(Exception):
    """Raised when a data mall API key is invalid"""
    pass
class DataMallBackendError(Exception):
    """Raised when the LTA backend servers encounter error(s) in processing requests"""
    pass
class DataMallRateLimitError(Exception):
    """Raised when the API rate limit is exceeded"""
    pass

def make_request(headers,url,params=None):
    r=create_client().get(url,headers=headers,params=params)
    if r.status_code in (404,401,403):
        raise DataMallPermissionError({
            "error": {
                "code": r.status_code,
                "message": "Invalid API key. Check your LTA data mall API key.",
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            }
        })
    elif r.status_code==500:
        raise DataMallBackendError(  {
            "error": {
                "code": r.status_code,
                "message": "LTA backend server encountered an error when processing request.",
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            }
        })
    elif r.status_code==429:
        raise DataMallRateLimitError({
            "error": {
                "code": r.status_code,
                "message": "Rate limit frequency exceeded, please back off your request frequency",
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            }
        })
    r.raise_for_status()
    return r.json()

def make_paginated_request(headers:dict[str,str],url:str,params:dict[str,str] | None = None) -> dict:
    params = dict(params or {})
    skip = 0
    combined = None
    while True:
        params["$skip"] = skip
        page = make_request(headers, url, params)
        batch = page.get("value", [])
        if combined is None:
            combined = page
        else:
            combined["value"].extend(batch)
        if len(batch) < 500:
            break
        skip += 500
    return combined