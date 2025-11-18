_E='db_user_id'
_D='drawing_type'
_C='db_layer_id'
_B=None
_A='drawing_id'
from qgis.core import QgsApplication,QgsProject,QgsVectorLayer
from qgis.PyQt.QtWidgets import QMessageBox
from..api_client import APIClient
from..tasks import SaveDrawingTask,UpdateDrawingTask
from..utilities.geometry import geometry_to_points
from..utilities.image_finder import find_nearest_image
class DrawingManager:
	def __init__(A,api_client,iface):A.api_client=api_client;A.iface=iface;A.monitored_layers={};A.active_tasks=[];A.pending_deletions={};QgsProject.instance().layerWasAdded.connect(A._on_layer_added)
	def _warn_manual_layer(A,layer_name):QMessageBox.information(A.iface.mainWindow(),'ARD360 - Layer Detected',f"Layer '{layer_name}' was created manually.\n\nTo save drawings to the ARD360 database, please use the 'Create New Layer' button in the ARD360 side panel.\n\nThis layer will not be synced to the database.",QMessageBox.Ok)
	def _layer_meta(B,layer):A=layer;return{_C:A.customProperty(_C),_E:A.customProperty(_E),_D:A.customProperty(_D)}
	def _extract_attributes(A,layer,feature,skip=(_A,'type')):B=feature;return{A.name():B[A.name()]for A in layer.fields()if A.name()not in skip and B[A.name()]is not _B}
	def _add_task(A,task):A.active_tasks.append(task);QgsApplication.taskManager().addTask(task)
	def _on_layer_added(B,layer):
		A=layer
		if isinstance(A,QgsVectorLayer)and not A.customProperty(_C):B._warn_manual_layer(A.name())
	def monitor_layer(B,layer):
		A=layer
		if A.id()in B.monitored_layers:print(f"[Sync] Layer {A.name()} already monitored");return
		C=B._layer_meta(A)
		if not C[_C]:print(f"[Sync] WARNING: Layer {A.name()} missing db_layer_id");return
		A.committedFeaturesAdded.connect(lambda _,feats:B._on_features_added(A,feats));A.beforeCommitChanges.connect(lambda:B._on_before_commit(A));A.committedFeaturesRemoved.connect(lambda _,ids:B._on_features_removed(A,ids));A.committedGeometriesChanges.connect(lambda _,ch:B._on_geometry_changed(A,ch));A.committedAttributeValuesChanges.connect(lambda _,ch:B._on_attributes_changed(A,ch));B.monitored_layers[A.id()]=A;print(f"[Sync] Now monitoring layer: {A.name()}")
	def _on_features_added(A,layer,features):
		C=layer;B=A._layer_meta(C)
		if not all(B.values()):print(f"[Sync] ERROR: Missing metadata in {C.name()}");return
		for D in features:
			try:
				E=geometry_to_points(D.geometry(),B[_D]);H=A._extract_attributes(C,D);F=_B
				if E:F=find_nearest_image(E[0],B[_E],A.api_client)
				G=SaveDrawingTask(A.api_client,B[_C],B[_E],B[_D],E,F,H or _B);I=D.id();G.drawing_saved.connect(lambda drawing_id,lyr=C,fid=I:A._on_drawing_saved(lyr,fid,drawing_id));A._add_task(G)
			except Exception as J:print(f"[Sync] ERROR processing feature {D.id()}: {J}")
	def _on_drawing_saved(D,layer,fid,drawing_id):
		A=layer
		try:A.startEditing();B=A.fields().indexOf(_A);A.changeAttributeValue(fid,B,drawing_id);A.commitChanges()
		except Exception as C:print(f"[Sync] ERROR updating drawing_id: {C}");A.rollBack()
	def _on_before_commit(H,layer):
		A=layer;D=A.editBuffer()
		if not D:return
		E=D.deletedFeatureIds()
		if not E:return
		I=A.id();J=H.pending_deletions.setdefault(I,{})
		for B in E:
			try:
				C=A.getFeature(B)
				if not C.isValid():
					from qgis.core import QgsFeatureRequest as K;F=list(A.dataProvider().getFeatures(K(B)))
					if F:C=F[0]
					else:continue
				G=C.attribute(_A)
				if G is not _B:J[B]=G
			except Exception as L:print(f"[Sync] ERROR caching drawing_id for {B}: {L}")
	def _on_features_removed(A,layer,fids):
		D=layer.id();C=A.pending_deletions.get(D,{})
		for B in fids:
			E=C.get(B)
			if not E:continue
			try:from..tasks import DeleteDrawingTask as F;G=F(A.api_client,E);A._add_task(G)
			except Exception as H:print(f"[Sync] ERROR deleting feature {B}: {H}")
		for B in fids:C.pop(B,_B)
		if not C:A.pending_deletions.pop(D,_B)
	def _on_geometry_changed(A,layer,changes):
		B=layer;D=B.customProperty(_D)
		for(C,E)in changes.items():
			try:F=B.getFeature(C)[_A];G=geometry_to_points(E,D);H=UpdateDrawingTask(A.api_client,F,points=G);A._add_task(H)
			except Exception as I:print(f"[Sync] ERROR geometry change for {C}: {I}")
	def _on_attributes_changed(A,layer,changes):
		B=layer
		for C in changes.keys():
			try:D=B.getFeature(C);E=D[_A];F={A.name():D[A.name()]for A in B.fields()if A.name()not in[_A,'type']};G=UpdateDrawingTask(A.api_client,E,attributes=F);A._add_task(G)
			except Exception as H:print(f"[Sync] ERROR attribute change for {C}: {H}")
	def stop_monitoring_layer(B,layer):
		A=layer
		if A.id()not in B.monitored_layers:return
		try:
			for C in(A.committedFeaturesAdded,A.beforeCommitChanges,A.committedFeaturesRemoved,A.committedGeometriesChanges,A.committedAttributeValuesChanges):C.disconnect()
		except Exception:pass
		del B.monitored_layers[A.id()];print(f"[Sync] Stopped monitoring: {A.name()}")
	def stop_all_monitoring(A):
		for B in list(A.monitored_layers.values()):A.stop_monitoring_layer(B)
		print('[Sync] Stopped monitoring all layers')