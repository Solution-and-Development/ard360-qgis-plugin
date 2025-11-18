_D='username'
_C=False
_B=True
_A=None
from qgis.core import QgsSettings
class AuthStorage:
	SETTINGS_KEY_JWT_TOKEN='ard360/jwt_token';SETTINGS_KEY_USER_ID='ard360/user_id';SETTINGS_KEY_USERNAME='ard360/username';SETTINGS_KEY_USER_ROLE='ard360/user_role'
	@staticmethod
	def save_session(jwt_token,user_data):
		B=user_data
		try:A=QgsSettings();A.setValue(AuthStorage.SETTINGS_KEY_JWT_TOKEN,jwt_token);A.setValue(AuthStorage.SETTINGS_KEY_USER_ID,B.get('id'));A.setValue(AuthStorage.SETTINGS_KEY_USERNAME,B.get(_D));A.setValue(AuthStorage.SETTINGS_KEY_USER_ROLE,B.get('role'));return _B,'Session saved successfully'
		except Exception as C:return _C,f"Failed to save session: {str(C)}"
	@staticmethod
	def load_session():
		A=QgsSettings();C=A.value(AuthStorage.SETTINGS_KEY_JWT_TOKEN,_A);B=A.value(AuthStorage.SETTINGS_KEY_USER_ID,_A);D=A.value(AuthStorage.SETTINGS_KEY_USERNAME,_A);E=A.value(AuthStorage.SETTINGS_KEY_USER_ROLE,_A)
		if not C or not B:return _C,'No saved session found'
		return _B,{'jwt_token':C,'user_id':int(B)if B else _A,_D:D,'role':E}
	@staticmethod
	def clear_session():
		try:A=QgsSettings();A.remove(AuthStorage.SETTINGS_KEY_JWT_TOKEN);A.remove(AuthStorage.SETTINGS_KEY_USER_ID);A.remove(AuthStorage.SETTINGS_KEY_USERNAME);A.remove(AuthStorage.SETTINGS_KEY_USER_ROLE);return _B,'Session cleared'
		except Exception as B:return _C,f"Failed to clear session: {str(B)}"
	@staticmethod
	def has_stored_session():A=QgsSettings();B=A.value(AuthStorage.SETTINGS_KEY_JWT_TOKEN,'');C=A.value(AuthStorage.SETTINGS_KEY_USER_ID,_A);return bool(B and C)
	@staticmethod
	def get_stored_username():A=QgsSettings();return A.value(AuthStorage.SETTINGS_KEY_USERNAME,'')
	@staticmethod
	def get_jwt_token():A=QgsSettings();return A.value(AuthStorage.SETTINGS_KEY_JWT_TOKEN,_A)
	@staticmethod
	def get_user_id():B=QgsSettings();A=B.value(AuthStorage.SETTINGS_KEY_USER_ID,_A);return int(A)if A is not _A else _A
	@staticmethod
	def set_user_id(user_id):
		A=user_id;B=QgsSettings()
		if A is not _A:B.setValue(AuthStorage.SETTINGS_KEY_USER_ID,A)
		else:B.remove(AuthStorage.SETTINGS_KEY_USER_ID)
	@staticmethod
	def save_token(token,user_id,username):
		A=QgsSettings()
		try:A.setValue(AuthStorage.SETTINGS_KEY_JWT_TOKEN,token);A.setValue(AuthStorage.SETTINGS_KEY_USER_ID,user_id);A.setValue(AuthStorage.SETTINGS_KEY_USERNAME,username);return _B,'Token saved successfully'
		except Exception as B:return _C,f"Failed to save token: {str(B)}"
	@staticmethod
	def get_token():B=QgsSettings();A=B.value(AuthStorage.SETTINGS_KEY_JWT_TOKEN,_A);return A if A else _A
	@staticmethod
	def clear_token():A=QgsSettings();A.remove(AuthStorage.SETTINGS_KEY_JWT_TOKEN);A.remove(AuthStorage.SETTINGS_KEY_USER_ID);A.remove(AuthStorage.SETTINGS_KEY_USERNAME);return _B,'Token cleared successfully'
	@staticmethod
	def has_token():return AuthStorage.get_token()is not _A