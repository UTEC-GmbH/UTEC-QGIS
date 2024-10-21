"""Constants"""

from dataclasses import dataclass

# TEST_PROJECT_PATH: str = "thermos_output_for_testing/thermos_output_full.qgz"
TEST_PROJECT_PATH: str = "thermos_output_for_testing/thermos_output_mini.qgz"


@dataclass
class ThermosFields:
    """Field names for Thermos results"""

    area_roof: str = "candidate/roof-area"
    area_ground: str = "candidate/ground-area"
    capacity: str = "solution/capacity-kw"
    connected: str = "solution/connected"
    diversity_pipe: str = "solution/diversity"
    demand_cap_cooling: str = "cooling/kwp"
    demand_cap_heat: str = "demand/kwp"
    demand_cons_cooling: str = "cooling/kwh"
    demand_cons_heat: str = "demand/kwh"
    diameter: str = "solution/diameter-mm"
    fid: str = "fid"
    height: str = "candidate/user-fields Height"
    id: str = "id"
    in_solution: str = "solution/included"
    length: str = "path/length"
    point_id_connection: str = "candidate/connections 0"
    point_id_end: str = "path/end"
    point_id_start: str = "path/start"
    type: str = "candidate/user-fields Category"
    supply_capacity: str = "supply/capacity-kwp"


THERMOS_FIELD_NAMES: list[str] = [
    "candidate/connections 0",
    "candidate/connections 1",
    "candidate/connections 2",
    "candidate/connections 3",
    "candidate/connections 4",
    "candidate/connections 5",
    "candidate/ground-area",
    "candidate/id",
    "candidate/inclusion",
    "candidate/modified",
    "candidate/roof-area",
    "candidate/selected",
    "candidate/type",
    "candidate/user-fields Category",
    "candidate/user-fields Height",
    "candidate/user-fields Name",
    "candidate/wall-area",
    "cooling/kwh",
    "cooling/kwp",
    "demand/connection-count",
    "demand/group",
    "demand/kwh",
    "demand/kwp",
    "demand/source",
    "id",
    "path/end",
    "path/length",
    "path/start",
    "solution/capacity-kw",
    "solution/connected",
    "solution/connection-capex annual",
    "solution/connection-capex present",
    "solution/connection-capex principal",
    "solution/connection-capex total",
    "solution/connection-capex type",
    "solution/counterfactual",
    "solution/diameter-mm",
    "solution/diversity",
    "solution/heat-cost annual",
    "solution/heat-cost present",
    "solution/heat-cost total",
    "solution/heat-cost type",
    "solution/heat-revenue annual",
    "solution/heat-revenue present",
    "solution/heat-revenue total",
    "solution/heat-revenue type",
    "solution/included",
    "solution/kwh",
    "solution/kwp",
    "solution/length-factor",
    "solution/losses-kwh",
    "solution/max-capacity-kw",
    "solution/output-kwh",
    "solution/pipe-capex annual",
    "solution/pipe-capex present",
    "solution/pipe-capex principal",
    "solution/pipe-capex total",
    "solution/pipe-capex type",
    "solution/pumping-cost annual",
    "solution/pumping-cost present",
    "solution/pumping-cost total",
    "solution/pumping-cost type",
    "solution/pumping-emissions co2 annual",
    "solution/pumping-emissions co2 kg",
    "solution/pumping-emissions co2 present",
    "solution/pumping-emissions co2 type",
    "solution/pumping-emissions co2 total",
    "solution/pumping-emissions nox annual",
    "solution/pumping-emissions nox kg",
    "solution/pumping-emissions nox present",
    "solution/pumping-emissions nox total",
    "solution/pumping-emissions nox type",
    "solution/pumping-emissions pm25 annual",
    "solution/pumping-emissions pm25 kg",
    "solution/pumping-emissions pm25 present",
    "solution/pumping-emissions pm25 total",
    "solution/pumping-emissions pm25 type",
    "solution/pumping-kwh",
    "solution/supply-capex annual",
    "solution/supply-capex present",
    "solution/supply-capex principal",
    "solution/supply-capex total",
    "solution/supply-capex type",
    "solution/supply-emissions co2 annual",
    "solution/supply-emissions co2 kg",
    "solution/supply-emissions co2 present",
    "solution/supply-emissions co2 total",
    "solution/supply-emissions co2 type",
    "solution/supply-emissions nox annual",
    "solution/supply-emissions nox kg",
    "solution/supply-emissions nox present",
    "solution/supply-emissions nox total",
    "solution/supply-emissions nox type",
    "solution/supply-emissions pm25 annual",
    "solution/supply-emissions pm25 kg",
    "solution/supply-emissions pm25 present",
    "solution/supply-emissions pm25 total",
    "solution/supply-emissions pm25 type",
    "solution/supply-opex annual",
    "solution/supply-opex present",
    "solution/supply-opex total",
    "solution/supply-opex type",
    "solution/unreachable",
    "supply/capacity-kwp",
    "supply/profile-id",
    "tariff/cc-id",
    "tariff/id",
]
