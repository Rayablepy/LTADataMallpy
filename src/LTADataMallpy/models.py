from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field

T = TypeVar("T")


def to_pascal(field_name: str) -> str:
    return "".join(word.capitalize() for word in field_name.split("_"))


class DataMallModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_pascal, populate_by_name=True)


class LtaResult(DataMallModel, Generic[T]):
    odata_metadata: str = Field(alias="odata.metadata")
    value: list[T] = Field(alias="value")


class NextBus(DataMallModel):
    origin_code: str
    destination_code: str
    estimated_arrival: str
    monitored: int
    latitude: str
    longitude: str
    visit_number: str
    load: str
    feature: str
    type: str


class BusArrivalService(DataMallModel):
    service_no: str
    operator: str
    next_bus: NextBus
    next_bus_2: NextBus
    next_bus_3: NextBus


class BusArrivalResponse(DataMallModel):
    odata_metadata: str = Field(alias="odata.metadata")
    bus_stop_code: str
    services: list[BusArrivalService]


class BusService(DataMallModel):
    service_no: str
    operator: str
    direction: int
    category: str
    origin_code: str
    destination_code: str
    am_peak_freq: str = Field(alias="AM_Peak_Freq")
    am_offpeak_freq: str = Field(alias="AM_Offpeak_Freq")
    pm_peak_freq: str = Field(alias="PM_Peak_Freq")
    pm_offpeak_freq: str = Field(alias="PM_Offpeak_Freq")
    loop_desc: str


class BusRoute(DataMallModel):
    service_no: str
    operator: str
    direction: int
    stop_sequence: int
    bus_stop_code: str
    distance: float
    wd_first_bus: str = Field(alias="WD_FirstBus")
    wd_last_bus: str = Field(alias="WD_LastBus")
    sat_first_bus: str = Field(alias="SAT_FirstBus")
    sat_last_bus: str = Field(alias="SAT_LastBus")
    sun_first_bus: str = Field(alias="SUN_FirstBus")
    sun_last_bus: str = Field(alias="SUN_LastBus")


class BusStop(DataMallModel):
    bus_stop_code: str
    road_name: str
    description: str
    latitude: float
    longitude: float


class PlannedBusRoute(DataMallModel):
    file_url: str
    revision_number: int


class PassengerVolumeDownload(DataMallModel):
    file_url: str