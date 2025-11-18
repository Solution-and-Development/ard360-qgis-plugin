_E='User not logged in'
_D='Please login first'
_C=False
_B=None
_A='ARD360'
import os
from qgis.core import QgsMapLayer
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction
from.constants.host import DEFAULT_HOST
from.api_client import APIClient
from.components.side_panel import SidePanel
from.constants.general import APPLICATION_TITLE
from.data_loader import DataLoader
from.managers import DrawingManager
from.utilities.auth_storage import AuthStorage
plugin_dir=os.path.dirname(__file__)
class ArdPlugin:
	def __init__(A,iface):A.iface=iface;A.api_client=APIClient();A.data_loader=DataLoader(A.api_client);A.current_layer=_B;A.main_panel=_B;A.sync_manager=_B
	def initGui(A):A.main_panel=SidePanel(A.api_client,A.iface.mainWindow());A.main_panel.login_successful.connect(A.on_login_successful);A.main_panel.logout_requested.connect(A.on_logout);A.main_panel.load_data_requested.connect(A.on_load_data_requested);A.iface.addDockWidget(Qt.RightDockWidgetArea,A.main_panel);B=os.path.join(plugin_dir,'assets/images/logo.png');C=QIcon(B)if os.path.exists(B)else QIcon();A.action_main=QAction(C,APPLICATION_TITLE,A.iface.mainWindow());A.action_main.triggered.connect(A.toggle_panel);A.iface.addToolBarIcon(A.action_main);A.iface.mapCanvas().selectionChanged.connect(A.on_selection_changed)
	def unload(A):
		A.iface.removeToolBarIcon(A.action_main)
		if A.main_panel:A.iface.removeDockWidget(A.main_panel);A.main_panel.deleteLater();A.main_panel=_B
		try:A.iface.mapCanvas().selectionChanged.disconnect(A.on_selection_changed)
		except ConnectionError:pass
		del A.action_main
	def toggle_panel(A):
		if A.main_panel:
			if A.main_panel.isVisible():A.main_panel.hide()
			else:A.main_panel.show()
	def on_login_successful(A,user_id):
		A.sync_manager=DrawingManager(A.api_client,A.iface)
		if A.main_panel:A.main_panel.sync_manager=A.sync_manager;A.main_panel.load_datasets_and_layers()
		A.iface.messageBar().pushSuccess(_A,'Login successful')
	def on_logout(A):
		if A.sync_manager:A.sync_manager.stop_all_monitoring();A.sync_manager=_B
		if A.main_panel:A.main_panel.sync_manager=_B
		A.iface.messageBar().pushInfo(_A,'Logged out')
	def on_load_data_requested(A,selected_datasets,selected_layers):
		D=selected_layers;C=selected_datasets;H=0;K=0
		if C:
			A.iface.messageBar().pushInfo(_A,f"Loading {len(C)} dataset(s)...");E,B=A.load_tracklog(C)
			if E:
				F=B if isinstance(B,list)else[B]
				for G in F:H+=G.featureCount();K+=1
				A.iface.messageBar().pushSuccess(_A,f"Loaded {H} 360 points from {len(C)} dataset(s)")
			else:A.iface.messageBar().pushCritical(_A,f"Failed to load 360 points: {B}")
		if D:
			A.iface.messageBar().pushInfo(_A,f"Loading {len(D)} drawing layer(s)...");E,B=A.load_drawings(D)
			if E:
				L=B;I=0;J=0
				for(M,F)in L:
					for G in F:I+=G.featureCount();J+=1
				A.iface.messageBar().pushSuccess(_A,f"Loaded {I} drawing(s) in {J} layer(s)")
			else:A.iface.messageBar().pushCritical(_A,f"Failed to load drawings: {B}")
		if C and D:A.iface.messageBar().pushSuccess(_A,'Successfully loaded all selected data')
	def load_tracklog(A,dataset_ids=_B):
		D=dataset_ids;F=AuthStorage.get_user_id()
		if F is _B:
			A.iface.messageBar().pushWarning(_A,_D)
			if A.main_panel:A.main_panel.show()
			return _C,_E
		if D is _B:A.iface.messageBar().pushInfo(_A,'Loading 360 points from database...')
		H,C=A.data_loader.load_tracklog_layer(F,dataset_ids=D)
		if H:
			B=C if isinstance(C,list)else[C];E=0
			for G in B:A.data_loader.add_layer_to_project(G);E+=G.featureCount()
			A.current_layer=B[0]if B else _B
			if D is _B:
				if len(B)==1:A.iface.messageBar().pushSuccess(_A,f"Successfully loaded {E} 360 points")
				else:A.iface.messageBar().pushSuccess(_A,f"Successfully loaded {E} 360 points across {len(B)} layers")
			return True,B
		else:
			if D is _B:A.iface.messageBar().pushCritical(_A,f"Failed to load 360 points: {C}")
			return _C,C
	def load_drawings(A,layer_ids=_B):
		R='refresh_positions';J='db_layer_id';D=layer_ids;K=AuthStorage.get_user_id()
		if K is _B:
			A.iface.messageBar().pushWarning(_A,_D)
			if A.main_panel:A.main_panel.show()
			return _C,_E
		if D is _B:A.iface.messageBar().pushInfo(_A,'Loading drawings from database...')
		S,H=A.data_loader.load_drawing_layers(K,layer_ids=D)
		if S:
			E=H;L=0;M=0;from qgis.core import QgsProject as T
			for(I,B)in E:
				N=_B
				if A.main_panel and B and hasattr(A.main_panel,R):
					C=B[0].customProperty(J)
					if C and C in A.main_panel.refresh_positions:N=A.main_panel.refresh_positions[C]
				A.data_loader.add_layers_as_group(I,B,index=N);U=T.instance().layerTreeRoot();F=U.findGroup(I);O=-1
				if F:
					P=F.parent()
					if P:Q=P.children();O=Q.index(F)if F in Q else-1
				if A.main_panel and B:
					C=B[0].customProperty(J)
					if C:A.main_panel.loaded_drawing_groups[C]={'name':I,'index':O}
				if A.sync_manager:
					for G in B:A.sync_manager.monitor_layer(G);print(f"[Main] Monitoring layer: {G.name()} (id={G.customProperty(J)}, type={G.customProperty('drawing_type')})")
				else:A.iface.messageBar().pushCritical(_A,'Sync manager not initialized, loaded layers will not be monitored')
			if A.main_panel and A.main_panel.loaded_drawing_groups:A.main_panel.refresh_btn.setVisible(True)
			if A.main_panel and hasattr(A.main_panel,R):A.main_panel.refresh_positions.clear()
			if D is _B:
				if len(E)==1:A.iface.messageBar().pushSuccess(_A,f"Successfully loaded {L} drawing(s) in {M} layer(s)")
				else:A.iface.messageBar().pushSuccess(_A,f"Successfully loaded {L} drawing(s) across {len(E)} group(s) ({M} layer(s))")
			return True,E
		else:
			if D is _B:A.iface.messageBar().pushCritical(_A,f"Failed to load drawings: {H}")
			return _C,H
	def on_selection_changed(C,layer):
		A=layer
		if A and isinstance(A,QgsMapLayer):
			B=A.selectedFeatures()
			if len(B)==1:C.view_selected_360(B[0])
	def view_selected_360(A,feature=_B):
		C=feature
		if not C:
			D=A.iface.activeLayer()
			if not D:A.iface.messageBar().pushWarning(_A,'No layer selected');return
			E=D.selectedFeatures()
			if not E:A.iface.messageBar().pushWarning(_A,'Please select a 360 point on the map');return
			C=E[0]
		B=_B
		try:B=C['coordinate_id']
		except KeyError:
			try:B=C['id']
			except KeyError:pass
		if not B:A.iface.messageBar().pushWarning(_A,'No coordinate ID found for selected feature');return
		F=AuthStorage.get_token()
		if not F:A.iface.messageBar().pushWarning(_A,'No authentication token found. Please login first.');return
		G=DEFAULT_HOST;from urllib.parse import quote;H=f"{G}/map?coordinate_id={B}&token={quote(F)}"
		try:from qgis.PyQt.QtCore import QUrl;from qgis.PyQt.QtGui import QDesktopServices as I;J=QUrl(H);I.openUrl(J);A.iface.messageBar().pushInfo(_A,f"Opening 360 image (coordinate_id: {B}) in browser...")
		except Exception as K:A.iface.messageBar().pushCritical(_A,f"Failed to open 360 viewer: {str(K)}")