import os
import time
import pytest

from dotenv import load_dotenv

from LTADataMallpy import DataMall
from LTADataMallpy.helpers import build_url, close_client
from LTADataMallpy.models import LtaResult, TaxiAvailability, TaxiStand

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
    print(f"\nTaxi Test: {name}")
    print(f"    endpoint : GET {url} {detail}")
    print("...", flush=True)


def test_taxi_availability() -> None:
    sleep()
    require_client()
    report_endpoint("Taxi Availability (real-time)", build_url("Taxi-Availability"))

    result = client.transport.taxi.get_taxi_availability()
    assert isinstance(result, LtaResult[TaxiAvailability])
    assert result.value, "no taxis returned"
    first = result.value[0]
    print(f"    PASS     -> {len(result.value)} taxis; "
          f"first: Latitude={first.latitude}, Longitude={first.longitude}")


def test_taxi_stands() -> None:
    sleep()
    require_client()
    report_endpoint("Taxi Stands", build_url("TaxiStands"))

    result = client.transport.taxi.get_taxi_stands()
    assert isinstance(result, LtaResult[TaxiStand])
    assert result.value, "no taxi stands returned"
    first = result.value[0]
    print(f"    PASS     -> {len(result.value)} stands; "
          f"first: TaxiCode={first.taxi_code}, Name={first.name}")


def run_direct() -> None:
    tests = [
        test_taxi_availability,
        test_taxi_stands,
    ]
    failures = 0
    for test in tests:
        try:
            test()
        except Exception as exc:
            failures += 1
            print(f"    FAIL     -> {type(exc).__name__}: {exc}")
    close_client()
    print(f"\nTaxi Tests Complete: {len(tests) - failures}/{len(tests)} passed")
    raise SystemExit(1 if failures else 0)


if __name__ == "__main__":
    run_direct()