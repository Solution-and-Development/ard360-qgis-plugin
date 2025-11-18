_G='dropdown'
_F='required'
_E='Cancel'
_D='Add Field'
_C='fa-solid fa-layer-group'
_B='Validation Error'
_A='options'
from qgis.PyQt.QtCore import pyqtSignal
from qgis.PyQt.QtGui import QColor
from qgis.PyQt.QtWidgets import QCheckBox,QColorDialog,QComboBox,QDialog,QFormLayout,QGroupBox,QHBoxLayout,QLabel,QLineEdit,QListWidget,QListWidgetItem,QMessageBox,QPushButton,QVBoxLayout
from..api_client import APIClient
class CreateLayerDialog(QDialog):
	layer_created=pyqtSignal(dict)
	def __init__(A,user_id,api_client,parent=None):super().__init__(parent);A.user_id=user_id;A.api_client=api_client;A.custom_fields=[];A.setup_ui()
	def setup_ui(A):K='#3388FF';A.setWindowTitle('Create New Layer');A.setMinimumWidth(500);B=QVBoxLayout();C=QFormLayout();A.name_input=QLineEdit();A.name_input.setPlaceholderText('Building Inspection');C.addRow('Layer Name',A.name_input);D=QHBoxLayout();A.color_button=QPushButton('Choose Color');A.color_button.clicked.connect(A.choose_color);A.color_label=QLabel(K);A.color_label.setStyleSheet('QLabel { background-color: #3388FF; color: white; padding: 5px; border-radius: 3px; }');A.selected_color=QColor(K);D.addWidget(A.color_button);D.addWidget(A.color_label);D.addStretch();C.addRow('Color',D);A.icon_input=QComboBox();A.icon_input.setEditable(True);A.icon_input.addItems([_C,'fa-solid fa-building','fa-solid fa-map-marker','fa-solid fa-draw-polygon','fa-solid fa-route','fa-solid fa-map','fa-solid fa-location-dot']);C.addRow('Icon',A.icon_input);B.addLayout(C);G=QGroupBox('Custom Fields');F=QVBoxLayout();A.fields_list=QListWidget();A.fields_list.setMaximumHeight(150);F.addWidget(A.fields_list);H=QPushButton(_D);H.clicked.connect(A.add_custom_field);F.addWidget(H);G.setLayout(F);B.addWidget(G);E=QHBoxLayout();E.addStretch();I=QPushButton(_E);I.clicked.connect(A.reject);E.addWidget(I);J=QPushButton('Create Layer');J.clicked.connect(A.on_create_clicked);E.addWidget(J);B.addLayout(E);A.setLayout(B)
	def choose_color(A):
		B=QColorDialog.getColor(A.selected_color,A,'Choose Layer Color')
		if B.isValid():A.selected_color=B;C=B.name();A.color_label.setText(C);A.color_label.setStyleSheet(f"QLabel {{ background-color: {C}; color: white; padding: 5px; border-radius: 3px; }}")
	def add_custom_field(B):
		D=AddFieldDialog(B)
		if D.exec_():
			A=D.get_field_data();B.custom_fields.append(A);C=f"{A[_F]} {A['key']} ({A['type']})"
			if A.get(_A):C=f"{C} - {A[_A]}"
			E=QListWidgetItem(C);B.fields_list.addItem(E)
	def on_create_clicked(A):
		K='attributes_template';J='icon';I='color';H='name';D=A.name_input.text().strip()
		if not D:QMessageBox.warning(A,_B,'Please enter a layer name.');return
		E=A.selected_color.name();B=A.icon_input.currentText().strip()
		if not B:B=_C
		C=None
		if A.custom_fields:C={'fields':A.custom_fields}
		F={H:D,I:E,J:B,'layer_type':'all'}
		if C:F[K]=C
		L,G=A.api_client.create_layer(F)
		if L:M={'id':G.get('id'),H:D,'user_id':A.user_id,I:E,J:B,K:C};A.layer_created.emit(M);A.accept()
		else:QMessageBox.critical(A,'Error',f"Failed to create layer via API:\n{G}")
class AddFieldDialog(QDialog):
	def __init__(A,parent=None):super().__init__(parent);A.setup_ui()
	def setup_ui(A):F=False;A.setWindowTitle('Add Custom Field');A.setMinimumWidth(400);B=QFormLayout();A.required=QCheckBox();B.addRow('Required',A.required);A.name_input=QLineEdit();A.name_input.setPlaceholderText('inspector_name (lowercase, no spaces)');B.addRow('Field Name',A.name_input);A.type_combo=QComboBox();A.type_combo.addItems(['text','number','date',_G]);B.addRow('Field Type',A.type_combo);A.dropdown_value=QLineEdit();A.dropdown_value.setPlaceholderText('paper, rock, scissor ');A.dropdown_label=QLabel('Dropdown Value');B.addRow(A.dropdown_label,A.dropdown_value);A.type_combo.currentTextChanged.connect(A.on_type_changed);A.dropdown_value.setVisible(F);A.dropdown_label.setVisible(F);C=QHBoxLayout();C.addStretch();D=QPushButton(_E);D.clicked.connect(A.reject);C.addWidget(D);E=QPushButton(_D);E.clicked.connect(A.on_add_clicked);C.addWidget(E);B.addRow('',C);A.setLayout(B)
	def on_type_changed(A,field_type):B=field_type==_G;A.dropdown_value.setVisible(B);A.dropdown_label.setVisible(B)
	def on_add_clicked(A):
		B=A.name_input.text().strip()
		if not B:QMessageBox.warning(A,_B,'Please enter a field name.');return
		if not B.replace('_','').isalnum()or not B.islower():QMessageBox.warning(A,_B,'Field name must be lowercase and contain only letters, numbers, and underscores.');return
		A.accept()
	def get_field_data(A):
		B={'key':A.name_input.text().strip(),'type':A.type_combo.currentText(),_F:A.required.isChecked()}
		if len(A.dropdown_value.text().split(','))>1:B[_A]=[A.strip()for A in A.dropdown_value.text().split(',')]
		return B