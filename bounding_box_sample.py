"""
from dict_test import Modified
try:
    from xml.etree import cElementTree as ElementTree
    from xml.etree.cElementTree import Element
except ImportError:
    from xml.etree import ElementTree
    from xml.etree.ElementTree import Element
"""
from datetime import datetime
import urllib2
import shutil
import subprocess

start = datetime.now()

#date (inclusive)
year = 2013
month = 4

"""
Test Area
left = -122.736059
bottom = 45.309679
right = -122.236059
top = 45.809679
"""

left = -122.4
bottom = 45.5
right = -122.35
top = 45.55

root_path = '/home/jeff/trimet/output/' 
#master = root_path + 'test_map.osm'
#master = root_path + 'map.osm'


def Download(left, bottom, right, top, out_file):
    print "Downloading"
    url = 'http://overpass-api.de/api/map?bbox=' + \
           str(left) + "," + str(bottom) + "," + str(right) + "," + str(top)

    xml = urllib2.urlopen(url)
    print "Download Complete"
    with open(out_file, 'wb') as fp:
        shutil.copyfileobj(xml, fp)


def Select_Highways(in_file):
    osmosis = "osmosis"
    rx = "--rx"
    wx = "--wx"
    sort = "--s"
    tf_highway = "--tf accept-ways highway=* --used-node"
    out_file = "all_highways.osm"
    command = " ".join([osmosis, rx, in_file, sort, tf_highway, wx, out_file])
    subprocess.call(command, shell=True)
    print command


def Build_Master_Dictionary(count, root_path):
   
    nodes = {}
    ways = {} 
    nodes_list = []
    ways_list = []
 
    current = 0
    
    while(current < count - 1):
        current += 1
        current_path = root_path + 'modified' + str(current) + '.osm'
        tree = ElementTree.parse(current_path)
        root = tree.getroot()
        
        for child in root.findall('node'):
            nodes[child.attrib['id']] = child
            nodes_list.append(child.attrib['id'])
        for child in root.findall('way'):
            ways[child.attrib['id']] = child
            ways_list.append(child.attrib['id'])
 
        print "current: " + str(current)
        print len(nodes_list)
        print len(ways_list)

 
    nodes_list = list(set(nodes_list))
    ways_list = list(set(ways_list))

    return {'nodes':nodes, 'ways':ways, \
            'nodes_list':nodes_list, 'ways_list':ways_list}


def New_Tree(left, bottom, right, top):
    osm = Element('osm')
    osm.set('version', '0.6')
    bounds = Element('bounds', {'maxlat':str(top), 'maxlon':str(right), \
                                'minlat':str(bottom), 'minlon':str(left)})
    osm.append(bounds)

    return ElementTree.ElementTree(osm)


def Build_Final_File(osm, results, root_path):
    nodes = results['nodes']
    nodes_list = results['nodes_list']
    ways = results['ways']
    ways_list = results['ways_list']

    root = osm.getroot()
    for node in nodes_list:
        root.append(nodes[node])
    for way in ways_list:
        root.append(ways[way])

    
    osm.write(root_path + 'final_modified.osm')



print "Start Program:"
print start

#print "parsing master osm file"

#master_tree = ElementTree.parse(master)
#root = master_tree.getroot()
count = 1
inc = 0.25

row = top
sub_left = left
sub_right = left + inc
sub_top = top
sub_bottom = top - inc

all_required_nodes = []
all_required_ways = []



print "starting on seperate segments"

while row > bottom:
    print "segment: " + str(count)
    required_nodes = []
    required_ways = []
    print str(count) + ": " + \
          str(round(sub_left, 1)) + ", " + \
          str(round(sub_bottom, 1)) + ", " + \
          str(round(sub_right, 1)) + ", " + \
          str(round(sub_top, 1))
    
    #results = Modified(sub_left, sub_bottom, sub_right, sub_top, \
    #                   year, month, root_path, count)

    #all_required_nodes.extend(results['nodes'])
    #all_required_ways.extend(results['ways'])

    sub_left = sub_left + inc
    sub_right = sub_right + inc

    if(sub_right >= right):
        sub_left = left
        sub_right = left + inc
        row = row - inc
        sub_top = row
        sub_bottom = sub_top - inc
        
    count += 1

print "analyzed all areas"


out_file = "output.osm"
Download(left, bottom, right, top, out_file)
Select_Highways(out_file)

#osm = New_Tree(left, bottom, right, top)
#results = Build_Master_Dictionary(count, root_path)
#Build_Final_File(osm, results, root_path)



 
#print "length before.."
#print len(all_required_nodes)
#print len(all_required_ways)

#all_required_nodes = list(set(all_required_nodes))
#all_required_ways = list(set(all_required_ways))

#print "length after.."
#print len(all_required_nodes)
#print len(all_required_ways)

#analyze = datetime.now()
#print "download and analyze all data: " + str(analyze - start)


#print "searching for required nodes" 
#for child in root.findall('node'):
#    if(child.attrib['id'] not in all_required_nodes):
#        root.remove(child)

#nodes_time = datetime.now()
#print "grab nodes: " + str(nodes_time - analyze)

#print "searching for required ways"
#for child in root.findall('way'):
#    if(child.attrib['id'] not in all_required_ways):
#        root.remove(child)

#ways_time = datetime.now()
#print "grab ways: " + str(ways_time - nodes_time)


#print "removing relations"
#for child in root.findall('relation'):
#    root.remove(child)


#print "writing final file to " + root_path + 'final_output.osm'
#master_tree.write(root_path + 'final_output.osm')

#finish = datetime.now()
#print "total time:" + str(finish - start)
    
#sub_left
#sub_right
#sub_top
#sub_bottom
