import urllib2
from xml.etree import ElementTree
from xml.etree.ElementTree import Element

#------------------------------------------
#required paramters
#bounding box
left = '-122.66'
bottom = '45.51'
right = '-122.63'
top = '45.54'

#date (inclusive)
year = 2013
month = 4

#out_file = 'P://osm/modified.osm'
#orig_file = 'P://osm/orig.osm'
out_file = '/home/jeff/trimet/modified_over7.osm'
orig_file = '/home/jeff/trimet/orig_over7.osm'

#------------------------------------------

#download osm file from openstreetmap using bounding box paramters
url = 'http://overpass-api.de/api/map?bbox=' + left + "," + bottom + "," + right + "," + top
#url = 'http://api.openstreetmap.org/api/0.6/map?bbox=' + left + "," + bottom + "," + right + "," + top

try:
    print "downloading area"
    print "left: " + left
    print "bottom: " + bottom
    print "right: " + right
    print "top: " + top

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
    required_nodes = []
    required_ways = []
    remove_nodes = []
    
    #select out only ways with a highway tag
    print "removing ways without highway tag"
    for child in root.findall('way'):
	
	highway = False
	for sub_element in child.iter('tag'):
            if(sub_element.attrib['k'] == 'highway'):
                highway = True
        if(highway == False):
            root.remove(child)
        else:
            for sub_element in child.iter('nd'):
                required_nodes.append(sub_element.attrib['ref'])  

    required_nodes = list(set(required_nodes))

    
    #remove nodes that were not part of way with highway tag
    print "removing nodes not part of a way with highway tag"
    for child in root.findall('node'):
    
        if(child.attrib['id'] not in required_nodes):        
            root.remove(child)
    
     
    #select all nodes with a recent timestamp
    print "searching for recent nodes"
    for child in root.findall('node'):

	date = child.attrib['timestamp'].split('-')
	if(int(date[0]) >= year and int(date[1]) >= month):
	    required_nodes.append(child.attrib['id'])
	    child.append(Element('tag', {'k': 'recent', 'v': 'true'}))
    

    #go back and search for ways containing recent nodes
    print "searching for ways with recent nodes"
    for child in root.findall('way'):
	
	for node in required_nodes:
		for sub_element in child.iter('nd'):
		    if(node == sub_element.attrib['ref']):
			required_ways.append(child.attrib['id'])

    #search for recent ways
    print "searching for recent ways"
    for child in root.findall('way'):
	
	date = child.attrib['timestamp'].split('-')
	if(int(date[0]) >= year and int(date[1]) >= month):
	    required_ways.append(child.attrib['id'])
	    child.append(Element('tag', {'k': 'recent', 'v': 'true'}))
		
		#add all nodes from recent way to required_nodes list
	    for sub_element in child.iter('nd'):
		required_nodes.append(sub_element.attrib['ref'])

    
    #search for recent relations
    print "searching for recent relations"
    for child in root.findall('relation'):
        root.remove(child)
    """
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
    """

    #go back and add any nodes still needed from ways
    #added to required_ways from recent_relations
    print "searching for nodes that still need to be included"
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
    print "removing non required nodes"
    for child in root.findall('node'):

	found = False
	for node in required_nodes:
	    if(node == child.attrib['id']):
		found = True

	if(found == False):
	    root.remove(child)

    print "removing non required ways"
    for child in root.findall('way'):

	found = False
	for node in required_ways:
	    if(node == child.attrib['id']):
		found = True

	if(found == False):
	    root.remove(child)

    print "removing non required relations"
    for child in root.findall('relation'):

	    found = False
	    for node in recent_relations:
		if(node == child.attrib['id']):
		    found = True

	    if(found == False):
	       root.remove(child)

    #write out modified osm file
    print "writing file to " + out_file
    osm_tree.write(out_file)

except urllib2.HTTPError, e:
    print e
    print "Invalid Bounding Box?"
except urllib2.URLError, e:
    print e




