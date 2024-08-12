"""Features and attributes"""

# pylint: disable=no-name-in-module
from dataclasses import dataclass, field

from qgis.core import (
    Qgis,
    QgsFeature,
    QgsProject,
)

from modules import constants as cont
from modules import project_layers as prl

PROJ: QgsProject = prl.load_project()


@dataclass
class Features:
    """Features and attributes"""

    all_pipes: list[QgsFeature] = field(init=False)
    connectors: list[QgsFeature] = field(init=False)
    links: list[QgsFeature] = field(init=False)
    all_buildings: list[QgsFeature] = field(init=False)
    closest_building: dict[QgsFeature, QgsFeature] = field(init=False)

    def __post_init__(self) -> None:
        """Fill class attributes"""
        thermos_layers = prl.ThermosLayers()
        self.all_pipes = list(thermos_layers.pipes.getFeatures())
        self.all_buildings = list(thermos_layers.buildings.getFeatures())
        self.connectors = list(filter(self.is_connector, self.all_pipes))

    def is_connector(self, feature: QgsFeature) -> bool:
        """Check if the given feature is a connector"""
        return (
            feature.attribute(cont.ThermosFields.type) == "Connector"
            and feature.attribute(cont.ThermosFields.in_solution)
            and feature.geometry().type() == Qgis.GeometryType.Line
        )


# def get_all_connectors(layer_name: str = "Trassen") -> list[QgsFeature]:
#     """Get all features in the given layer"""
#     layer: QgsMapLayer = prl.get_layer(layer_name)
#     features: QgsFeatureIterator = layer.getFeatures()
#     return list(filter(is_connector, features))


# def find_closest_polygon(
#     line_layer_name: str = "Trassen",
#     polygon_layer_name: str = "Gebäude",
# ) -> dict:
#     # Load the layers
#     line_layer: QgsMapLayer = prl.get_layer(line_layer_name)
#     polygon_layer: QgsMapLayer = prl.get_layer(polygon_layer_name)

#     closest_building: dict = {}

#     # Iterate through each line in the line layer
#     for line_feature in line_layer.getFeatures():
#         line_geom = line_feature.geometry()
#         min_distance = float("inf")
#         closest_polygon = None

#         # Iterate through each polygon in the polygon layer
#         for polygon_feature in polygon_layer.getFeatures():
#             polygon_geom = polygon_feature.geometry()
#             distance = line_geom.distance(polygon_geom)

#             # Check if this polygon is closer than the previous closest
#             if distance < min_distance:
#                 min_distance = distance
#                 closest_polygon = polygon_feature

#         # Store the closest polygon for this line
#         closest_building[line_feature.id()] = closest_polygon.id()

#     return closest_building


# # Example usage
# line_layer_name = "Lines"
# polygon_layer_name = "Polygons"
# closest_polygons = find_closest_polygon(line_layer_name, polygon_layer_name)

# for line_id, polygon_id in closest_polygons.items():
#     print(f"Line {line_id} is closest to Polygon {polygon_id}")
