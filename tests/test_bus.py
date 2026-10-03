
import os
import time
import pytest

from dotenv import load_dotenv

from LTADataMallpy import DataMall
from LTADataMallpy.helpers import build_url, close_client
from LTADataMallpy.models import (
    BusArrivalResponse,
    BusRoute,
    BusService,
    BusStop,
    LtaResult,
    PassengerVolumeDownload,
    PlannedBusRoute,
)

load_dotenv()

API_KEY = os.getenv("LTADATAMALL_API_KEY")
DELAY_SECONDS = 3.0
BUS_STOP_CODE = "83139"

client = DataMall(api_key=API_KEY) if API_KEY else None


def sleep() -> None:
    time.sleep(DELAY_SECONDS)


def require_client() -> None:
    if client is not None:
        return
    msg = "LTADATAMALL_API_KEY is not set"
    pytest.skip(msg)


def report_endpoint(name: str, url: str, detail: str = "") -> None:
    print(f"\nBus Test: {name}")
    print(f"    endpoint : GET {url} {detail}")
    print("...", flush=True)


def test_bus_arrival() -> None:
    sleep()
    require_client()
    report_endpoint(
        "Bus Arrival (real-time)",
        build_url("v3/BusArrival"),
        f"(BusStopCode={BUS_STOP_CODE})",
    )
    result = client.transport.bus.arrival.get_bus_arrival(stopcode=BUS_STOP_CODE)
    assert isinstance(result, BusArrivalResponse)
    assert result.bus_stop_code == BUS_STOP_CODE
    assert result.services, "no services returned for bus stop"
    first = result.services[0]
    print(f"    PASS     -> {len(result.services)} services; "
          f"first: ServiceNo={first.service_no}, Operator={first.operator}")


def test_bus_services() -> None:
    sleep()
    require_client()
    report_endpoint("Bus Services", build_url("BusServices"), f"(ServiceNo=)")

    result = client.transport.bus.services.get_bus_services(serviceno=None)
    assert isinstance(result, LtaResult[BusService])
    assert result.value, "no bus services returned"
    first = result.value[0]
    print(f"    PASS     -> {len(result.value)} services; "
          f"first: ServiceNo={first.service_no}, Operator={first.operator}")


def test_bus_filtered_services() -> None:
    sleep()
    require_client()
    report_endpoint("Bus Services (filtered)", build_url("BusServices"), "(ServiceNo=107M)")
    result = client.transport.bus.services.get_bus_services(serviceno="107M")
    assert isinstance(result, LtaResult[BusService])
    assert result.value, "no services returned for ServiceNo=107M"
    assert all(s.service_no == "107M" for s in result.value)
    print(f"    PASS     -> {len(result.value)} services for ServiceNo=107M")


def test_bus_routes() -> None:
    sleep()
    require_client()
    report_endpoint("Bus Routes", build_url("BusRoutes"))

    result = client.transport.bus.routes.get_bus_routes()
    assert isinstance(result, LtaResult[BusRoute])
    assert result.value, "no bus routes returned"
    first = result.value[0]
    print(f"    PASS     -> {len(result.value)} route records; "
          f"first: ServiceNo={first.service_no}, StopSequence={first.stop_sequence}")


def test_planned_bus_routes() -> None:
    sleep()
    require_client()
    report_endpoint("Planned Bus Routes", build_url("PlannedBusRoutes"))

    result = client.transport.bus.routes.get_planned_routes()
    assert isinstance(result, LtaResult[PlannedBusRoute])
    if not result.value:
        print("    PASS     -> 0 downloads (static dataset not currently published; OK)")
        return
    assert result.value[0].file_url
    first = result.value[0]
    print(f"    PASS     -> {len(result.value)} download(s); "
          f"first: RevisionNumber={first.revision_number}, FileUrl={first.file_url[:60]}...")


def test_bus_stops() -> None:
    sleep()
    require_client()
    report_endpoint("Bus Stops", build_url("BusStops"), f"(BusStopCode={BUS_STOP_CODE})")

    result = client.transport.bus.stops.get_bus_stops(stopcode=BUS_STOP_CODE)
    assert isinstance(result, LtaResult[BusStop])
    assert result.value, "no bus stops returned"
    first = result.value[0]
    assert first.bus_stop_code == BUS_STOP_CODE
    print(f"    PASS     -> {len(result.value)} stop(s); "
          f"first: RoadName={first.road_name}, Description={first.description}")


def test_bus_passenger_volume() -> None:
    sleep()
    require_client()
    report_endpoint("Passenger Volume by Bus Stop", build_url("PV/Bus"), "(Date=)")

    result = client.transport.bus.stops.get_pvolume_bus_stop()
    assert isinstance(result, LtaResult[PassengerVolumeDownload])
    assert result.value, "no passenger volume downloads returned"
    assert result.value[0].file_url
    first = result.value[0]
    print(f"Pass -> {len(result.value)} download(s) | FileUrl={first.file_url[:60]}...")


def run_direct() -> None:
    tests = [
        test_bus_arrival,
        test_bus_services,
        test_bus_filtered_services,
        test_bus_routes,
        test_planned_bus_routes,
        test_bus_stops,
        test_bus_passenger_volume,
    ]
    failures = 0
    for test in tests:
        try:
            test()
        except Exception as exc:
            failures += 1
            print(f"    FAIL     -> {type(exc).__name__}: {exc}")
    close_client()
    print(f"\nBus Tests Complete: {len(tests) - failures}/{len(tests)} passed")
    raise SystemExit(1 if failures else 0)


if __name__ == "__main__":
    run_direct()
