_H='file_name'
_G='longitude'
_F='latitude'
_E='id'
_D='layer_name'
_C=None
_B='save_folder'
_A=False
import json
from qgis.core import QgsFeature,QgsField,QgsGeometry,QgsPointXY,QgsVectorLayer
from qgis.PyQt.QtCore import QVariant
from..constants.color import DEFAULT_MARKER_COLOR
from..mixins import StyleMixin,ProjectMixin
from..api_client import APIClient
class TracklogLoader(StyleMixin,ProjectMixin):
	def __init__(A,api_client=_C):A.api_client=api_client or APIClient()
	def create_tracklog_layer(S,data,layer_name=_C,latitude=_F,longitude=_G,image_link=_H,layer_suffix=_C,color=DEFAULT_MARKER_COLOR):
		N=layer_suffix;M=layer_name;J=image_link;I=longitude;H=latitude;E=data
		if N:M=f"{N}"
		if not E:return _A,'No data to load'
		try:
			A=QgsVectorLayer('Point?crs=EPSG:4326',M,'memory');T=A.dataProvider();G=[QgsField('coordinate_id',QVariant.Int),QgsField(_F,QVariant.Double),QgsField(_G,QVariant.Double),QgsField('image_url',QVariant.String),QgsField(_B,QVariant.String),QgsField(_D,QVariant.String)]
			if E:
				O=E[0]
				for C in O.keys():
					if C not in[H,I,J,_E,_B,_D]:
						B=O[C]
						if isinstance(B,int):G.append(QgsField(C,QVariant.Int))
						elif isinstance(B,float):G.append(QgsField(C,QVariant.Double))
						else:G.append(QgsField(C,QVariant.String))
			T.addAttributes(G);A.updateFields();K=[];U=0
			for(V,D)in enumerate(E):
				try:
					P=float(D[H]);Q=float(D[I]);W=QgsPointXY(Q,P);X=QgsGeometry.fromPointXY(W);L=QgsFeature(A.fields());L.setGeometry(X);F=[D.get(_E,V+1),P,Q,str(D.get(J,'')),str(D.get(_B,'')),str(D.get(_D,''))]
					for C in D.keys():
						if C not in[H,I,J,_E,_B,_D]:
							B=D[C]
							if B is _C or str(B).upper()=='NULL':F.append(_C)
							elif isinstance(B,list):F.append(json.dumps(B)if B else _C)
							elif isinstance(B,dict):F.append(json.dumps(B))
							else:F.append(B)
					L.setAttributes(F);K.append(L)
				except(ValueError,KeyError)as R:U+=1;continue
			if not K:Y=f"All {len(E)} records were skipped due to errors. Check the data format.";return _A,Y
			if not A.isEditable():A.startEditing()
			b,c=A.dataProvider().addFeatures(K)
			if A.isEditable():
				Z=A.commitChanges()
				if not Z:a=A.commitErrors();return _A,f"Failed to commit features: {'; '.join(a)}"
			A.updateExtents()
			if A.featureCount()==0:return _A,'Features were not added to layer (unknown error)'
			S.apply_custom_style(A,color);return True,A
		except Exception as R:return _A,f"Failed to create layer: {str(R)}"
	def load_tracklog_layer(G,user_id,dataset_ids=_C):
		C='name'
		if user_id is _C:return _A,'User ID is required'
		N,K=G.api_client.get_datasets();L={}
		if N and K:
			for D in K:A=D.get(_E);O=D.get(C,f"Dataset {A}");L[A]={C:O,_B:D.get(_B,D.get(C,''))}
		H,I=G.api_client.get_tracklog(dataset_ids=dataset_ids)
		if not H:return _A,f"Failed to get tracklog: {I}"
		if not I:return _A,'No data found in the specified table'
		E={}
		for(R,F)in enumerate(I):
			A=F.get('dataset_id');M=L.get(A,{C:f"Dataset {A}"if A else'Unknown',_B:''});B=M[C];F[_D]=B;F[_B]=M[_B]
			if B not in E:E[B]=[]
			E[B].append(F)
		J=[]
		for(S,(B,P))in enumerate(E.items()):
			H,Q=G.create_tracklog_layer(data=P,latitude=_F,longitude=_G,image_link=_H,layer_suffix=B,color=DEFAULT_MARKER_COLOR)
			if H:J.append(Q)
		if not J:return _A,'Failed to create any layers'
		return True,J