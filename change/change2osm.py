import urllib2
from xml.etree import cElementTree as ElementTree
from xml.etree.cElementTree import Element

old_path = '/home/jeff/trimet/osm/change/0813_highways.osm'
change_path = '/home/jeff/trimet/osm/change/0813_to_0827_change.osm'
out_path = '/home/jeff/trimet/osm/change/0813_to_0827.osm'

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
    needed_nodes = {}
    
    print "...delete"
    for child in change_root.findall('delete'):
        print 'node'
        for node in child.findall('node'):
	    print node.attrib['id']
            node.append(Element('tag', {'k':'change', 'v':'delete'}))
	    delete_nodes[node.attrib['id']] = node
        #way
        print 'way'
        for way in child.findall('way'):
	    print way.attrib['id']
	    way.append(Element('tag', {'k':'change', 'v':'delete'}))
            for sub_element in way.findall('nd'):
                needed_nodes[sub_element.attrib['ref']] = sub_element.attrib['ref']
            delete_ways[way.attrib['id']] = way

        #relation
        #for relation in child.findall('relation'):
	#    print relation.attrib['id']
	#    delete_relations[relation.attrib['id']] = relation.attrib['id']

    print "...modify"
    for child in change_root.findall('modify'):
        #node
        print child.tag
        print 'node'
        for node in child.findall('node'):
	    print node.attrib['id']
            node.append(Element('tag', {'k':'change', 'v':'modify'}))
	    modify_nodes[node.attrib['id']] = node
        #way
        print 'way'
        for way in child.findall('way'):
	    print way.attrib['id']
            way.append(Element('tag', {'k':'change', 'v':'modify'}))
            for sub_element in way.findall('nd'):
                needed_nodes[sub_element.attrib['ref']] = sub_element.attrib['ref']
	    modify_ways[way.attrib['id']] = way

        #relation
        #for relation in child.findall('relation'):
	#    print relation.attrib['id']
	#    modify_relations[relation.attrib['id']] = relation

    print "...create"
    for child in change_root.findall('create'):
        #node
        print child.tag
        print 'node'
        for node in child.findall('node'):
	    print node.attrib['id']
	    node.append(Element('tag', {'k':'change', 'v':'create'}))
            create_nodes[node.attrib['id']] = node
        #way
        print 'way'
        for way in child.findall('way'):
	    print way.attrib['id']
	    way.append(Element('tag', {'k':'change', 'v':'create'}))
            for sub_element in way.findall('nd'):
                needed_nodes[sub_element.attrib['ref']] = sub_element.attrib['ref']
            create_ways[way.attrib['id']] = way

        #relation
        #for relation in child.findall('relation'):
	#    print relation.attrib['id']
	#    create_relations[relation.attrib['id']] = relation

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


def Build(results, old_path, out_path):
    old_tree = ElementTree.parse(old_path)
    old_root = old_tree.getroot()
    new_tree = New_Tree(old_root)
    new_root = new_tree.getroot()

    delete_nodes = results['delete_nodes']
    delete_ways = results['delete_ways']
    #delete_relations = results['delete_relations']
    modify_nodes = results['modify_nodes']
    modify_ways = results['modify_ways']
    #modify_relations = results['modify_relations']
    create_nodes = results['create_nodes']
    create_ways = results['create_ways']
    #create_relations = results['create_relations']
    needed_nodes = results['needed_nodes']


    for node in old_root.findall('node'):
        match = node.attrib['id']
        if match in delete_nodes:
            new_root.append(delete_nodes[match])
        elif match in modify_nodes:
            new_root.append(modify_nodes[match])
        elif match in create_nodes:
            new_root.append(create_nodes[match])
        elif match in needed_nodes:
            new_root.append(node)


    for way in old_root.findall('way'):
        match = way.attrib['id']
        if match in delete_ways:
            new_root.append(delete_ways[match])
        elif match in modify_ways:
            new_root.append(modify_ways[match])
        elif match in create_ways:
            new_root.append(create_ways[match])


    new_tree.write(out_path)



results = Identify(change_path)
Build(results, old_path, out_path)
