from qgis.core import *
import qgis.utils

QgsApplication.setPrefixPath('/usr/share/qgis/python', True)
QgsApplication.initQgis()

ds = '/home/jeff/test_gis_data/nbo_hood.shp'

nodes = QgsVectorLayer(ds, 'nodes', 'ogr')
if not nodes.isValid():
    print "Layer failed to load!"

print "count: " + str(nodes.featureCount())
