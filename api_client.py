_I='/drawings'
_H='DELETE'
_G='/layers'
_F='POST'
_E=False
_D=None
_C='data'
_B='GET'
_A=True
import json,os
from typing import Any,Dict,List,Optional,Tuple
from urllib import error,request
from urllib.parse import urlencode
from qgis.core import QgsSettings
from.constants.host import DEFAULT_HOST
class APIClient:
	SETTINGS_KEY_API_BASE_URL='ard360/api_base_url';SETTINGS_KEY_JWT_TOKEN='ard360/jwt_token';DEFAULT_API_BASE_URL=f"{DEFAULT_HOST}/api"
	def __init__(A):A.settings=QgsSettings();A.base_url=A.get_base_url();A.jwt_token=A.get_jwt_token()
	def get_base_url(B):
		E=os.path.dirname(__file__);D=os.path.join(E,'.env')
		if os.path.exists(D):
			try:
				with open(D,'r')as F:
					for A in F:
						A=A.strip()
						if A.startswith('API_BASE_URL='):C=A.split('=',1)[1].strip();C=C.strip('"').strip("'");return C
			except Exception:pass
		return B.settings.value(B.SETTINGS_KEY_API_BASE_URL,B.DEFAULT_API_BASE_URL)
	def set_base_url(A,url):A.base_url=url;A.settings.setValue(A.SETTINGS_KEY_API_BASE_URL,url)
	def get_jwt_token(A):return A.settings.value(A.SETTINGS_KEY_JWT_TOKEN,_D)
	def set_jwt_token(A,token):
		B=token;A.jwt_token=B
		if B:A.settings.setValue(A.SETTINGS_KEY_JWT_TOKEN,B)
		else:A.settings.remove(A.SETTINGS_KEY_JWT_TOKEN)
	def clear_token(A):A.set_jwt_token(_D)
	def _make_request(C,endpoint,method=_B,data=_D,params=_D,require_auth=_A):
		L='error';K='success';H=params;G=method;F='utf-8'
		try:
			E=f"{C.base_url}{endpoint}"
			if H and G==_B:E=f"{E}?{urlencode(H)}"
			D=request.Request(E,method=G)
			if require_auth:
				if not C.jwt_token:return _E,'No authentication token available. Please login.'
				D.add_header('Authorization',f"Bearer {C.jwt_token}")
			if data is not _D:D.add_header('Content-Type','application/json');M=json.dumps(data).encode(F);D.data=M
			with request.urlopen(D)as N:
				I=N.read().decode(F);B=json.loads(I)if I else{}
				if isinstance(B,dict)and K in B:
					if B[K]:return _A,B.get(_C,B)
					else:return _E,B.get(L,'Unknown error')
				return _A,B
		except error.HTTPError as A:
			try:O=json.loads(A.read().decode(F));J=O.get(L,str(A))
			except Exception:J=f"HTTP {A.code}: {A.reason}"
			if A.code==401:C.clear_token();return _E,'Authentication failed. Please login again.'
			return _E,J
		except error.URLError as A:return _E,f"Network error: {str(A.reason)}"
		except Exception as A:return _E,f"Request failed: {str(A)}"
	def authenticate(B,username,password):
		C='token';D,A=B._make_request('/users/authenticate',method=_F,data={'username':username,'password':password},require_auth=_E)
		if D:
			if C in A:B.set_jwt_token(A[C])
			return _A,A
		return _E,A
	def verify_token(B):
		C,A=B._make_request('/users/verify',method=_B)
		if C and isinstance(A,dict)and A.get('valid'):return _A,A.get('user',{})
		return _E,'Token invalid or expired'
	def get_current_user(A):return A._make_request('/users/me',method=_B)
	def get_datasets(C):
		B,A=C._make_request('/datasets',method=_B)
		if B:
			if isinstance(A,list):return _A,A
			elif isinstance(A,dict)and _C in A:return _A,A[_C]
		return B,A
	def get_dataset(A,dataset_id):return A._make_request(f"/datasets/{dataset_id}",method=_B)
	def get_tracklog(F,dataset_ids=_D,limit=_D):
		D=limit;C=dataset_ids;B={}
		if C:B['dataset_ids']=','.join(map(str,C))
		if D:B['limit']=D
		E,A=F._make_request('/coordinates/tracklog',method=_B,params=B)
		if E:
			if isinstance(A,list):return _A,A
			elif isinstance(A,dict)and _C in A:return _A,A[_C]
		return E,A
	def get_layers(C):
		B,A=C._make_request(_G,method=_B)
		if B:
			if isinstance(A,list):return _A,A
			elif isinstance(A,dict)and _C in A:return _A,A[_C]
		return B,A
	def get_layer(A,layer_id):return A._make_request(f"/layers/{layer_id}",method=_B)
	def create_layer(A,layer_data):return A._make_request(_G,method=_F,data=layer_data)
	def update_layer(A,layer_id,layer_data):return A._make_request(f"/layers/{layer_id}",method='PATCH',data=layer_data)
	def delete_layer(A,layer_id):return A._make_request(f"/layers/{layer_id}",method=_H)
	def get_layer_template(A,layer_id):return A._make_request(f"/layers/{layer_id}/template",method=_B)
	def get_drawings(E,layer_id=_D):
		B=layer_id;C={}
		if B is not _D:C['layer_id']=B
		D,A=E._make_request(_I,method=_B,params=C)
		if D:
			if isinstance(A,list):return _A,A
			elif isinstance(A,dict)and _C in A:return _A,A[_C]
		return D,A
	def get_drawing(A,drawing_id):return A._make_request(f"/drawings/{drawing_id}",method=_B)
	def get_drawings_by_layer(C,layer_id):
		B,A=C._make_request(f"/drawings/layer/{layer_id}",method=_B)
		if B:
			if isinstance(A,list):return _A,A
			elif isinstance(A,dict)and _C in A:return _A,A[_C]
		return B,A
	def create_drawing(A,drawing_data):return A._make_request(_I,method=_F,data=drawing_data)
	def update_drawing(A,drawing_id,drawing_data):return A._make_request(f"/drawings/{drawing_id}",method='PATCH',data=drawing_data)
	def delete_drawing(A,drawing_id):return A._make_request(f"/drawings/{drawing_id}",method=_H)