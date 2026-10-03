import os
import time
import pytest

from dotenv import load_dotenv

from LTADataMallpy import DataMall
from LTADataMallpy.helpers import build_url, close_client
from LTADataMallpy.models import (
    EvBatchDownload,
    EvChargingResponse,
    FaultyTrafficLight,
    LtaResult,
    TrafficCamera,
    VmsMessage,
)

load_dotenv()

API_KEY = os.getenv("LTADATAMALL_API_KEY")
DELAY_SECONDS = 3.0
EV_POSTAL_CODE = "018956"

client = DataMall(api_key=API_KEY) if API_KEY else None


def sleep() -> None:
    time.sleep(DELAY_SECONDS)


def require_client() -> None:
    if client is not None:
        return
    msg = "LTADATAMALL_API_KEY is not set"
    pytest.skip(msg)


def report_endpoint(name: str, url: str, detail: str = "") -> None:
    print(f"\nInfra Test: {name}")
    print(f"    endpoint : GET {url} {detail}")
    print("...", flush=True)


def test_faulty_traffic_lights() -> None:
    sleep()
    require_client()
    report_endpoint("Faulty Traffic Lights", build_url("FaultyTrafficLights"))

    result = client.traffic.infra.get_faulty_lights()
    assert isinstance(result, LtaResult[FaultyTrafficLight])
    if not result.value:
        print("    PASS     -> 0 records (no faulty lights currently reported; OK)")
        return
    first = result.value[0]
    print(f"    PASS     -> {len(result.value)} records; "
          f"first: NodeID={first.node_id}, Type={first.type}")


def test_traffic_images() -> None:
    sleep()
    require_client()
    report_endpoint("Traffic Images", build_url("Traffic-Imagesv2"))

    result = client.traffic.infra.get_traffic_images()
    assert isinstance(result, LtaResult[TrafficCamera])
    assert result.value, "no traffic cameras returned"
    first = result.value[0]
    print(f"    PASS     -> {len(result.value)} cameras; "
          f"first: CameraID={first.camera_id}, ImageLink={first.image_link[:50]}...")


def test_vms_messages() -> None:
    sleep()
    require_client()
    report_endpoint("VMS (Electronic Message Alert System)", build_url("VMS"))

    result = client.traffic.infra.get_vms_emas()
    assert isinstance(result, LtaResult[VmsMessage])
    if not result.value:
        print("    PASS     -> 0 messages (no VMS messages currently active; OK)")
        return
    first = result.value[0]
    print(f"    PASS     -> {len(result.value)} messages; "
          f"first: EquipmentID={first.equipment_id}, Message={first.message[:60]!r}")


def test_ev_charging_points() -> None:
    sleep()
    require_client()
    report_endpoint("EV Charging Points", build_url("EVChargingPoints"), f"(PostalCode={EV_POSTAL_CODE})")

    result = client.traffic.infra.get_ev_charge_points(EV_POSTAL_CODE)
    assert isinstance(result, EvChargingResponse)
    assert result.value.ev_locations_data, "no EV charging stations returned"
    first = result.value.ev_locations_data[0]
    first_point = first.charging_points[0]
    print(f"    PASS     -> {len(result.value.ev_locations_data)} station(s); "
          f"first: Name={first.name!r}, Longitude={first.longitude}, "
          f"ChargingPoints={len(first.charging_points)}, "
          f"first PlugType={first_point.plug_types[0].plug_type}")


def test_ev_charging_batch() -> None:
    sleep()
    require_client()
    report_endpoint("EV Charging Points Batch Download", build_url("EVCBatch"))

    result = client.traffic.infra.get_ev_charge_points_batch()
    assert isinstance(result, LtaResult[EvBatchDownload])
    assert result.value, "no EV batch downloads returned"
    assert result.value[0].link
    first = result.value[0]
    print(f"    PASS     -> {len(result.value)} download(s); "
          f"FileUrl={first.link[:60]}...")


def run_direct() -> None:
    tests = [
        test_faulty_traffic_lights,
        test_traffic_images,
        test_vms_messages,
        test_ev_charging_points,
        test_ev_charging_batch,
    ]
    failures = 0
    for test in tests:
        try:
            test()
        except Exception as exc:
            failures += 1
            print(f"    FAIL     -> {type(exc).__name__}: {exc}")
    close_client()
    print(f"\nInfra Tests Complete: {len(tests) - failures}/{len(tests)} passed")
    raise SystemExit(1 if failures else 0)


if __name__ == "__main__":
    run_direct()