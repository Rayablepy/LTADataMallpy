import os
import time
import pytest

from dotenv import load_dotenv

from LTADataMallpy import DataMall
from LTADataMallpy.helpers import build_url, close_client
from LTADataMallpy.models import (
    CarParkAvailability,
    EstimatedTravelTime,
    LtaResult,
    PubFloodAlert,
    RoadOpening,
    RoadWork,
    TrafficFlowDownload,
    TrafficIncident,
    TrafficSpeedBand,
)

load_dotenv()

API_KEY = os.getenv("LTADATAMALL_API_KEY")
DELAY_SECONDS = 3.0

client = DataMall(api_key=API_KEY) if API_KEY else None


def sleep() -> None:
    time.sleep(DELAY_SECONDS)


def require_client() -> None:
    if client is not None:
        return
    msg = "LTADATAMALL_API_KEY is not set"
    pytest.skip(msg)


def report_endpoint(name: str, url: str, detail: str = "") -> None:
    print(f"\nRoads Test: {name}")
    print(f"    endpoint : GET {url} {detail}")
    print("...", flush=True)


def test_est_travel_times() -> None:
    sleep()
    require_client()
    report_endpoint("Expressway Estimated Travel Times", build_url("EstTravelTimes"))

    result = client.traffic.roads.get_est_travel_times()
    assert isinstance(result, LtaResult[EstimatedTravelTime])
    assert result.value, "no travel times returned"
    first = result.value[0]
    print(f"    PASS     -> {len(result.value)} records; "
          f"first: Name={first.name}, Direction={first.direction}, "
          f"EstTime={first.est_time}min ({first.start_point} -> {first.end_point})")


def test_carpark_availability() -> None:
    sleep()
    require_client()
    report_endpoint("Car Park Availability", build_url("CarParkAvailabilityv2"))

    result = client.traffic.roads.get_carpark_availability()
    assert isinstance(result, LtaResult[CarParkAvailability])
    assert result.value, "no car park availability returned"
    first = result.value[0]
    print(f"    PASS     -> {len(result.value)} car parks; "
          f"first: CarParkID={first.car_park_id}, Development={first.development!r}, "
          f"AvailableLots={first.available_lots}")


def test_road_openings() -> None:
    sleep()
    require_client()
    report_endpoint("Road Openings", build_url("RoadOpenings"))

    result = client.traffic.roads.get_road_openings()
    assert isinstance(result, LtaResult[RoadOpening])
    assert result.value, "no road openings returned"
    first = result.value[0]
    print(f"    PASS     -> {len(result.value)} records; "
          f"first: EventID={first.event_id}, RoadName={first.road_name}")


def test_road_works() -> None:
    sleep()
    require_client()
    report_endpoint("Road Works", build_url("RoadWorks"))

    result = client.traffic.roads.get_road_works()
    assert isinstance(result, LtaResult[RoadWork])
    assert result.value, "no road works returned"
    first = result.value[0]
    print(f"    PASS     -> {len(result.value)} records; "
          f"first: EventID={first.event_id}, RoadName={first.road_name}")


def test_traffic_incidents() -> None:
    sleep()
    require_client()
    report_endpoint("Traffic Incidents", build_url("TrafficIncidents"))

    result = client.traffic.roads.get_traffic_incidents()
    assert isinstance(result, LtaResult[TrafficIncident])
    if not result.value:
        print("    PASS     -> 0 incidents (none currently reported; OK)")
        return
    first = result.value[0]
    print(f"    PASS     -> {len(result.value)} incidents; "
          f"first: Type={first.type}, Message={first.message[:60]!r}")


def test_traffic_speed_bands() -> None:
    sleep()
    require_client()
    report_endpoint("Traffic Speed Bands", build_url("v4/TrafficSpeedBands"))

    result = client.traffic.roads.get_traffic_speed_bands()
    assert isinstance(result, LtaResult[TrafficSpeedBand])
    assert result.value, "no speed bands returned"
    first = result.value[0]
    print(f"    PASS     -> {len(result.value)} records; "
          f"first: LinkID={first.link_id}, RoadName={first.road_name}, "
          f"SpeedBand={first.speed_band}")


def test_traffic_flow() -> None:
    sleep()
    require_client()
    report_endpoint("Traffic Flow Download", build_url("TrafficFlow"))

    result = client.traffic.roads.get_traffic_flows()
    assert isinstance(result, LtaResult[TrafficFlowDownload])
    assert result.value, "no traffic flow downloads returned"
    assert result.value[0].link
    first = result.value[0]
    print(f"    PASS     -> {len(result.value)} download(s); "
          f"FileUrl={first.link[:60]}...")


def test_flood_alerts() -> None:
    sleep()
    require_client()
    report_endpoint("Public Flood Alerts", build_url("PubFloodAlerts"))

    result = client.traffic.roads.get_flood_alerts()
    assert isinstance(result, LtaResult[PubFloodAlert])
    if not result.value:
        print("    PASS     -> 0 alerts (no flood alerts currently active; OK)")
        return
    first = result.value[0]
    print(f"    PASS     -> {len(result.value)} alerts; "
          f"first: Severity={first.severity}, Headline={first.headline[:60]!r}")


def run_direct() -> None:
    tests = [
        test_est_travel_times,
        test_carpark_availability,
        test_road_openings,
        test_road_works,
        test_traffic_incidents,
        test_traffic_speed_bands,
        test_traffic_flow,
        test_flood_alerts,
    ]
    failures = 0
    for test in tests:
        try:
            test()
        except Exception as exc:
            failures += 1
            print(f"    FAIL     -> {type(exc).__name__}: {exc}")
    close_client()
    print(f"\nRoads Tests Complete: {len(tests) - failures}/{len(tests)} passed")
    raise SystemExit(1 if failures else 0)


if __name__ == "__main__":
    run_direct()