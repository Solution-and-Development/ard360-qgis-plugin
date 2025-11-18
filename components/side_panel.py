_N='Select All'
_M='color: gray; font-style: italic;'
_L='No drawing layers found'
_K='color: orange;'
_J='color: red;'
_I='color: blue;'
_H='ARD360'
_G='Loading...'
_F='Deselect All'
_E='name'
_D=None
_C='id'
_B=False
_A=True
from qgis.core import QgsProject
from qgis.PyQt.QtCore import Qt,pyqtSignal
from qgis.PyQt.QtWidgets import QCheckBox,QDockWidget,QFormLayout,QHBoxLayout,QLabel,QLineEdit,QMessageBox,QPushButton,QScrollArea,QStackedWidget,QVBoxLayout,QWidget
from..constants.general import APPLICATION_TITLE
from..api_client import APIClient
from..services import DrawingService
from..utilities.auth_storage import AuthStorage
from.create_layer_dialog import CreateLayerDialog
class SidePanel(QDockWidget):
	login_successful=pyqtSignal(int);logout_requested=pyqtSignal();load_data_requested=pyqtSignal(list,list)
	def __init__(A,api_client,parent=_D):super().__init__(APPLICATION_TITLE,parent);A.api_client=api_client;A.datasets=[];A.layers=[];A.dataset_checkboxes=[];A.layer_checkboxes=[];A.sync_manager=_D;A.loaded_drawing_groups={};A.layer_position={};A.setAllowedAreas(Qt.LeftDockWidgetArea|Qt.RightDockWidgetArea);A.setFeatures(QDockWidget.DockWidgetClosable|QDockWidget.DockWidgetMovable);A.init_ui()
	def init_ui(A):B=QWidget();C=QVBoxLayout(B);C.setContentsMargins(10,10,10,10);A.stacked_widget=QStackedWidget();A.login_page=A.create_login_page();A.stacked_widget.addWidget(A.login_page);A.selection_page=A.create_selection_page();A.stacked_widget.addWidget(A.selection_page);C.addWidget(A.stacked_widget);A.setWidget(B);A.show_login_page()
	def create_login_page(A):F='Login';E=QWidget();B=QVBoxLayout(E);C=QLabel(F);C.setStyleSheet('font-weight: bold; font-size: 16px; padding: 10px 0;');C.setAlignment(Qt.AlignCenter);B.addWidget(C);D=QFormLayout();A.username_input=QLineEdit();A.username_input.setPlaceholderText('Enter username');A.username_input.returnPressed.connect(A.handle_login);D.addRow('Username:',A.username_input);A.password_input=QLineEdit();A.password_input.setEchoMode(QLineEdit.Password);A.password_input.setPlaceholderText('Enter password');A.password_input.returnPressed.connect(A.handle_login);D.addRow('Password:',A.password_input);B.addLayout(D);A.remember_me_checkbox=QCheckBox('Remember me');A.remember_me_checkbox.setChecked(_A);B.addWidget(A.remember_me_checkbox);A.login_status_label=QLabel('');A.login_status_label.setAlignment(Qt.AlignCenter);A.login_status_label.setWordWrap(_A);B.addWidget(A.login_status_label);A.login_btn=QPushButton(F);A.login_btn.clicked.connect(A.handle_login);A.login_btn.setDefault(_A);B.addWidget(A.login_btn);B.addStretch();return E
	def create_selection_page(A):Q='font-weight: bold; font-size: 13px;';J=QWidget();B=QVBoxLayout(J);C=QHBoxLayout();A.user_label=QLabel('');A.user_label.setStyleSheet('font-weight: bold;');C.addWidget(A.user_label);C.addStretch();A.logout_btn=QPushButton('Logout');A.logout_btn.clicked.connect(A.handle_logout);C.addWidget(A.logout_btn);B.addLayout(C);K=QLabel('Select data to load:');K.setStyleSheet('font-weight: bold; font-size: 14px; padding: 10px 0;');B.addWidget(K);F=QScrollArea();F.setWidgetResizable(_A);L=QWidget();G=QVBoxLayout(L);M=QWidget();H=QVBoxLayout(M);H.setContentsMargins(0,0,0,0);D=QHBoxLayout();N=QLabel('Datasets');N.setStyleSheet(Q);D.addWidget(N);D.addStretch();A.toggle_datasets_btn=QPushButton(_F);A.toggle_datasets_btn.setMaximumWidth(100);A.toggle_datasets_btn.clicked.connect(A.toggle_datasets_selection);D.addWidget(A.toggle_datasets_btn);H.addLayout(D);A.datasets_container=QVBoxLayout();A.datasets_loading_label=QLabel(_G);A.datasets_container.addWidget(A.datasets_loading_label);H.addLayout(A.datasets_container);G.addWidget(M);O=QWidget();I=QVBoxLayout(O);I.setContentsMargins(0,0,0,10);E=QHBoxLayout();P=QLabel('Layers');P.setStyleSheet(Q);E.addWidget(P);E.addStretch();A.toggle_layers_btn=QPushButton(_F);A.toggle_layers_btn.setMaximumWidth(100);A.toggle_layers_btn.clicked.connect(A.toggle_layers_selection);E.addWidget(A.toggle_layers_btn);I.addLayout(E);A.layers_container=QVBoxLayout();A.layers_loading_label=QLabel(_G);A.layers_container.addWidget(A.layers_loading_label);I.addLayout(A.layers_container);G.addWidget(O);G.addStretch();F.setWidget(L);B.addWidget(F);A.selection_status_label=QLabel('');A.selection_status_label.setAlignment(Qt.AlignCenter);A.selection_status_label.setWordWrap(_A);B.addWidget(A.selection_status_label);A.create_layer_btn=QPushButton('New Layer');A.create_layer_btn.clicked.connect(A.on_create_layer_clicked);B.addWidget(A.create_layer_btn);A.load_btn=QPushButton('Load Selected Data');A.load_btn.clicked.connect(A.handle_load_data);B.addWidget(A.load_btn);A.refresh_btn=QPushButton('Refresh Selected Layer');A.refresh_btn.clicked.connect(A.on_refresh_drawings_clicked);A.refresh_btn.setVisible(_B);B.addWidget(A.refresh_btn);return J
	def show_login_page(A):
		A.stacked_widget.setCurrentWidget(A.login_page)
		if AuthStorage.has_stored_session():from qgis.PyQt.QtCore import QTimer as B;B.singleShot(100,A.attempt_auto_login)
		else:A.username_input.setFocus()
	def show_selection_page(A):A.stacked_widget.setCurrentWidget(A.selection_page)
	def attempt_auto_login(A):
		A.login_status_label.setText('Auto-login...');A.login_status_label.setStyleSheet(_I);A.login_btn.setEnabled(_B);C,B=AuthStorage.load_session()
		if not C:A.login_status_label.setText(f"Auto-login failed: {B}");A.login_status_label.setStyleSheet(_J);A.login_btn.setEnabled(_A);A.username_input.setFocus();AuthStorage.clear_session();return
		D=B['jwt_token'];E=B['username'];F=B['user_id'];A.api_client.set_jwt_token(D);G,H=A.api_client.verify_token()
		if G:A.user_label.setText(E);A.login_status_label.setText('');A.show_selection_page();A.login_successful.emit(F)
		else:A.login_status_label.setText(f"Auto-login failed: Session expired");A.login_status_label.setStyleSheet(_K);A.login_btn.setEnabled(_A);A.username_input.setFocus();AuthStorage.clear_session()
	def handle_login(A):
		B=A.username_input.text().strip();D=A.password_input.text()
		if not B or not D:A.login_status_label.setText('Please enter both username and password');A.login_status_label.setStyleSheet(_J);return
		A.login_status_label.setText('Authenticating...');A.login_status_label.setStyleSheet(_I);A.login_btn.setEnabled(_B);G,E=A.api_client.authenticate(B,D)
		if G:
			F=E.get('user',{});C=F.get(_C);H=E.get('token')
			if A.remember_me_checkbox.isChecked():
				I,J=AuthStorage.save_session(H,F)
				if not I:AuthStorage.set_user_id(C);A.login_status_label.setText(f"Warning: Failed to save session: {J}");A.login_status_label.setStyleSheet(_K)
			else:AuthStorage.clear_session();AuthStorage.set_user_id(C)
		A.user_label.setText(B);A.login_status_label.setText('');A.password_input.clear();A.show_selection_page();A.login_successful.emit(C);A.login_btn.setEnabled(_A)
	def handle_logout(A):
		E='Are you sure you want to logout?';D='Confirm Logout';F=AuthStorage.has_stored_session()
		if F:
			B=QMessageBox(A);B.setWindowTitle(D);B.setText(E);B.setInformativeText('Do you want to forget your saved session?');B.setStandardButtons(QMessageBox.Yes|QMessageBox.No|QMessageBox.Cancel);B.setDefaultButton(QMessageBox.No);B.button(QMessageBox.Yes).setText('Logout && Forget');B.button(QMessageBox.No).setText('Logout Only');C=B.exec_()
			if C==QMessageBox.Cancel:return
			if C==QMessageBox.Yes:AuthStorage.clear_session()
		else:
			C=QMessageBox.question(A,D,E,QMessageBox.Yes|QMessageBox.No,QMessageBox.No)
			if C!=QMessageBox.Yes:return
		A.username_input.clear();A.password_input.clear();A.login_status_label.setText('');A.clear_datasets();A.clear_layers();A.loaded_drawing_groups.clear();A.refresh_btn.setVisible(_B);A.show_login_page();A.logout_requested.emit()
	def load_datasets_and_layers(A):
		E=AuthStorage.get_user_id()
		if E is _D:return
		B,C=A.api_client.get_datasets()
		if B and C:A.datasets=C;A.display_datasets()
		else:A.datasets_loading_label.setText('No datasets found'if B else f"Error: {C}")
		B,D=A.api_client.get_layers()
		if B and D:A.layers=D;A.display_layers()
		else:A.layers_loading_label.setText(_L if B else f"Error: {D}")
	def clear_datasets(A):
		for B in A.dataset_checkboxes:A.datasets_container.removeWidget(B);B.deleteLater()
		A.dataset_checkboxes.clear();A.datasets.clear();A.datasets_loading_label=QLabel(_G);A.datasets_container.addWidget(A.datasets_loading_label)
	def clear_layers(A):
		for B in A.layer_checkboxes:A.layers_container.removeWidget(B);B.deleteLater()
		A.layer_checkboxes.clear();A.layers.clear();A.layers_loading_label=QLabel(_G);A.layers_container.addWidget(A.layers_loading_label)
	def display_datasets(A):
		if A.datasets_loading_label:A.datasets_container.removeWidget(A.datasets_loading_label);A.datasets_loading_label.deleteLater();A.datasets_loading_label=_D
		for C in A.datasets:B=QCheckBox(f"{C[_E]} (ID: {C[_C]})");B.setChecked(_A);B.dataset_id=C[_C];A.dataset_checkboxes.append(B);A.datasets_container.addWidget(B)
		if not A.datasets:D=QLabel('No datasets available');D.setStyleSheet(_M);A.datasets_container.addWidget(D)
	def display_layers(A):
		if A.layers_loading_label:A.layers_container.removeWidget(A.layers_loading_label);A.layers_loading_label.deleteLater();A.layers_loading_label=_D
		for C in A.layers:B=QCheckBox(f"{C[_E]} (ID: {C[_C]})");B.setChecked(_A);B.layer_id=C[_C];B.layer_color=C['color'];A.layer_checkboxes.append(B);A.layers_container.addWidget(B)
		if not A.layers:D=QLabel('No drawing layers available');D.setStyleSheet(_M);A.layers_container.addWidget(D)
	def toggle_datasets_selection(A):
		C=all(A.isChecked()for A in A.dataset_checkboxes)if A.dataset_checkboxes else _B;B=not C
		for D in A.dataset_checkboxes:D.setChecked(B)
		A.toggle_datasets_btn.setText(_F if B else _N)
	def toggle_layers_selection(A):
		C=all(A.isChecked()for A in A.layer_checkboxes)if A.layer_checkboxes else _B;B=not C
		for D in A.layer_checkboxes:D.setChecked(B)
		A.toggle_layers_btn.setText(_F if B else _N)
	def handle_load_data(A):
		B=A.get_selected_datasets();C=A.get_selected_layers()
		if not B and not C:QMessageBox.warning(A,'No Selection','Please select at least one dataset or layer to load.');return
		D=[]
		if B:D.append(f"{len(B)} dataset(s)")
		if C:D.append(f"{len(C)} drawing layer(s)")
		E=f"Load {' and '.join(D)} to the map?";F=QMessageBox.question(A,'Confirm Selection',E,QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)
		if F==QMessageBox.Yes:A.load_data_requested.emit(B,C)
	def get_selected_datasets(A):return[A.dataset_id for A in A.dataset_checkboxes if A.isChecked()]
	def get_selected_layers(A):return[A.layer_id for A in A.layer_checkboxes if A.isChecked()]
	def get_user_id(A):return AuthStorage.get_user_id()
	def on_create_layer_clicked(A):
		B=AuthStorage.get_user_id()
		if not B:QMessageBox.warning(A,'Not Logged In','Please login to create a layer');return
		C=CreateLayerDialog(B,A.api_client,A);C.layer_created.connect(A.on_layer_created);C.exec_()
	def on_layer_created(A,layer_data):
		D=layer_data;G=DrawingService(A.api_client);H,E=G.create_empty_layer_group(D)
		if not H:QMessageBox.critical(A,'Error',f"Failed to create QGIS layers:\n{E}");return
		B=D[_E];I=QgsProject.instance().layerTreeRoot();J=I.insertGroup(0,B)
		for C in E:QgsProject.instance().addMapLayer(C,_B);J.addLayer(C)
		if A.sync_manager:
			for C in E:A.sync_manager.monitor_layer(C)
		F=D[_C];A.loaded_drawing_groups[F]={_E:B,'index':0};print(f"[SidePanel] Tracking newly created group: {B} at index 0 (layer_id={F})");A.refresh_btn.setVisible(_A);A.refresh_layer_list();from qgis.utils import iface;iface.messageBar().pushSuccess(_H,f"Layer group '{B}' created! You can now draw markers, lines, or polygons.")
	def on_refresh_drawings_clicked(A):
		if not A.loaded_drawing_groups:from qgis.utils import iface;iface.messageBar().pushWarning(_H,'No drawing layers are currently loaded');return
		from qgis.core import QgsProject as D;from qgis.utils import iface;E=list(A.loaded_drawing_groups.keys());L=len(E);iface.messageBar().pushInfo(_H,f"Refreshing {L} drawing layer(s)...");F=D.instance().layerTreeRoot();G={}
		for(M,N)in list(A.loaded_drawing_groups.items()):
			H=N[_E];B=F.findGroup(H)
			if B:
				I=B.parent()
				if I:J=I.children();O=J.index(B)if B in J else-1;G[M]=O
				K=[A.layer()for A in B.findLayers()]
				if A.sync_manager:
					for C in K:
						if C:A.sync_manager.stop_monitoring_layer(C)
				for C in K:
					if C:D.instance().removeMapLayer(C.id())
				F.removeChildNode(B);print(f"[SidePanel] Removed layer group: {H}")
		A.refresh_positions=G;A.loaded_drawing_groups.clear();A.load_data_requested.emit([],E)
	def refresh_layer_list(A):
		D=AuthStorage.get_user_id()
		if not D:return
		A.clear_layers();C,B=A.api_client.get_layers()
		if C and B:A.layers=B;A.display_layers()
		else:A.layers_loading_label.setText(_L if C else f"Error: {B}")