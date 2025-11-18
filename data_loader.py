from.services import DrawingService,TracklogLoader
class DataLoader:
	def __init__(A,api_client):B=api_client;A.api_client=B;A._tracklog_loader=TracklogLoader(B);A._drawing_loader=DrawingService(B)
	def load_tracklog_layer(A,*B,**C):return A._tracklog_loader.load_tracklog_layer(*B,**C)
	def load_drawing_layers(A,*B,**C):return A._drawing_loader.load_drawing_layers(*B,**C)
	def add_layer_to_project(A,*B,**C):return A._tracklog_loader.add_layer_to_project(*B,**C)
	def add_layers_as_group(A,*B,**C):return A._tracklog_loader.add_layers_as_group(*B,**C)