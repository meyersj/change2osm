import subprocess

"""
filter out only ways that have a highway tag

osmosis \  
--read-xml 08132013_multnomah-SE.osm \
--tag-filter accept-ways highway=* \
--used-node \                        
--write-xml 0813_highways.osm \        

osmosis \                        
--read-xml 08272013_multnomah-SE.osm \
--tag-filter accept-ways highway=* \
--used-node \                        
--write-xml 0827_highways.osm \        


derive change file from old and new highway filtered osm files

osmosis                            
--read-xml 0813_highways.osm \   
--read-xml 0827_highways.osm \
--derive-change \ 
--write-xml-change 0813_to_0827_change.osm \       
"""

osmosis = 'osmosis'
read_xml = '--rx'
write_xml = '--wx'
derive_change = '--dc'
write_change = '--wxc'
tagfilter_highways = '--tf accept-ways highway=*'
tagfilter_relations = '--tf accept-relations type=restriction'
used_node = '--un'

old_osm = '08132013_multnomah.osm'
new_osm = '08272013_multnomah.osm'
old_highways = '0813_highways.osm'
new_highways = '0827_highways.osm'
change = '0813_to_0827_change.osm'
final = '0813_to_0827.osm'

process_old = " ".join([osmosis, read_xml, old_osm, tagfilter_highways, \
                        used_node, tagfilter_relations, write_xml, old_highways])

process_new = " ".join([osmosis, read_xml, new_osm, tagfilter_highways, \
                        used_node, tagfilter_relations, write_xml, new_highways])

process_change = " ".join([osmosis, read_xml, new_highways, read_xml, \
                            old_highways, derive_change, write_change, change])

process_create = " ".join(["python", "change2osm.py", old_highways, change, final])

subprocess.call(process_old, shell=True)
subprocess.call(process_new, shell=True)
subprocess.call(process_change, shell=True)
subprocess.call(process_create, shell=True)



