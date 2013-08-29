import urllib2
import sys
from xml.etree import cElementTree as ElementTree
from xml.etree.cElementTree import Element

#old_path = '/home/jeff/trimet/osm/change/0813_highways.osm'
#change_path = '/home/jeff/trimet/osm/change/0813_to_0827_change.osm'
#out_path = '/home/jeff/trimet/osm/change/0813_to_0827.osm'


old_file = sys.argv[1]
change_file = sys.argv[2]
out_file = sys.argv[3]

print old_file
print change_file
print out_file

def Identify(change_file):
    change_tree = ElementTree.parse(change_file)
    change_root = change_tree.getroot()

    delete_nodes = {}
    delete_ways = {}
    delete_relations = {}
    modify_nodes = {}
    modify_ways = {}
    modify_relations = {}
    create_nodes = {}
    create_ways = {}
    create_relations = {}
    needed_nodes = {}
    
    for child in change_root.findall('delete'):
        for node in child.findall('node'):
            node.append(Element('tag', {'k':'change', 'v':'delete'}))
	    delete_nodes[node.attrib['id']] = node
        
        for way in child.findall('way'):
	    way.append(Element('tag', {'k':'change', 'v':'delete'}))
            for sub_element in way.findall('nd'):
                needed_nodes[sub_element.attrib['ref']] = sub_element.attrib['ref']
            delete_ways[way.attrib['id']] = way

        for relation in child.findall('relation'):
	    relation.append(Element('tag', {'k':'change', 'v':'delete'}))
            delete_relations[relation.attrib['id']] = relation


    for child in change_root.findall('modify'):
        for node in child.findall('node'):
            node.append(Element('tag', {'k':'change', 'v':'modify'}))
	    modify_nodes[node.attrib['id']] = node
        
        for way in child.findall('way'):
            way.append(Element('tag', {'k':'change', 'v':'modify'}))
            for sub_element in way.findall('nd'):
                needed_nodes[sub_element.attrib['ref']] = sub_element.attrib['ref']
	    modify_ways[way.attrib['id']] = way

        for relation in child.findall('relation'):
	    relation.append(Element('tag', {'k':'change', 'v':'modify'}))
            modify_relations[relation.attrib['id']] = relation


    for child in change_root.findall('create'):
        for node in child.findall('node'):
	    node.append(Element('tag', {'k':'change', 'v':'create'}))
            create_nodes[node.attrib['id']] = node

        for way in child.findall('way'):
	    way.append(Element('tag', {'k':'change', 'v':'create'}))
            for sub_element in way.findall('nd'):
                needed_nodes[sub_element.attrib['ref']] = sub_element.attrib['ref']
            create_ways[way.attrib['id']] = way
        
        for relation in child.findall('relation'):
	    relation.append(Element('tag', {'k':'change', 'v':'create'}))
            create_relations[relation.attrib['id']] = relation

    return {'delete_nodes':delete_nodes, \
            'delete_ways':delete_ways, \
            'delete_relations':delete_relations, \
            'modify_nodes':modify_nodes, \
            'modify_ways':modify_ways, \
            'modify_relations':modify_relations, \
            'create_nodes':create_nodes, \
            'create_ways':create_ways, \
            'create_relations':create_relations, \
            'needed_nodes':needed_nodes}

def New_Tree(old_root):
    new_root = Element('osm')
    new_root.set('version', old_root.attrib['version'])
    new_root.append(old_root.find('bounds'))
    return ElementTree.ElementTree(new_root)


def Build(results, old_file, out_file):
    old_tree = ElementTree.parse(old_file)
    old_root = old_tree.getroot()
    new_tree = New_Tree(old_root)
    new_root = new_tree.getroot()

    delete_nodes = results['delete_nodes']
    delete_ways = results['delete_ways']
    modify_nodes = results['modify_nodes']
    modify_ways = results['modify_ways']
    create_nodes = results['create_nodes']
    create_ways = results['create_ways']
    needed_nodes = results['needed_nodes']


    for node in old_root.findall('node'):
        match = node.attrib['id']
        if match in delete_nodes:
            new_root.append(delete_nodes[match])
        elif match in modify_nodes:
            new_root.append(modify_nodes[match])
        elif match in needed_nodes:
            node.append(Element('tag', {'k':'change', 'v':'false'}))
            new_root.append(node)


    for way in old_root.findall('way'):
        match = way.attrib['id']
        if match in delete_ways:
            new_root.append(delete_ways[match])
        elif match in modify_ways:
            new_root.append(modify_ways[match])
        

    for node in create_nodes.keys():
        new_root.append(create_nodes[node])
    for way in create_ways.keys():
        new_root.append(create_ways[way])

    


    new_tree.write(out_file)



results = Identify(change_file)
Build(results, old_file, out_file)


