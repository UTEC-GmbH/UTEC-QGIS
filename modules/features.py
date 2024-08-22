"""Features and attributes"""

# pylint: disable=no-name-in-module
from dataclasses import dataclass, field, fields
from typing import Self

from qgis.core import Qgis, QgsDistanceArea, QgsFeature, QgsGeometry, QgsPointXY

from modules import constants as cont
from modules import exceptions as ex
from modules import project_layers as prl


@dataclass
class Building:
    """Building feature"""

    feature: QgsFeature
    attributes: dict = field(init=False)
    geometry: QgsGeometry = field(init=False)
    area_roof: float | None = None
    area_ground: float | None = None
    demand_cap_cooling: float | None = None
    demand_cap_heat: float | None = None
    demand_cap_ww: float | None = None
    demand_cons_cooling: float | None = None
    demand_cons_heat: float | None = None
    demand_cons_ww: float | None = None
    height: int | None = None
    id: str | None = None
    in_solution: bool | None = None
    point_id_connection: str | None = None
    supply_capacity: int | None = None

    def __post_init__(self) -> None:
        """Fill class attributes"""
        self.attributes = self.feature.attributeMap()
        self.geometry = self.feature.geometry()
        for attr in fields(self):
            field_name: str | None = getattr(cont.ThermosFields, attr.name, None)
            if (
                attr.name not in ["feature", "attributes", "geometry"]
                and isinstance(field_name, str)
                and isinstance(self.attributes.get(field_name), attr.type)  # type: ignore[argument-type]
            ):
                setattr(self, attr.name, self.attributes.get(field_name))


@dataclass
class Pipe:
    """Pipe feature"""

    feature: QgsFeature
    attributes: dict = field(init=False)
    geometry: QgsGeometry = field(init=False)
    id: str | None = None
    connected_buildings: list[Building] | Building | None = None
    connected_pipes: list[Self] | Self | None = None
    point_id_end: str | None = None
    point_id_start: str | None = None
    diameter: int | None = None
    length: int | None = None
    capacity: int | None = None  # Heizleistung in Leitung
    diversity: float | None = None  # Gleichzeitigkeitsfaktor

    def __post_init__(self) -> None:
        """Fill class attributes"""
        self.attributes = self.feature.attributeMap()
        self.geometry = self.feature.geometry()
        for attr in fields(self):
            field_name: str | None = getattr(cont.ThermosFields, attr.name, None)
            if (
                attr.name not in ["feature", "attributes", "geometry"]
                and isinstance(field_name, str)
                and isinstance(self.attributes.get(field_name), attr.type)  # type: ignore[argument-type]
            ):
                setattr(self, attr.name, self.attributes.get(field_name))


@dataclass
class Knot:
    """Knot feature"""

    id: str
    coordinates: QgsPointXY
    connected_pipes: list[Pipe] | Pipe | None = None
    connected_buildings: list[Building] | Building | None = None


@dataclass
class Branch:
    """Branch feature"""

    id: str
    connected_pipes: list[Pipe] | Pipe | None = None
    connected_buildings: list[Building] | Building | None = None


