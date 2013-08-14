import urllib2

from xml.etree import ElementTree
from xml.etree.ElementTree import Element
#from xml.etree.ElementTree import SubElement

#*paramters*
#bounding box

"""
#test area
left = '-122.675'
bottom = '45.520'
right = '-122.670'
top = '45.525'
"""

#larger portland core
left = '-122.71'
bottom = '45.50'
right = '-122.70'
top = '45.51'

#date
year = 2013
month = 4
#url = 'http://api.openstreetmap.org/api/0.6/map?bbox=' + left + "," + bottom + "," + right + "," + top

out_file = '/home/jeff/osm/modified.osm'
orig_file = '/home/jeff/osm/orig.osm'
#out_file = 'P://osm/modified.osm'
#orig_file = 'P://osm/orig.osm'




url = 'http://overpass-api.de/api/map?bbox=' + left + "," + bottom + "," + right + "," + top

print url

#download osm file from openstreetmap using bounding box paramters
osm_file = urllib2.urlopen(str(url))


#parse downloaded osm file into element tree
osm_tree = ElementTree.parse(osm_file)

#write out original recieved file
osm_tree.write(orig_file)

#create empty list to store ids for recently modified features
recent_nodes = []
recent_ways = []
recent_relations = []

#create empty list for nodes that will be required
required_nodes = []
required_ways = []

#insert id for features with timestamp after specified date into correct list
root = osm_tree.getroot()

for child in root.findall('node'):

    date = child.attrib['timestamp'].split('-')
    if(int(date[0]) >= year and int(date[1]) >= month):
        required_nodes.append(child.attrib['id'])
        child.append(Element('tag', {'k': 'recent', 'v': 'true'}))


#go back and add search for the way containing the updated 
for child in root.findall('way'):

    for node in required_nodes:
            for sub_element in child.iter('nd'):
                if(node == sub_element.attrib['ref']):
                    required_ways.append(child.attrib['id'])

for child in root.findall('way'):

    #recent ways
    date = child.attrib['timestamp'].split('-')
    if(int(date[0]) >= year and int(date[1]) >= month):
        required_ways.append(child.attrib['id'])
        child.append(Element('tag', {'k': 'recent', 'v': 'true'}))
            
            #add all nodes from recent way to required_nodes list
        for sub_element in child.iter('nd'):
            required_nodes.append(sub_element.attrib['ref'])
          
for child in root.findall('relation'):

    #recent relations
    date = child.attrib['timestamp'].split('-')
    if(int(date[0]) >= year and int(date[1]) >= month):
        recent_relations.append(child.attrib['id'])
        child.append(Element('tag', {'k': 'recent', 'v': 'true'}))

        #add all nodes from recent way to required_nodes list
        for sub_element in child.iter('member'):
            if(sub_element.attrib['type'] == 'node'):
                required_nodes.append(sub_element.attrib['ref'])
            if(sub_element.attrib['type'] == 'way'):
                required_ways.append(sub_element.attrib['ref'])



#go back and add any nodes still needed from ways added to required_ways from recent_relations
for child in root.findall('way'):

    for way in required_ways:
        if(child.attrib['id'] == way):
            for sub_element in child.iter('nd'):
                required_nodes.append(sub_element.attrib['ref'])


#remove duplicates from list
required_nodes = list(set(required_nodes))
required_ways = list(set(required_ways))


#remove any elements from osm file that are not needed
#search for matching feature in correct required list for match
#if there is no match remove feature from element tree
for child in root.findall('node'):
    #node
    #print child.tag + " - " + child.attrib['id']
    found = False
    for node in required_nodes:
        if(node == child.attrib['id']):
            found = True

    if(found == False):
        root.remove(child)


for child in root.findall('way'):
    #way
    found = False
    for node in required_ways:
        if(node == child.attrib['id']):
            found = True

    if(found == False):
        root.remove(child)


for child in root.findall('relation'):
    #relation
    #root.remove(child)

        found = False
        for node in recent_relations:
            if(node == child.attrib['id']):
                found == True

        if(found == False):
           root.remove(child)


#write out modified osm file
osm_tree.write(out_file)


