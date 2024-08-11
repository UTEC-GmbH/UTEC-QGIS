"""Features and attributes"""

# pylint: disable=no-name-in-module

from qgis.core import (
    QgsFeature,
    QgsFeatureIterator,
    QgsMapLayer,
    QgsProject,
    QgsWkbTypes,
)

from modules import project_layers as prl

PROJ: QgsProject = prl.load_project()


def all_features_in_layer(layer_name: str = "Trassen") -> QgsFeatureIterator:
    """Get all features in the given layer"""
    layer: QgsMapLayer = prl.get_layer(layer_name)
    return layer.getFeatures()


def get_all_connectors(layer_name: str = "Trassen") -> list[QgsFeature]:
    """Get all features in the given layer"""
    layer: QgsMapLayer = prl.get_layer(layer_name)
    return [
        feature
        for feature in layer.getFeatures()
        if feature.attribute("candidate/user-fields Category") == "Connector"
        and feature.attribute("solution/included")
        and QgsWkbTypes.displayString(feature.geometry().wkbType()) == "LineString"
    ]