@dataclass
class ThermosFeatures:
    """Features and attributes in solution"""

    all_pipes: list[Pipe] = field(init=False)
    all_buildings: list[Building] = field(init=False)
    connectors: list[Pipe] = field(init=False)
    links: list[Pipe] = field(init=False)

    def __post_init__(self) -> None:
        """Fill class attributes"""
        thermos_layers = prl.ThermosLayers()
        self.all_pipes = [
            Pipe(feat)
            for feat in list(thermos_layers.pipes.getFeatures())  # type: ignore[reportArgumentType]
            if self.check_pipe(feat)
        ]
        self.all_buildings = [
            Building(feat)
            for feat in list(thermos_layers.buildings.getFeatures())  # type: ignore[reportArgumentType]
            if self.check_building(feat)
        ]

        for pipe in self.all_pipes:
            pipe.connected_buildings = self.directly_connected_building(pipe)

        for pipe in [
            pip
            for pip in self.all_pipes
            if isinstance(pip.connected_buildings, list)
            and len(pip.connected_buildings) > 1
        ]:
            self.clean_up_pipe_connected_to_multi_bldg(pipe)

        self.connectors = [pipe for pipe in self.all_pipes if pipe.connected_buildings]
        self.links = [pipe for pipe in self.all_pipes if pipe not in self.connectors]

    def check_pipe(self, feature: QgsFeature) -> bool:
        """Check if a given feature is a pipe"""
        return (
            feature.attribute(cont.ThermosFields.in_solution)
            and feature.geometry().type() == Qgis.GeometryType.Line
        )

    def check_building(self, feature: QgsFeature) -> bool:
        """Check if a given feature is a building"""
        return (
            feature.attribute(cont.ThermosFields.in_solution)
            and feature.geometry().type() == Qgis.GeometryType.Polygon
        )

    def get_building_from_id(self, id_str: str) -> Building | None:
        """Return the building with the given id"""
        return next(bldg for bldg in self.all_buildings if bldg.id == id_str)

    def get_pipe_from_id(self, id_str: str) -> Pipe | None:
        """Return the pipe with the given id"""
        return next(pipe for pipe in self.all_pipes if pipe.id == id_str)

    def directly_connected_building(
        self, pipe: Pipe
    ) -> list[Building] | Building | None:
        """Return the building directly connected to the given pipe"""
        if buildings_close_to_pipe := [
            building
            for building in self.all_buildings
            if any(
                self.point_near_polygon(point, building.geometry)
                for point in pipe.geometry.asPolyline()
            )
        ]:
            return (
                buildings_close_to_pipe[0]
                if len(buildings_close_to_pipe) == 1
                else buildings_close_to_pipe
            )
        return None

    def clean_up_pipe_connected_to_multi_bldg(self, pipe: Pipe) -> None:
        """Return the building directly connected to the given pipe,
        when there are multiple buildings close to it
        """
        if not isinstance(pipe.connected_buildings, list):
            raise ex.PipeNotConnectedToMultipleBuildingsError(pipe)

        for building in pipe.connected_buildings:
            if [
                pip
                for pip in [p for p in self.all_pipes if p != pipe]
                if (
                    isinstance(pip.connected_buildings, Building)
                    and pip.connected_buildings == building
                )
                or (
                    isinstance(pip.connected_buildings, list)
                    and building in pip.connected_buildings
                )
            ]:
                pipe.connected_buildings.remove(building)

        if len(pipe.connected_buildings) == 1:
            pipe.connected_buildings = pipe.connected_buildings[0]

    def point_near_polygon(
        self, point: QgsPointXY, building: QgsGeometry, tolerance: float = 0.01
    ) -> bool:
        """Check if a point is in, on or near a polygon"""
        point_geom: QgsGeometry = QgsGeometry.fromPointXY(point)
        shortest_line: QgsGeometry = point_geom.shortestLine(building)

        # Create a QgsDistanceArea object to calculate distances
        distance_area_object: QgsDistanceArea = QgsDistanceArea()
        distance_area_object.setEllipsoid("WGS84")  # "WGS84" is the default

        return (
            building.contains(point_geom)
            or building.intersects(point_geom)
            or distance_area_object.measureLength(shortest_line) < tolerance
        )

    def problematic_pipes(
        self, *, return_ids: bool = True
    ) -> dict[str, list[str]] | dict[str, list[Pipe]]:
        """Return problematic pipes"""
        multi: str = "pipes with multiple connected buildings"
        dic: dict[str, list[Pipe]] = {
            multi: [
                pipe
                for pipe in self.all_pipes
                if isinstance(pipe.connected_buildings, list)
                and len(pipe.connected_buildings) > 1
            ]
        }

        return (
            {
                multi: sorted([p.id for p in dic[multi] if p.id], key=str.lower),
            }
            if return_ids
            else dic
        )

    def problematic_buildings(
        self, *, return_ids: bool = True
    ) -> dict[str, list[Building]] | dict[str, list[str]]:
        """Check if all buildings are connected"""
        directly_connected_buildings: list[Building] = [
            pipe.connected_buildings
            for pipe in self.all_pipes
            if isinstance(pipe.connected_buildings, Building)
        ]
        wo: str = "buildings without connector"
        multi: str = "buildings with multiple connectors"
        dic: dict[str, list[Building]] = {
            wo: [
                building
                for building in self.all_buildings
                if building not in directly_connected_buildings
            ],
            multi: [
                building
                for building in self.all_buildings
                if directly_connected_buildings.count(building) > 1
                and not building.supply_capacity
            ],
        }

        return (
            {
                wo: sorted([b.id for b in dic[wo] if b.id], key=str.lower),
                multi: sorted([b.id for b in dic[multi] if b.id], key=str.lower),
            }
            if return_ids
            else dic
        )
