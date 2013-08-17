import urllib2
from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from datetime import datetime
#------------------------------------------

#required paramters
#bounding box
left = -122.62
bottom = 45.50
right = -122.60
top = 45.52

#date (inclusive)
year = 2013
month = 4

#out_file = 'P://osm/output/modified_5hund.osm'
#orig_file = 'P://osm/output/orig_5hun.osm'
out_file = '/home/jeff/trimet/modified.osm'
orig_file = '/home/jeff/trimet/orig.osm'

#------------------------------------------

#out_file = 'P://osm/output/modifie.osm'
#orig_file = 'P://osm/output/orig.osm'

start = datetime.now()
print start 

#download osm file from openstreetmap using bounding box paramters
url = 'http://overpass-api.de/api/map?bbox=' + str(left) + "," + str(bottom) + "," + str(right) + "," + str(top)
#url = 'http://api.openstreetmap.org/api/0.6/map?bbox=' + left + "," + bottom + "," + right + "," + top

try:
    print "downloading area"
    print "left: " + str(left)
    print "bottom: " + str(bottom)
    print "right: " + str(right)
    print "top: " + str(top)

    osm_file = urllib2.urlopen(url)

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

    #create empty list to ids for required features
    recent_relations = []
    recent_nodes = []
    required_nodes = []
    required_ways = []
    remove_nodes = []

    highway_nodes = []
        
    #select out only ways with a highway tag
    print "removing ways without highway tag"
    for child in root.findall('way'):

        highway = False
        for sub_element in child.iter('tag'):
            if(sub_element.attrib['k'] == 'highway'):
                highway = True
        if(highway == True):
            for sub_element in child.iter('nd'):
                highway_nodes.append(sub_element.attrib['ref'])
            if(child.attrib['id'] == '5532397'):
                print "found fucker"

            date = child.attrib['timestamp'].split('-')
            if(int(date[0]) >= year and int(date[1]) >= month):
                required_ways.append(child.attrib['id'])
                child.append(Element('tag', {'k': 'recent', 'v': 'true'}))
                for sub_element in child.iter('nd'):
                    required_nodes.append(sub_element.attrib['ref'])
            else:
                child.append(Element('tag', {'k': 'recent', 'v': 'false'}))
                #root.remove(child)
    

	#select all nodes with a recent timestamp
    print "searching for recent nodes"
    for child in root.findall('node'):

        if(child.attrib['id'] not in highway_nodes):
            root.remove(child)
        else:
            date = child.attrib['timestamp'].split('-')
            if(int(date[0]) >= year and int(date[1]) >= month):
                recent_nodes.append(child.attrib['id'])
                child.append(Element('tag', {'k': 'recent', 'v': 'true'}))
            else:
                child.append(Element('tag', {'k': 'recent', 'v': 'false'}))	

    #go back and search for ways containing recent nodes
    print "searching for ways with recent nodes"
    for child in root.findall('way'):
    
        for node in recent_nodes:
            if(child.attrib['id'] == '5532397'):
                print "found fucker"
            for sub_element in child.iter('nd'):
                if(node == sub_element.attrib['ref']):
                    required_ways.append(child.attrib['id'])

    #remove duplicates from list
    required_nodes = list(set(required_nodes))
    required_ways = list(set(required_ways))
    recent_nodes = list(set(recent_nodes))
    #remove any elements from osm file that are not needed
    #search for matching feature in correct required list for match
    #if there is no match remove feature from element tree
    print "removing non required nodes"
    for child in root.findall('node'):

        if(child.attrib['id'] not in required_nodes):
            root.remove(child)

    print "removing non required ways"
    for child in root.findall('way'):

        if(child.attrib['id'] not in required_ways):
            root.remove(child)

    print "removing relations"
    for child in root.findall('relation'):
        root.remove(child)

    #write out modified osm file
    print "writing file to " + out_file
    osm_tree.write(out_file)
    
except urllib2.HTTPError, e:
    print e
    print "Invalid Bounding Box?"
except urllib2.URLError, e:
    print e


finish = datetime.now()
print finish

diff = finish - start
print diff
