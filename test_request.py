#import library to do http requests:
import urllib2
import codecs

#import easy to use xml parser called minidom:
from xml.dom.minidom import parseString
#all these imports are standard on most modern python implementations
 
#download the file:


file = urllib2.urlopen('http://api.openstreetmap.org/api/0.6/map?bbox=-122.675,45.520,-122.670,45.525')


f = codecs.open("P://osm/test.osm", "w", "utf-8")
f2 = codecs.open("P://osm/test2.osm", "w", "utf-8")


#convert to string:
data = file.read()
#close file because we dont need it anymore:
file.close()
#parse the xml you downloaded



dom = parseString(data)





#retrieve the first xml tag (<tag>data</tag>) that the parser finds with name tagName:

#way_nodes = dom.getElementsByTagName('way')[0].toxml()

#<node id="2172271854" visible="true" version="1" changeset="15154336" timestamp="2013-02-24T21:18:33Z" user="wegavision" uid="564585" lat="45.5232600" lon="-122.6735153"/>

for node in dom.getElementsByTagName('node'):
    user = node.getAttribute('user') 
    date = node.getAttribute('timestamp')
    lat = node.getAttribute('lat')
    lon = node.getAttribute('lon')
    date_parse = date.split('-')
    #print date
    year = int(date_parse[0])
    month = int(date_parse[1])

    if(year > 2012 and month > 4):
        data = node.toxml()
        f.write(data + u'\n')
        #print user + " " + lat + "-" + lon



for way in dom.getElementsByTagName('way'):  # visit every node <bar />
    user = way.getAttribute('user') 
    date = way.getAttribute('timestamp')
    date_parse = date.split('-')
    #print date
    year = int(date_parse[0])
    month = int(date_parse[1])

    if(year > 2012 and month > 4):
        #print way.getAttribute('id')
        data = way.toxml()
        f.write(data + u'\n')
        #print way.toxml()



for relation in dom.getElementsByTagName('relation'):  # visit every node <bar />
    user = relation.getAttribute('user') 
    date = relation.getAttribute('timestamp')
    date_parse = date.split('-')
    #print date
    year = int(date_parse[0])
    month = int(date_parse[1])

    if(year > 2012 and month > 4):
        data = relation.toxml()
        f.write(data + u'\n')
        #print way.toxml()

f.close()


    #month = int(str(node.getAttribute('timestamp')[5:7]))
    #print "year: " + year
    #print "month: " + month

    #if(int(str(node.getAttribute('timestamp')[0:4])) > 2012):
    #print node.getAttribute('timestamp')
    #way_data = node.replace(


    #print node.toxml()

#for way in way_nodes:
 #   print way

#print way_nodes


#strip off the tag (<tag>data</tag>  --->   data):
    #xmlData=xmlTag.replace('<tagName>','').replace('</tagName>','')
#just print the data
    #print xmlData

#print out the xml tag and data in this format: <tag>data</tag>
#print xmlTag



#http://api.openstreetmap.org/api/0.6/map?bbox=-122.675,45.525,-122674,45.526
#http://api.openstreetmap.org/api/0.6/map?bbox=11.54,48.14,11.543,48.145

#http://api.openstreetmap.org/api/0.6/map?bbox=-122.67,45.52,-122.66,45.53


#http://api.openstreetmap.org/api/0.6/changesets?bbox=-122.67,45.52,-122.66,45.53?time=2012-07-17T00:00:00Z



#time=2012-07-17T00:00:00Z
