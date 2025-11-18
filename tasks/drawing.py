_E='attributes'
_D='points'
_C=False
_B='ARD360'
_A=None
from qgis.core import Qgis,QgsMessageLog,QgsTask
from qgis.PyQt.QtCore import pyqtSignal
class SaveDrawingTask(QgsTask):
	drawing_saved=pyqtSignal(int)
	def __init__(A,api_client,layer_id,user_id,drawing_type,points,image_file=_A,attributes=_A):super().__init__('Saving drawing via API',QgsTask.CanCancel);A.api_client=api_client;A.layer_id=layer_id;A.user_id=user_id;A.drawing_type=drawing_type;A.points=points;A.image_file=image_file;A.attributes=attributes;A.drawing_id=_A;A.error_message=_A
	def run(A):
		try:
			B={'layer_id':A.layer_id,'type':A.drawing_type,_D:A.points}
			if A.image_file:B['image_file']=A.image_file
			if A.attributes:B[_E]=A.attributes
			D,C=A.api_client.create_drawing(B)
			if D:A.drawing_id=C.get('id');return True
			else:A.error_message=C;return _C
		except Exception as E:A.error_message=str(E);return _C
	def finished(A,result):
		if result and A.drawing_id:A.drawing_saved.emit(A.drawing_id);QgsMessageLog.logMessage(f"Drawing saved successfully (ID: {A.drawing_id})",_B,Qgis.Info)
		else:QgsMessageLog.logMessage(f"Failed to save drawing: {A.error_message}",_B,Qgis.Critical)
class UpdateDrawingTask(QgsTask):
	drawing_updated=pyqtSignal(int)
	def __init__(A,api_client,drawing_id,points=_A,attributes=_A):super().__init__('Updating drawing via API',QgsTask.CanCancel);A.api_client=api_client;A.drawing_id=drawing_id;A.points=points;A.attributes=attributes;A.error_message=_A
	def run(A):
		try:
			B={}
			if A.points is not _A:B[_D]=A.points
			if A.attributes is not _A:B[_E]=A.attributes
			C,D=A.api_client.update_drawing(A.drawing_id,B)
			if not C:A.error_message=D
			return C
		except Exception as E:A.error_message=str(E);return _C
	def finished(A,result):
		if result:A.drawing_updated.emit(A.drawing_id);QgsMessageLog.logMessage(f"Drawing updated successfully (ID: {A.drawing_id})",_B,Qgis.Info)
		else:QgsMessageLog.logMessage(f"Failed to update drawing: {A.error_message}",_B,Qgis.Critical)
class DeleteDrawingTask(QgsTask):
	drawing_deleted=pyqtSignal(int)
	def __init__(A,api_client,drawing_id):super().__init__('Deleting drawing via API',QgsTask.CanCancel);A.api_client=api_client;A.drawing_id=drawing_id;A.error_message=_A
	def run(A):
		try:
			B,C=A.api_client.delete_drawing(A.drawing_id)
			if not B:A.error_message=C
			return B
		except Exception as D:A.error_message=str(D);return _C
	def finished(A,result):
		if result:A.drawing_deleted.emit(A.drawing_id);QgsMessageLog.logMessage(f"Drawing deleted successfully (ID: {A.drawing_id})",_B,Qgis.Info)
		else:QgsMessageLog.logMessage(f"Failed to delete drawing: {A.error_message}",_B,Qgis.Critical)