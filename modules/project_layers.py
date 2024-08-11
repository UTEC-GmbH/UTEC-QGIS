"""Project and Layers"""

# pylint: disable=no-name-in-module

from qgis.core import (
    QgsLayerTree,
    QgsLayerTreeGroup,
    QgsMapLayer,
    QgsProject,
    QgsVectorLayer,
)

TEST_PROJECT_PATH: str = "Thermos Output for Testing/thermos.qgz"


def load_project(project_path: str = TEST_PROJECT_PATH) -> QgsProject:
    """Open a QGIS Project using the path to the project file"""
    project: QgsProject | None = QgsProject.instance()
    if not project:
        raise ValueError

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
    if root := proj.layerTreeRoot():
        root.addGroup(group_name)
    else:
        raise ValueError


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
        raise ValueError

    # Create a temporary layer (Example: memory layer)
    layer_type_string: str = f"{layer_type}?crs={proj.crs().authid()}"
    new_tmp_layer = QgsVectorLayer(layer_type_string, layer_name, "memory")
    if not new_tmp_layer.isValid():
        raise ValueError

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
