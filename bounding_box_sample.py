from export_recent_highways import recent_highways
from datetime import datetime
from xml.etree import ElementTree
from xml.etree.ElementTree import Element

start = datetime.now()

#date (inclusive)
year = 2013
month = 4

#left = -123.177212
#bottom = 45.241791
#right = -122.271479
#top = 45.681151

left = -123.0
bottom = 45.5
right = -122.8
top = 45.7

root_path = '/home/jeff/trimet/' 
#master = root_path + 'test_map.osm'
master = root_path + 'map.osm'


print "Start Program:"
print start

print "parsing master osm file"

master_tree = ElementTree.parse(master)
root = master_tree.getroot()
count = 1
inc = 0.1

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
    
    results = recent_highways(sub_left, sub_bottom, sub_right, sub_top, year, month, root_path, count)

    all_required_nodes.extend(results['nodes'])
    all_required_ways.extend(results['ways'])

    sub_left = sub_left + inc
    sub_right = sub_right + inc

    if(sub_right >= right):
        sub_left = left
        sub_right = left + inc
        row = row - inc
        sub_top = row
        sub_bottom = sub_top - inc
        
    count += 1


print "length before.."
print len(all_required_nodes)
print len(all_required_ways)

all_required_nodes = list(set(all_required_nodes))
all_required_ways = list(set(all_required_ways))

print "length after.."
print len(all_required_nodes)
print len(all_required_ways)

analyze = datetime.now()
print "download and analyze all data: " + str(analyze - start)


print "searching for required nodes" 
for child in root.findall('node'):
    if(child.attrib['id'] not in all_required_nodes):
        root.remove(child)

nodes_time = datetime.now()
print "grab nodes: " + str(nodes_time - analyze)

print "searching for required ways"
for child in root.findall('way'):
    if(child.attrib['id'] not in all_required_ways):
        root.remove(child)

ways_time = datetime.now()
print "grab ways: " + str(ways_time - nodes_time)


print "removing relations"
for child in root.findall('relation'):
    root.remove(child)


print "writing final file to " + root_path + 'final_output.osm'
master_tree.write(root_path + 'final_output.osm')

finish = datetime.now()
print "total time:" + str(finish - start)
    
#sub_left
#sub_right
#sub_top
#sub_bottom
