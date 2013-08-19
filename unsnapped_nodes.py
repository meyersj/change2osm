import urllib2
from decimal import Decimal
from xml.etree import ElementTree
from xml.etree.ElementTree import Element

#------------------------------------------
#required paramters
#bounding box
left = '-122.65'
bottom = '45.49'
right = '-122.64'
top = '45.5'

#date (inclusive)
year = 2013
month = 4

#tolerance for how close nodes need to be
tolerance = 0.000005 

#out_file = 'P://osm/output/modified_close.osm'
#orig_file = 'P://osm/output/orig_close.osm'
out_file = '/home/jeff/trimet/modified_close.osm'
orig_file = '/home/jeff/trimet/orig_close.osm'

#------------------------------------------

#download osm file from openstreetmap using bounding box paramters
url = 'http://overpass-api.de/api/map?bbox=' + left + "," + bottom + "," + right + "," + top
#url = 'http://api.openstreetmap.org/api/0.6/map?bbox=' + left + "," + bottom + "," + right + "," + top


def New_Tree(root):
   new_root = Element('osm')
   new_root.set('version', root.attrib['version'])
   new_root.append(root.find('bounds'))
   new_root.append(Element('ERROR'))
   return ElementTree.ElementTree(new_root)


try:
    print "downloading area"
    print "left: " + left
    print "bottom: " + bottom
    print "right: " + right
    print "top: " + top

    osm_file = urllib2.urlopen(url)
    #osm_file = open('P://osm/output/modified2.osm')
    #parse downloaded osm file into element tree
    osm_tree = ElementTree.parse(osm_file)

    #insert id for features with timestamp after specified date into correct list
    root = osm_tree.getroot()
    
    #remove extra tags from overpass api
    child = root.find('note')
    root.remove(child)
    child = root.find('meta')
    root.remove(child)

    #write out original recieved file
    osm_tree.write(orig_file)


    nodes = []

    print "locating all nodes"
    for child in root.iter('node'): 
        item = {'id':child.attrib['id'], \
                'lat':child.attrib['lat'], \
                'lon':child.attrib['lon']}
        nodes.append(item)    


    new_tree = New_Tree(root)
    new_root = new_tree.getroot()
    print "checking for unsnapped nodes"
    for node in nodes:
        #print "lat: " + str(node['lat']) + "/lon: " + str(node['lon'])

        for child in root.iter('node'):

            lon_diff = abs(float(child.attrib['lon']) - float(node['lon']))
            lat_diff = abs(float(child.attrib['lat']) - float(node['lat']))

            if(lat_diff == 0 and lon_diff == 0):
                if(node['id'] != child.attrib['id']):
                    child.append(Element('tag', {'k': 'close', 'v': 'unsnapped'}))
                    new_root.append(child)
            elif(lat_diff < tolerance and lon_diff < tolerance):
                child.append(Element('tag', {'k': 'close', 'v': 'true'}))
                new_root.append(child)





    #write out modified osm file
    print "writing file to " + out_file
    new_tree.write(out_file)

except urllib2.HTTPError, e:
    print e
    print "Invalid Bounding Box?"
except urllib2.URLError, e:
    print e




