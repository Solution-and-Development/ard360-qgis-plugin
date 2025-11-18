_R='attributes_template'
_Q='sync_enabled'
_P='drawing_type'
_O='db_user_id'
_N='db_layer_id'
_M='drawing_id'
_L='memory'
_K='Polygons'
_J='Lines'
_I='Markers'
_H='Polygon'
_G='LineString'
_F=True
_E='Point'
_D='id'
_C=False
_B=None
_A='type'
import json
from qgis.core import QgsFeature,QgsField,QgsGeometry,QgsPointXY,QgsVectorLayer
from qgis.PyQt.QtCore import QVariant
from..constants.drawing_types import DRAWING_LINE,DRAWING_POLYGON,HEIGHT,LINE,MARKER,POLYGON
from..constants.qgis_layer_type import LINE_STRING_LAYER,POINT_LAYER,POLYGON_LAYER
from..mixins import StyleMixin,ProjectMixin
from..api_client import APIClient
class DrawingService(StyleMixin,ProjectMixin):
	def __init__(A,api_client=_B):A.api_client=api_client or APIClient()
	def create_drawing_layer(H,drawings,layer_name,color,geometry_type=_E,db_layer_id=_B,db_user_id=_B,drawing_type=_B,custom_fields=_B):
		Y='unknown';U=drawing_type;T=db_user_id;S=db_layer_id;R=drawings;Q='lat';P='lng';I=color;G=custom_fields;F=geometry_type
		if not R:return _C,'No drawings to load'
		try:
			A=QgsVectorLayer(f"{F}?crs=EPSG:4326",layer_name,_L);Z=A.dataProvider();V=[QgsField(_M,QVariant.Int),QgsField(_A,QVariant.String)]
			if G:V.extend(G)
			Z.addAttributes(V);A.updateFields();J=[];K=0
			for B in R:
				try:
					L=B['points']
					if isinstance(L,str):C=json.loads(L)
					else:C=L
					if B[_A].lower()in[MARKER,HEIGHT]and len(C)>0:W=C[0];a=QgsPointXY(float(W[P]),float(W[Q]));M=QgsGeometry.fromPointXY(a)
					elif B[_A].lower()in[LINE,DRAWING_LINE]and len(C)>1:D=[QgsPointXY(float(A[P]),float(A[Q]))for A in C];M=QgsGeometry.fromPolylineXY(D)
					elif B[_A].lower()in[POLYGON,DRAWING_POLYGON]and len(C)>=3:
						D=[QgsPointXY(float(A[P]),float(A[Q]))for A in C]
						if D[0]!=D[-1]:D.append(D[0])
						M=QgsGeometry.fromPolygonXY([D])
					else:K+=1;print(f"[Drawing Debug] Skipped drawing {B.get(_D,Y)}: type='{B[_A]}', points={len(C)} (invalid for {F})");continue
					N=QgsFeature(A.fields());N.setGeometry(M);X=[B[_D],B[_A]];E=B.get('attributes',{})
					if G and E is not _B:
						if isinstance(E,str):E=json.loads(E)if E else{}
						for b in G:c=b.name();X.append(E.get(c))
					N.setAttributes(X);J.append(N)
				except(ValueError,KeyError,json.JSONDecodeError)as O:K+=1;print(f"[Drawing Debug] ERROR processing drawing {B.get(_D,Y)}: {str(O)}");continue
			if not J:return _C,f"No valid geometries created (skipped {K})"
			A.startEditing();A.addFeatures(J);A.commitChanges();A.updateExtents()
			if F==_E:H.apply_custom_style(A,I)
			elif F==_G:H.apply_line_style(A,I)
			elif F==_H:H.apply_polygon_style(A,I)
			if S is not _B:A.setCustomProperty(_N,S)
			if T is not _B:A.setCustomProperty(_O,T)
			if U is not _B:A.setCustomProperty(_P,U);A.setCustomProperty(_Q,_F)
			return _F,A
		except Exception as O:return _C,f"Failed to create drawing layer: {str(O)}"
	def load_drawing_layers(B,user_id,layer_ids=_B):
		O=layer_ids;F=user_id
		if F is _B:return _C,'User ID is required'
		A,I=B.api_client.get_layers()
		if not A:return _C,f"Failed to get layers: {I}"
		if not I:return _C,'No layers found for this user'
		if O:
			I=[A for A in I if A[_D]in O]
			if not I:return _C,'No matching layers found'
		N=[]
		for J in I:
			C=J[_D];V=J['name'];H=J['color'];P=J.get(_R)or J.get('attributesTemplate');G=[]
			if P:G=B.parse_attributes_template(P)
			A,D=B.api_client.get_drawings_by_layer(C)
			if not A:print(f"[Drawing Debug] ERROR: Failed to get drawings for layer {C}: {D}");continue
			Q=[A for A in D if A[_A].lower()==MARKER]if D else[];R=[A for A in D if A[_A].lower()in[LINE,DRAWING_LINE]]if D else[];S=[A for A in D if A[_A].lower()in[POLYGON,DRAWING_LINE]]if D else[];T=[A for A in D if A[_A].lower()==HEIGHT]if D else[];E=[]
			if not D:print(f"[Drawing Debug] Creating empty layer group for layer {C}");K=B._create_single_empty_layer(_I,_E,H,C,F,MARKER,G);E.append(K);L=B._create_single_empty_layer(_J,_G,H,C,F,LINE,G);E.append(L);M=B._create_single_empty_layer(_K,_H,H,C,F,POLYGON,G);E.append(M)
			else:
				if Q:
					A,K=B.create_drawing_layer(Q,_I,H,_E,db_layer_id=C,db_user_id=F,drawing_type=MARKER,custom_fields=G)
					if A:E.append(K)
					else:print(f"[Drawing Debug] ✗ FAILED to create marker layer: {K}")
				if R:
					A,L=B.create_drawing_layer(R,_J,H,_G,db_layer_id=C,db_user_id=F,drawing_type=LINE,custom_fields=G)
					if A:E.append(L)
					else:print(f"[Drawing Debug] ✗ FAILED to create line layer: {L}")
				if S:
					A,M=B.create_drawing_layer(S,_K,H,_H,db_layer_id=C,db_user_id=F,drawing_type=POLYGON,custom_fields=G)
					if A:E.append(M)
					else:print(f"[Drawing Debug] ✗ FAILED to create polygon layer: {M}")
			if T:
				A,U=B.create_drawing_layer(T,'Heights',H,_E,db_layer_id=C,db_user_id=F,drawing_type=HEIGHT,custom_fields=G)
				if A:E.append(U)
				else:print(f"[Drawing Debug] ✗ FAILED to create height layer: {U}")
			if E:N.append((V,E))
		if not N:return _C,'No valid layers created from drawings'
		return _F,N
	def create_empty_layer_group(A,layer_data):
		B=layer_data;E=B[_D];F=B['color'];G=B['user_id'];H=B.get(_R);C=[]
		if H:C=A.parse_attributes_template(H)
		D=[]
		try:I=A._create_single_empty_layer(_I,POINT_LAYER,F,E,G,MARKER,C);D.append(I);J=A._create_single_empty_layer(_J,LINE_STRING_LAYER,F,E,G,LINE,C);D.append(J);K=A._create_single_empty_layer(_K,POLYGON_LAYER,F,E,G,POLYGON,C);D.append(K);return _F,D
		except Exception as L:return _C,f"Failed to create layer group: {str(L)}"
	def _create_single_empty_layer(C,layer_name,geometry_type,color,db_layer_id,user_id,drawing_type,custom_fields):
		D=color;B=geometry_type;A=QgsVectorLayer(f"{B}?crs=EPSG:4326",layer_name,_L);F=A.dataProvider();E=[QgsField(_M,QVariant.Int),QgsField(_A,QVariant.String)];E.extend(custom_fields);F.addAttributes(E);A.updateFields();A.setCustomProperty(_N,db_layer_id);A.setCustomProperty(_O,user_id);A.setCustomProperty(_P,drawing_type);A.setCustomProperty(_Q,_F)
		if B==POINT_LAYER:C.apply_custom_style(A,D)
		elif B==LINE_STRING_LAYER:C.apply_line_style(A,D)
		elif B==POLYGON_LAYER:C.apply_polygon_style(A,D)
		return A
	def parse_attributes_template(J,template):
		A=template;B=[]
		if isinstance(A,str):
			try:C=json.loads(A)
			except json.JSONDecodeError:print('[Drawing Service] WARNING: Invalid attributes_template JSON');return B
		else:C=A
		F=C.get('fields',[]);G={'text':QVariant.String,'number':QVariant.Int,'date':QVariant.Date,'dropdown':QVariant.String}
		for D in F:
			E=D.get('key');H=D.get(_A,'string')
			if not E:continue
			I=G.get(H,QVariant.String);B.append(QgsField(E,I))
		return B