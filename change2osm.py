import urllib2
from xml.etree import cElementTree as ElementTree
from xml.etree.cElementTree import Element

old_path = '/home/jeff/trimet/test/full.osm'
change_path = '/home/jeff/trimet/test/change.osm'

old_tree = ElementTree.parse(old_path)
old_root = old_tree.getroot()

delete_node = {}
delete_way = {}
delete_relation = {}



def Identify(change_path):
    change_tree = ElementTree.parse(change_path)
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

    
    print "...delete"
    for child in change_root.findall('delete'):
        print 'node'
        for node in child.findall('node'):
	    print node.attrib['id']
	    delete_nodes[node.attrib['id']] = node.attrib['id']
        #way
        print 'way'
        for way in child.findall('way'):
	    print way.attrib['id']
	    delete_ways[way.attrib['id']] = way.attrib['id']

        #relation
        for relation in child.findall('relation'):
	    print relation.attrib['id']
	    delete_relations[relation.attrib['id']] = relation.attrib['id']

    print "...modify"
    for child in change_root.findall('modify'):
        #node
        print child.tag
        print 'node'
        for node in child.findall('node'):
	    print node.attrib['id']
	    modify_nodes[node.attrib['id']] = node
        #way
        print 'way'
        for way in child.findall('way'):
	    print way.attrib['id']
	    modify_ways[way.attrib['id']] = way

        #relation
        for relation in child.findall('relation'):
	    print relation.attrib['id']
	    modify_relations[relation.attrib['id']] = relation

    print "...create"
    for child in change_root.findall('create'):
        #node
        print child.tag
        print 'node'
        for node in child.findall('node'):
	    print node.attrib['id']
	    create_nodes[node.attrib['id']] = node
        #way
        print 'way'
        for way in child.findall('way'):
	    print way.attrib['id']
	    create_ways[way.attrib['id']] = way

        #relation
        for relation in child.findall('relation'):
	    print relation.attrib['id']
	    create_relations[relation.attrib['id']] = relation

    return {'delete_nodes':delete_nodes, \
            'delete_ways':delete_ways, \
            'delete_relations':delete_relations, \
            'modify_nodes':modify_nodes, \
            'modify_ways':modify_ways, \
            'modify_relations':modify_relations, \
            'create_nodes':create_nodes, \
            'create_ways':create_ways, \
            'create_relations':create_relations}



Identify(change_path)

