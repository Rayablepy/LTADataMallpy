import httpx

base_url="https://datamall2.mytransport.sg/ltaodataservice/"

def build_headers(api_key:str,accept:str|None=None) -> dict[str,str]:
    headers:dict[str,str]={"AccountKey":api_key}
    if accept:
        headers["accept"]=accept
    return headers

def build_url(endpoint:str) -> str:
    return base_url+endpoint

client = None
def create_client() -> httpx.Client:
    global client
    if client is None:
        client = httpx.Client(timeout=30.0)
    return client

#may be open to exports
def close_client() -> None:
    global client
    if client is not None:
        client.close()
        client = None

#Custom exceptions, open to updates
class DataMallError(Exception):
    """Base class for LTA DataMall API errors"""

    def __init__(self, status_code: int, detail: str) -> None:
        self.status_code = status_code
        self.detail = detail
        super().__init__(f"{status_code} {detail}")


class DataMallPermissionError(DataMallError):
    """Raised when a data mall API key is invalid or lacks access to the api"""
    pass
class DataMallNotFoundError(DataMallError):
    """Raised when the requested data is not available for this account"""
    pass
class DataMallBackendError(DataMallError):
    """Raised when the LTA backend servers encounter error(s) in processing requests"""
    pass
class DataMallRateLimitError(DataMallError):
    """Raised when the API rate limit is exceeded"""
    pass


def extract_error_detail(response) -> str:
    try:
        body = response.json()
    except Exception:
        return response.reason_phrase or "Unknown error"
    error = body.get("error")
    if isinstance(error, dict):
        message = error.get("message")
        if message:
            return str(message)
    value = body.get("value")
    if isinstance(value, dict) and isinstance(value.get("status"), dict):
        message = value["status"].get("message")
        if message:
            return str(message)
    return response.reason_phrase or "Unknown error"

def make_request(headers,url,params=None):
    r=create_client().get(url,headers=headers,params=params)
    if r.status_code in (401,403):
        raise DataMallPermissionError(r.status_code, extract_error_detail(r))
    elif r.status_code in (404,):
        raise DataMallNotFoundError(r.status_code, extract_error_detail(r))
    elif r.status_code in (500,502,503):
        raise DataMallBackendError(r.status_code, extract_error_detail(r))
    elif r.status_code==429:
        raise DataMallRateLimitError(r.status_code, extract_error_detail(r))
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
