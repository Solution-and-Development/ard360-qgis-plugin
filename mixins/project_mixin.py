_A=False
from qgis.core import QgsProject
class ProjectMixin:
	def add_layer_to_project(B,layer):
		try:QgsProject.instance().addMapLayer(layer);return True
		except Exception as A:print(f"Failed to add layer to project: {str(A)}");return _A
	def add_layers_as_group(G,group_name,layers,index=None):
		B=index;A=group_name
		try:
			C=QgsProject.instance().layerTreeRoot()
			if B is not None:D=C.insertGroup(B,A)
			else:D=C.addGroup(A)
			for E in layers:QgsProject.instance().addMapLayer(E,_A);D.addLayer(E)
			return True
		except Exception as F:print(f"Failed to add layers as group '{A}': {str(F)}");return _A