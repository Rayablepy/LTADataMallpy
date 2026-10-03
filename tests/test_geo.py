import os
import time
import pytest

from dotenv import load_dotenv

from LTADataMallpy import DataMall
from LTADataMallpy.helpers import build_url, close_client
from LTADataMallpy.models import GeospatialLayerDownload, LtaResult

load_dotenv()

API_KEY = os.getenv("LTADATAMALL_API_KEY")
DELAY_SECONDS = 3.0
GEO_LAYER_ID = "ArrowMarking"

client = DataMall(api_key=API_KEY) if API_KEY else None


def sleep() -> None:
    time.sleep(DELAY_SECONDS)


def require_client() -> None:
    if client is not None:
        return
    msg = "LTADATAMALL_API_KEY is not set"
    pytest.skip(msg)


def report_endpoint(name: str, url: str, detail: str = "") -> None:
    print(f"\nGeo Test: {name}")
    print(f"    endpoint : GET {url} {detail}")
    print("...", flush=True)


def test_geo_layer() -> None:
    sleep()
    require_client()
    report_endpoint(
        "Geospatial Whole Island",
        build_url("GeospatialWholeIsland"),
        f"(ID={GEO_LAYER_ID})",
    )

    result = client.geospatial.get_geo_layer(GEO_LAYER_ID)
    assert isinstance(result, LtaResult[GeospatialLayerDownload])
    assert result.value, "no geospatial downloads returned"
    assert result.value[0].link
    first = result.value[0]
    print(f"    PASS     -> {len(result.value)} download(s); "
          f"FileUrl={first.link[:60]}...")


def run_direct() -> None:
    tests = [
        test_geo_layer,
    ]
    failures = 0
    for test in tests:
        try:
            test()
        except Exception as exc:
            failures += 1
            print(f"    FAIL     -> {type(exc).__name__}: {exc}")
    close_client()
    print(f"\nGeo Tests Complete: {len(tests) - failures}/{len(tests)} passed")
    raise SystemExit(1 if failures else 0)


if __name__ == "__main__":
    run_direct()
