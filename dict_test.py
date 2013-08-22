import urllib2
from datetime import datetime
try:
    from xml.etree import cElementTree as ElementTree
    from xml.etree.cElementTree import Element 
except ImportError:
    from xml.etree import ElementTree
    from xml.etree.ElementTree import Element
#------------------------------------------

#required paramters
#bounding box
#left = -122.6
#bottom = 45.4
#right = -122.5
#top = 45.5

#date (inclusive)
#year = 2013
#month = 4

#out_file = 'P://osm/output/modified_5hund.osm'
#orig_file = 'P://osm/output/orig_5hun.osm'
#out_file = '/home/jeff/trimet/modified.osm'
#orig_file = '/home/jeff/trimet/orig.osm'


#------------------------------------------

#out_file = 'P://osm/output/modifie.osm'
#orig_file = 'P://osm/output/orig.osm'

start = datetime.now()
print start 

#download osm file from openstreetmap using bounding box paramters
#url = 'http://overpass-api.de/api/map?bbox=' + str(left) + "," + str(bottom) + "," + str(right) + "," + str(top)
#url = 'http://api.openstreetmap.org/api/0.6/map?bbox=' + left + "," + bottom + "," + right + "," + top


def Download(left, bottom, right, top):
    print "downloading area..."
    print "left: " + str(left)
    print "bottom: " + str(bottom)
    print "right: " + str(right)
    print "top: " + str(top)
    
    url = 'http://overpass-api.de/api/map?bbox=' + \
           str(left) + "," + \
           str(bottom) + "," + \
           str(right) + "," + \
           str(top)

    results = urllib2.urlopen(url)
    print "download complete"
    return results
   
def Parse(xml):
    return ElementTree.parse(xml)

def New_Tree(root):
   new_root = Element('osm')
   new_root.set('version', root.attrib['version'])
   new_root.append(root.find('bounds'))
   return ElementTree.ElementTree(new_root)


def Build_Dictionary(root):
    nodes = {}
    ways = {}
    relations = {}

    for child in root.findall('node'):
        nodes[child.attrib['id']] = child
        if(child.attrib['user'] == 'Grant Humphries'):
            child.append(Element('tag', {'k': 'grant', 'v': 'true'}))

    for child in root.findall('way'):
        ways[child.attrib['id']] = child
        if(child.attrib['user'] == 'Grant Humphries'):
            child.append(Element('tag', {'k': 'grant', 'v': 'true'}))

    for child in root.findall('relation'):
        relations[child.attrib['id']] = child
        if(child.attrib['user'] == 'Grant Humphries'):
            child.append(Element('tag', {'k': 'grant', 'v': 'true'}))

    return {'nodes': nodes, 'ways': ways, 'relations': relations}
   

def Highways(all_ways, from_date):
    recent_highways = []
    highway_nodes = []
    recent_highway_nodes = []
    highways = []

    for way_id, way in all_ways.items():
        highway = False
        for sub_element in way.findall('tag'):
            if(sub_element.attrib['k'] == 'highway'):
                highway = True
        
        #if way has highway tag
        #add all nodes in way to highway_nodes
        if(highway == True):
            highways.append(way_id)
            for sub_element in way.findall('nd'):
                highway_nodes.append(sub_element.attrib['ref'])

            date = way.attrib['timestamp'].split('-')
            if(int(date[0]) >= from_date[0] and int(date[1]) >= from_date[1]):
                way.append(Element('tag', {'k': 'recent_highway', 'v': 'true'}))
                recent_highways.append(way_id)
                for sub_element in way.findall('nd'):
                    recent_highway_nodes.append(sub_element.attrib['ref'])

            else:
                way.append(Element('tag', {'k': 'recent_highway', 'v': 'false'}))

    return {'recent_highways':recent_highways, \
            'highway_nodes':highway_nodes, \
            'recent_highway_nodes':recent_highway_nodes, \
            'highways':highways}


def Nodes(all_nodes, highway_nodes, from_date):
    recent_nodes = []

    for node in highway_nodes:
        element = all_nodes[node]
        date = element.attrib['timestamp'].split('-')
        if(int(date[0]) >= from_date[0] and int(date[1]) >= from_date[1]):
            element.append(Element('tag', {'k': 'recent_node', 'v': 'true'}))
            recent_nodes.append(node)
        else:
            element.append(Element('tag', {'k': 'recent_node', 'v': 'false'}))

    return recent_nodes


def Required_Ways(all_ways, recent_nodes, highways):
    new_required_highways = []
    new_required_nodes = []
    for way in highways:
        element = all_ways[way]
        match = False
        for sub_element in element.findall('nd'):
            if(match == True):
                break
            for node in recent_nodes:
                if(node == sub_element.attrib['ref']):
                    new_required_highways.append(element.attrib['id'])
                    match = True
                    break
        if(match == True):
            for sub_element in element.findall('nd'):
                new_required_nodes.append(sub_element.attrib['ref'])
    
    return {'new_required_highways':new_required_highways, \
            'new_required_nodes':new_required_nodes}

def Modified(left, bottom, right, top, year, month, root_path, count):
    url = 'http://overpass-api.de/api/map?bbox=' + \
          str(left) + "," + str(bottom) + "," + str(right) + "," + str(top)
    
    modified_file = root_path + 'modified' + str(count) + '.osm'
    orig_file = root_path + 'orig' + str(count) + '.osm'


    try:
	from_date = [year, month]
	tree = Parse(Download(left, bottom, right, top))
	root = tree.getroot()

	#write out original recieved file
	tree.write(orig_file)

	#build dictionary for nodes, ways, and relations 
	#of all features is .osm tree
	features_dict = Build_Dictionary(root)
	nodes = features_dict['nodes']
	ways = features_dict['ways']

	highway_results = Highways(ways, from_date)
	recent_nodes = Nodes(nodes, highway_results['highway_nodes'], from_date)
	required_highways = Required_Ways(ways, recent_nodes, highway_results['highways'])
	
	modified_nodes = []
	modified_ways = []

	#combine needed nodes and ways from different lists
	modified_nodes.extend(highway_results['recent_highway_nodes'])
	modified_nodes.extend(recent_nodes)
	modified_nodes.extend(required_highways['new_required_nodes'])
	modified_ways.extend(highway_results['recent_highways'])
	modified_ways.extend(required_highways['new_required_highways'])
	
	modified_nodes = list(set(modified_nodes))
	modified_ways = list(set(modified_ways))

	modified_tree = New_Tree(root)
	modified_root = modified_tree.getroot()

	for node in modified_nodes:
	    modified_root.append(nodes[node])

	for way in modified_ways:
	    modified_root.append(ways[way])

	modified_tree.write(modified_file)
	

    except urllib2.HTTPError, e:
	print e
	print "Invalid Bounding Box?"
    except urllib2.URLError, e:
	print e


    finish = datetime.now()
    print finish

    diff = finish - start
    print diff
