# LTADataMallpy

A Python wrapper for the [LTA DataMall](https://www.mytransport.sg/content/mytransport/home/dataMall.html) API, providing typed, easy-to-use access to Singapore's public transport and traffic data: buses, trains, taxis, roads, active mobility, and geospatial layers.

Built on `httpx`, it ships with automatic pagination for endpoints returning more than 500 records, a persistent connection pool, and descriptive custom exceptions.

## Features

- Single entry point: `DataMall` with `transport`, `traffic`, and `geospatial` namespaces
- Automatic pagination (`$skip` handling) for long endpoints
- Persistent `httpx.Client` with a 30s timeout and explicit `close_client()`
- Custom exceptions with response status code, message, and timestamp
- Python `>=3.10` (`X | None` syntax, built-in generics, TypedDict-compatible)

## Installation

### From PyPI 

```bash
pip install singapore-lta-datamall
```

## Getting an API key

1. Register at the [LTA DataMall](https://www.mytransport.sg/content/mytransport/home/dataMall.html) portal.
2. Create an account and request access to an API key.
3. Use the key as the `api_key` argument (or load it from an environment variable / `.env` file).

## Quick start

```python
from LTADataMallpy import DataMall
from dotenv import load_dotenv
import os

load_dotenv()

dm = DataMall(api_key=os.getenv("LTA_API_KEY"))

# Transport data
arrivals = dm.transport.bus.arrival.get_bus_arrival(stopcode="83111")
print(arrivals["Services"])

# Traffic data
speed_bands = dm.traffic.roads.get_traffic_speed_bands()
print(speed_bands["value"])
```

Always close the client when you are done to release the connection pool:

```python
from LTADataMallpy.helpers import close_client
# ... your requests ...
close_client()
```

## API reference

Everything is imported from the top-level package `LTADataMallpy`.

### Main entry point: `DataMall`

```python
from LTADataMallpy import DataMall

dm = DataMall(api_key: str, accept: str | None = None)
```

Raises `ValueError` if `api_key` is empty or missing. Exposes three namespaces:

| Attribute      | Type                        | Description                          |
| -------------- | --------------------------- | ------------------------------------ |
| `dm.transport` | `Transport`                 | Bus, train, taxi, active mobility    |
| `dm.traffic`   | `Traffic`                   | Roads and infrastructure             |
| `dm.geospatial`| `Geospatial`                | Geospatial whole-island layers       |

### `Transport`

```python
from LTADataMallpy import DataMall
dm = DataMall(API_KEY)
t = dm.transport
```

| Attribute            | Class                 | Description            |
| -------------------- | --------------------- | ---------------------- |
| `t.bus`              | `Bus`                 | Bus services/routes    |
| `t.train`            | `Train`               | Train stations/services|
| `t.taxi`             | `Taxi`                | Taxi availability      |
| `t.active_mobility`  | `ActiveMobility`      | Bicycle parking        |

### `Traffic`

```python
dm = DataMall(API_KEY)
tr = dm.traffic
```

| Attribute   | Class    | Description                  |
| ----------- | -------- | ---------------------------- |
| `tr.roads`  | `Roads`  | Road/traffic data            |
| `tr.infra`  | `Infra`  | Infrastructure data          |

### `Geospatial`

```python
dm = DataMall(API_KEY)
G = dm.geospatial
G.get_geo_layer(id="LayerName")
```

LTA DataMall geospatial layers require a `Token` in the request header in addition to `AccountKey`.
Pass the token as the `accept` argument (it is forwarded as the `accept` header value):

```python
dm = DataMall(api_key=API_KEY, accept=YOUR_GEOSPATIAL_TOKEN)
data = dm.geospatial.get_geo_layer(id="factoryarea")
```

### Classes to import directly

Each underlying class is importable on its own, taking `(api_key, accept=None)` unless noted:

```python
from LTADataMallpy.Bus import Bus
from LTADataMallpy.Train import Train
from LTADataMallpy.Taxi import Taxi
from LTADataMallpy.Roads import Roads
from LTADataMallpy.Infra import Infra
from LTADataMallpy.ActiveMobility import ActiveMobility
from LTADataMallpy.Geo import Geospatial
from LTADataMallpy.subclasses import Transport, Traffic
```

## Methods

### Bus

| Class         | Method                                                        | Notes                          |
| ------------- | ------------------------------------------------------------- | ------------------------------ |
| `Bus`         | —                                                             | Aggregates the four sub-objects |
| `Bus.arrival` | `(BusArrival)`                                                |                                |
| `BusArrival`  | `get_bus_arrival(stopcode, serviceno=None)`                   | `BusStopCode` required         |
| `Bus.services`| `(BusServices)`                                               |                                |
| `BusServices` | `get_bus_services(serviceno=None)`                            | Paginated                      |
| `Bus.routes`  | `(BusRoutes)`                                                 |                                |
| `BusRoutes`   | `get_bus_routes()`                                            | Paginated                      |
| `BusRoutes`   | `get_planned_routes()`                                        |                                |
| `Bus.stops`   | `(BusStops)`                                                  |                                |
| `BusStops`    | `get_bus_stops(stopcode=None)`                                | Paginated                      |
| `BusStops`    | `get_pvolume_bus_stop(date=None, origin_destination=None)`    | Bus or OD-Bus volume          |

### Train

| Class            | Method                                                       | Notes                          |
| ---------------- | ------------------------------------------------------------ | ------------------------------ |
| `Train`          | `station`, `service` sub-objects                             |                                |
| `TrainStation`   | `get_pvolume_train_station(date=None, origin_destination=None)` | Train or OD-Train volume     |
| `TrainStation`   | `get_maintenance()`                                          |                                |
| `TrainService`   | `get_train_service_alerts()`                                 |                                |
| `TrainService`   | `get_crowd_density(line)`                                    | `TrainLine` required           |
| `TrainService`   | `get_crowd_density_forecast(line)`                           | `TrainLine` required           |
| `TrainService`   | `get_gtfs_train_schedule()`                                  |                                |
| `TrainService`   | `get_gtfs_train_service_real_time()`                         |                                |
| `TrainService`   | `get_gtfs_train_trip_update()`                               |                                |

### Taxi

| Class  | Method                    | Notes |
| ------ | ------------------------- | ----- |
| `Taxi` | `get_taxi_availability()` | Paginated |
| `Taxi` | `get_taxi_stands()`       |        |

### Roads (traffic)

| Class   | Method                        | Notes       |
| ------- | ----------------------------- | ----------- |
| `Roads` | `get_est_travel_times()`      |             |
| `Roads` | `get_carpark_availability()`  | Paginated   |
| `Roads` | `get_road_openings()`         |             |
| `Roads` | `get_road_works()`            | Paginated   |
| `Roads` | `get_traffic_incidents()`     |             |
| `Roads` | `get_traffic_speed_bands()`   |             |
| `Roads` | `get_traffic_flows()`         |             |
| `Roads` | `get_flood_alerts()`          |             |

### Infra (traffic)

| Class   | Method                                | Notes      |
| ------- | ------------------------------------- | ---------- |
| `Infra` | `get_faulty_lights()`                 |            |
| `Infra` | `get_traffic_images()`                | Paginated  |
| `Infra` | `get_vms_emas()`                      |            |
| `Infra` | `get_ev_charge_points(postalcode)`    | `PostalCode` required |
| `Infra` | `get_ev_charge_points_batch()`        |            |

### ActiveMobility

| Class            | Method                                                  | Notes                       |
| ---------------- | ------------------------------------------------------- | --------------------------- |
| `ActiveMobility` | `get_bicycle_parking(lat, long, dist=None)`             | `Lat`/`Long` required; Paginated |

### Geospatial

| Class         | Method                | Notes                  |
| ------------- | --------------------- | ---------------------- |
| `Geospatial`  | `get_geo_layer(id)`   | `ID` required; needs `accept` token |

## Helpers

Low-level helpers live in `LTADataMallpy.helpers` and can be used for custom endpoint calls:

```python
from LTADataMallpy.helpers import (
    build_headers,        # build the AccountKey/accept header dict from an API key
    build_url,            # join an endpoint to the DataMall base URL
    make_request,         # GET one page; raises custom errors in the helpers module
    make_paginated_request,  # fetch all pages, combining "value" lists
    create_client,        # lazily create/reuse the persistent httpx.Client
    close_client,         # close the persistent client (self-heals on next use)
)
```

Example of a custom call:

```python
from LTADataMallpy.helpers import build_headers, build_url, make_request

headers = build_headers(API_KEY)
url = build_url("SomeEndpoint")
data = make_request(headers, url, params={"SomeParam": "value"})
```

### Persistent client

- The shared `httpx.Client` is created lazily on the first request (with `timeout=30.0`) and reused for every call, keeping TCP/TLS connections alive.
- Call `close_client()` at the end of a script to free resources. It is safe to call mid-run: the next request transparently recreates the client.
- `httpx.Client` is thread-safe, so the client can be shared across threads.

### Pagination

Endpoints marked *Paginated* above go through `make_paginated_request`, which automatically walks `$skip` in 500-record pages and merges every page's `value` list into a single result dict.

## Error handling and debugging

`make_request` maps known HTTP statuses to descriptive exceptions (all in `LTADataMallpy.helpers`, subclasses of `Exception`):

| HTTP status | Exception                  | Meaning                                       |
| ----------- | --------------------------- | --------------------------------------------- |
| 401 / 403 / 404 | `DataMallPermissionError` | Invalid/missing API key               |
| 500         | `DataMallBackendError`      | LTA backend server error                      |
| 429         | `DataMallRateLimitError`    | Rate limit hit; slow your request frequency   |

Each raised exception carries a `dict` describing the failure, e.g. `{"error": {"code": 401, "message": "...", "timestamp": "2026-09-13 12:00:00"}}`. Any other status passes through `httpx.Response.raise_for_status()`.

```python
from LTADataMallpy import DataMall
from LTADataMallpy.helpers import DataMallPermissionError, DataMallRateLimitError

dm = DataMall(api_key="invalid-key")

try:
    dm.transport.bus.arrival.get_bus_arrival("83111")
except DataMallPermissionError as e:
    print("Bad key:", e.args[0])
except DataMallRateLimitError as e:
    print("Slow down:", e.args[0])
```

### Debugging tips

- **429 / rate limit**: LTA enforces per-minute request quotas. Add backoff, or cache responses you fetch repeatedly.
- **Timeout**: the client uses a 30-second timeout; paginated calls to big datasets (e.g. `BusRoutes`, `BusServices`) can be slow on a cold connection.
- **Check connectivity**: confirm the key is active in the DataMall portal and that your network reaches `datamall2.mytransport.sg`.
- **`.env` / secrets**: load your key from an environment variable rather than hard-coding it. The `.env` file is git-ignored.

## Development

```bash
pip install -e .            # editable install from source
uv build                    # build sdist + wheel into dist/
```

No tests are currently shipped (`test/` is empty).

## License

Apache License 2.0. See [LICENSE](LICENSE).

## Links

- Repository: <https://github.com/Rayablepy/LTADataMallpy>
- Issues: <https://github.com/Rayablepy/LTADataMallpy/issues>
- LTA DataMall: <https://www.mytransport.sg/content/mytransport/home/dataMall.html>
