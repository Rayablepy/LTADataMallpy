import os
import time
import pytest

from dotenv import load_dotenv

from LTADataMallpy import DataMall
from LTADataMallpy.helpers import build_url, close_client
from LTADataMallpy.models import (
    FacilityMaintenance,
    GtfsScheduleDownload,
    LtaResult,
    PassengerVolumeDownload,
    PlatformCrowdDensityForecast,
    PlatformCrowdDensityRealTime,
    TrainServiceAlertsResponse,
)

load_dotenv()

API_KEY = os.getenv("LTADATAMALL_API_KEY")
DELAY_SECONDS = 3.0
TRAIN_LINE = "NEL"

client = DataMall(api_key=API_KEY) if API_KEY else None


def sleep() -> None:
    time.sleep(DELAY_SECONDS)


def require_client() -> None:
    if client is not None:
        return
    msg = "LTADATAMALL_API_KEY is not set"
    pytest.skip(msg)


def report_endpoint(name: str, url: str, detail: str = "") -> None:
    print(f"\nTrain Test: {name}")
    print(f"    endpoint : GET {url} {detail}")
    print("...", flush=True)


def test_train_passenger_volume() -> None:
    sleep()
    require_client()
    report_endpoint("Passenger Volume by Train Station", build_url("PV/Train"), "(Date=)")

    result = client.transport.train.station.get_pvolume_train_station()
    assert isinstance(result, LtaResult[PassengerVolumeDownload])
    assert result.value, "no passenger volume downloads returned"
    assert result.value[0].file_url
    first = result.value[0]
    print(f"    PASS     -> {len(result.value)} download(s); "
          f"FileUrl={first.file_url[:60]}...")


def test_train_od_passenger_volume() -> None:
    sleep()
    require_client()
    report_endpoint(
        "Passenger Volume by Origin-Destination Train Station",
        build_url("PV/ODTrain"),
        "(Date=)",
    )

    result = client.transport.train.station.get_pvolume_train_station(origin_destination=True)
    assert isinstance(result, LtaResult[PassengerVolumeDownload])
    assert result.value, "no passenger volume downloads returned"
    assert result.value[0].file_url
    first = result.value[0]
    print(f"    PASS     -> {len(result.value)} download(s); "
          f"FileUrl={first.file_url[:60]}...")


def test_facilities_maintenance() -> None:
    sleep()
    require_client()
    report_endpoint("Lift Maintenance", build_url("v2/FacilitiesMaintenance"))

    result = client.transport.train.station.get_maintenance()
    assert isinstance(result, LtaResult[FacilityMaintenance])
    assert result.value, "no maintenance records returned"
    first = result.value[0]
    print(f"    PASS     -> {len(result.value)} records; "
          f"first: StationName={first.station_name}, LiftID={first.lift_id}")


def test_train_service_alerts() -> None:
    sleep()
    require_client()
    report_endpoint("Train Service Alerts", build_url("TrainServiceAlerts"))

    result = client.transport.train.service.get_train_service_alerts()
    assert isinstance(result, TrainServiceAlertsResponse)
    assert result.value.status in (1, 2)
    status = {1: "NORMAL", 2: "DISRUPTED"}[result.value.status]
    print(f"    PASS     -> Status={status}; AffectedSegments="
          f"{len(result.value.affected_segments)}, Messages={len(result.value.message)}")


def test_crowd_density() -> None:
    sleep()
    require_client()
    report_endpoint(
        "Station Crowd Density (real-time)",
        build_url("PCDRealTime"),
        f"(TrainLine={TRAIN_LINE})",
    )

    result = client.transport.train.service.get_crowd_density(TRAIN_LINE)
    assert isinstance(result, LtaResult[PlatformCrowdDensityRealTime])
    assert result.value, "no crowd density records returned"
    first = result.value[0]
    print(f"    PASS     -> {len(result.value)} stations; "
          f"first: Station={first.station}, CrowdLevel={first.crowd_level}")


def test_crowd_density_forecast() -> None:
    sleep()
    require_client()
    report_endpoint(
        "Station Crowd Density (forecast)",
        build_url("PCDForecast"),
        f"(TrainLine={TRAIN_LINE})",
    )

    result = client.transport.train.service.get_crowd_density_forecast(TRAIN_LINE)
    assert isinstance(result, LtaResult[PlatformCrowdDensityForecast])
    assert result.value, "no crowd density forecast returned"
    first = result.value[0]
    first_station = first.stations[0]
    print(f"    PASS     -> ForecastDate={first.date}; "
          f"Stations={len(first.stations)}, "
          f"first: Station={first_station.station}, "
          f"Intervals={len(first_station.interval)}")


def test_gtfs_train_schedule() -> None:
    sleep()
    require_client()
    report_endpoint("GTFS Train Schedule", build_url("GTFSScheduleTrain"))

    result = client.transport.train.service.get_gtfs_train_schedule()
    assert isinstance(result, LtaResult[GtfsScheduleDownload])
    assert result.value, "no GTFS schedule downloads returned"
    assert result.value[0].file_url and result.value[0].timestamp
    first = result.value[0]
    print(f"    PASS     -> {len(result.value)} download(s); "
          f"Timestamp={first.timestamp}, FileUrl={first.file_url[:60]}...")


def test_gtfs_train_service_real_time() -> None:
    sleep()
    require_client()
    report_endpoint("GTFS Real-Time Train Service Alerts", build_url("GTFSRealTimeTrainServiceAlerts"))

    result = client.transport.train.service.get_gtfs_train_service_real_time()
    assert isinstance(result, LtaResult[GtfsScheduleDownload])
    assert result.value, "no GTFS real-time alert downloads returned"
    assert result.value[0].file_url and result.value[0].timestamp
    first = result.value[0]
    print(f"    PASS     -> {len(result.value)} download(s); "
          f"Timestamp={first.timestamp}, FileUrl={first.file_url[:60]}...")


def test_gtfs_train_trip_update() -> None:
    sleep()
    require_client()
    report_endpoint("GTFS Real-Time Train Trip Updates", build_url("GTFSRealtimeTrainTripUpdates"))

    result = client.transport.train.service.get_gtfs_train_trip_update()
    assert isinstance(result, LtaResult[GtfsScheduleDownload])
    assert result.value, "no GTFS trip update downloads returned"
    assert result.value[0].file_url and result.value[0].timestamp
    first = result.value[0]
    print(f"    PASS     -> {len(result.value)} download(s); "
          f"Timestamp={first.timestamp}, FileUrl={first.file_url[:60]}...")


def run_direct() -> None:
    tests = [
        test_train_passenger_volume,
        test_train_od_passenger_volume,
        test_facilities_maintenance,
        test_train_service_alerts,
        test_crowd_density,
        test_crowd_density_forecast,
        test_gtfs_train_schedule,
        test_gtfs_train_service_real_time,
        test_gtfs_train_trip_update,
    ]
    failures = 0
    for test in tests:
        try:
            test()
        except Exception as exc:
            failures += 1
            print(f"    FAIL     -> {type(exc).__name__}: {exc}")
    close_client()
    print(f"\nTrain Tests Complete: {len(tests) - failures}/{len(tests)} passed")
    raise SystemExit(1 if failures else 0)


if __name__ == "__main__":
    run_direct()