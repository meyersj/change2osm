from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement

from xml.dom import minidom
from xml.dom.minidom import parseString

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")


document = ElementTree.parse( 'P://osm/map.osm' )

print prettify(document)

#osm = document.find('osm')
bound = document.find('bound')

#print bound.attrib['minlat']


osm = Element( 'osm', version="0.6",
                      generator="CGImap 0.2.0",
                      copyright="OpenStreetMap and contributors",
                      attribution="http://www.openstreetmap.org/copyright",
                      license="http://opendatacommons.org/licenses/odbl/1-0/")

# <membership><users/>
bounds = SubElement( osm, 'bounds')

# <membership><users><user/>
SubElement( osm, 'id', v='1' )
SubElement( osm, 'id', v='2' )
SubElement( osm, 'id', v='2' )

print prettify(osm)

print "\n\n\n\n"

print osm

output_file = open( "P://osm/test2.osm", 'w' )
output_file.write( prettify(osm) )
output_file.close()


#<bounds minlat="45.5200000" minlon="-122.6750000" maxlat="45.5250000" maxlon="-122.6700000"/>

