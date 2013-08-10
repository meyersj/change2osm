import urllib2

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



changesets = urllib2.urlopen('http://api.openstreetmap.org/api/0.6/changesets?bbox=-122.675,45.520,-122.670,45.525?time=2013-04-00T00:00:00Z')


osm = urllib2.urlopen('http://api.openstreetmap.org/api/0.6/map?bbox=-122.675,45.520,-122.670,45.525')



changesets = ElementTree.parse(changesets)
osm = ElementTree.parse(osm)

#print document

root = changesets.getroot()


print root.tag
print root.attrib


changesets = []


for child in root:
  #print child.tag
 

  if(child.tag == 'changeset'): 
    #print child.attrib
    date = child.attrib['created_at'].split('-')

 
    if(int(date[0]) >= 2013 and int(date[1]) >= 4):
      #print child.attrib['user'] + " " + child.attrib['created_at']
      changesets.append(child.attrib['id'])



#for item in changesets:
#  print item

root = osm.getroot()

for child in root:
  if(child.tag == 'node' or child.tag == 'way' or child.tag == 'relation'):
    change_id = child.attrib['changeset']
  

    found = False
    for check in changesets:
      if(check == change_id):
        found = True
        print child.tag
        print child.attrib['timestamp']

    if(found == False):
      root.remove(child)
        #print "Match"
        #print changeset + " " + change
        #print child.attrib['user']

  #print child.tag

print root.tag
print root.attrib

osm.write('/home/jeff/trimet/create.osm')
#output_file = open('/home/jeff/trimet/create.osm', 'w' )
#output_file.write(osm)
#output_file.close()



#osm = document.find('osm')
#bound = document.find('bound')

#print bound.attrib['minlat']


#osm = Element( 'osm', version="0.6",
#                      generator="CGImap 0.2.0",
#                      copyright="OpenStreetMap and contributors",
#                      attribution="http://www.openstreetmap.org/copyright",
#                      license="http://opendatacommons.org/licenses/odbl/1-0/")




"""
# <membership><users/>
bounds = SubElement( osm, 'bounds')

# <membership><users><user/>
SubElement( osm, 'id', v='1' )
SubElement( osm, 'id', v='2' )
SubElement( osm, 'id', v='2' )

print prettify(osm)

print "\n\n\n\n"

print osm

output_file = open( "home/jeff/trimet/osm/create.osm", 'w' )
output_file.write( prettify(osm) )
output_file.close()


#<bounds minlat="45.5200000" minlon="-122.6750000" maxlat="45.5250000" maxlon="-122.6700000"/>
"""
