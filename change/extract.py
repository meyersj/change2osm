import subprocess

root_path = '/home/jeff/trimet/oms/change/'
recent = '08272013_multnomah-SE.osm'
old = '08132013_multnomah-SE.osm'
change_file = 'change.osm'

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

highways_old = 'osmosis --read-xml 08132013_multnomah.osm --tag-filter accept-ways highway=* --used-node --tag-filter reject-relations --write-xml 0813_highways.osm'

highways_new = 'osmosis --read-xml 08272013_multnomah.osm --tag-filter accept-ways highway=* --used-node --tag-filter reject-relations --write-xml 0827_highways.osm'

change = 'osmosis --read-xml 0827_highways.osm --read-xml 0813_highways.osm --derive-change --write-xml-change 0813_to_0827_change.osm'

subprocess.call(highways_old, shell=True)
subprocess.call(highways_new, shell=True)
subprocess.call(change, shell=True)





