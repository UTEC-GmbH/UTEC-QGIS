"""Project and Layers"""

# pylint: disable=[no-name-in-module]

from dataclasses import dataclass, field

from qgis.core import (
    Qgis,
    QgsLayerTree,
    QgsLayerTreeGroup,
    QgsMapLayer,
    QgsProject,
    QgsVectorLayer,
)

from modules import constants as cont
from modules import exceptions as ex


@dataclass
class ThermosLayers:
    """Layers from Thermos results"""

    pipes: QgsVectorLayer = field(init=False)
    buildings: QgsVectorLayer = field(init=False)

    def __post_init__(self) -> None:
        """Fill class attributes"""
        project: QgsProject | None = QgsProject.instance()
        if not project:
            raise ex.NoProjectError
        if not project.mapLayers():
            project.read(cont.TEST_PROJECT_PATH)

        for layer in project.mapLayers().values():
            if self.is_pipeline_layer(layer):
                self.pipes = layer
            if self.is_building_layer(layer):
                self.buildings = layer

    def is_pipeline_layer(self, layer: QgsMapLayer) -> bool:
        """Check if the given layer is a pipeline layer"""
        return (
            self.is_thermos_result_layer(layer)
            and layer.geometryType() == Qgis.GeometryType.Line  # type: ignore[AttributeAccessIssue, attr-defined]
        )

    def is_building_layer(self, layer: QgsMapLayer) -> bool:
        """Check if the given layer is a building layer"""
        return (
            self.is_thermos_result_layer(layer)
            and layer.geometryType() == Qgis.GeometryType.Polygon  # type: ignore[AttributeAccessIssue, attr-defined]
        )

    def is_thermos_result_layer(self, layer: QgsMapLayer) -> bool:
        """Check if the given layer is a layer from Thermos results"""
        return (
            layer.isValid()
            and layer.name() != "OpenStreetMap"
            and isinstance(layer, QgsVectorLayer)
            and layer.featureCount() > 0
            and all(
                field_name in layer.fields().names()
                for field_name in cont.THERMOS_FIELD_NAMES
            )
        )


def load_project(project_path: str = cont.TEST_PROJECT_PATH) -> QgsProject:
    """Open a QGIS Project using the path to the project file"""
    project: QgsProject | None = QgsProject.instance()
    if not project:
        raise ex.NoProjectError

    if not project.mapLayers():
        project.read(project_path)

    return project


def list_all_layer_names_in_project(
    qgis_project: QgsProject | None = None,
) -> list[str]:
    """List all layers in a project"""
    proj: QgsProject = qgis_project or load_project()
    layers = proj.mapLayers().values()

    return [layer.name() for layer in layers]


def get_layer(layer_name: str, qgis_project: QgsProject | None = None) -> QgsMapLayer:
    """Access a specific layer in a project"""
    proj: QgsProject = qgis_project or load_project()
    return proj.mapLayersByName(layer_name)[0]


def add_layer_group(
    group_name: str = "UTEC_Automation",
    qgis_project: QgsProject | None = None,
) -> None:
    """Add a layer group to a QGIS project"""
    proj: QgsProject = qgis_project or load_project()
    if layer_tree_root := proj.layerTreeRoot():
        layer_tree_root.addGroup(group_name)
    else:
        raise ex.LayerTreeError


def add_temporary_layer(
    layer_name: str,
    group_name: str | None = None,
    layer_type: str = "LineString",
    qgis_project: QgsProject | None = None,
) -> None:
    """Add a layer to a QGIS project"""
    proj: QgsProject = qgis_project or load_project()
    root: QgsLayerTree | None = proj.layerTreeRoot()
    if not root:
        raise ex.LayerTreeError

    # Create a temporary layer (Example: memory layer)
    layer_type_string: str = f"{layer_type}?crs={proj.crs().authid()}"
    new_tmp_layer = QgsVectorLayer(layer_type_string, layer_name, "memory")
    if not new_tmp_layer.isValid():
        raise ex.NewLayerInvalidError(layer_name)

    if group_name:
        # Check if the group exists, if not, create it
        group: QgsLayerTreeGroup | None = root.findGroup(group_name)
        if not group:
            group = root.addGroup(group_name)

        # Add the layer to the group
        if group:
            group.addLayer(new_tmp_layer)

    else:
        proj.addMapLayer(new_tmp_layer)

    proj.write()
