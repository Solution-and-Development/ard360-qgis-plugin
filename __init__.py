import sys,os
plugin_dir=os.path.dirname(__file__)
vendor_dir=os.path.join(plugin_dir,'vendor')
if vendor_dir not in sys.path:sys.path.insert(0,vendor_dir)
from.main import ArdPlugin
def classFactory(iface):return ArdPlugin(iface)