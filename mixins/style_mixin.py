_A='color'
from qgis.core import QgsFillSymbol,QgsLineSymbol,QgsMarkerSymbol,QgsSingleSymbolRenderer
from..constants.color import DEFAULT_DRAWING_COLOR
class StyleMixin:
	def apply_custom_style(E,layer,color=DEFAULT_DRAWING_COLOR):
		A=layer
		try:B=QgsMarkerSymbol.createSimple({'name':'circle',_A:color,'size':'3'});C=QgsSingleSymbolRenderer(B);A.setRenderer(C);A.triggerRepaint()
		except Exception as D:print(f"Failed to apply custom style: {str(D)}")
	def apply_line_style(F,layer,color=DEFAULT_DRAWING_COLOR):
		B='round';A=layer
		try:C=QgsLineSymbol.createSimple({_A:color,'width':'2','capstyle':B,'joinstyle':B});D=QgsSingleSymbolRenderer(C);A.setRenderer(D);A.triggerRepaint()
		except Exception as E:print(f"Failed to apply line style: {str(E)}")
	def apply_polygon_style(G,layer,color=DEFAULT_DRAWING_COLOR):
		D='solid';B=color;A=layer
		try:C=QgsFillSymbol.createSimple({_A:B,'style':D,'outline_color':B,'outline_style':D,'outline_width':'0.5'});C.setOpacity(.3);E=QgsSingleSymbolRenderer(C);A.setRenderer(E);A.triggerRepaint()
		except Exception as F:print(f"Failed to apply polygon style: {str(F)}")