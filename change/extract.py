import subprocess, sys, os, csv, change2osm

old_osm = sys.argv[1]
new_osm = sys.argv[2]
users_path = sys.argv[3]

users = []

try:
    approved_users = csv.reader(open(users_path, 'rb'))
    for user in approved_users:
        users.append(str(user)[2:-2])
    print users
except:
    print "users list not being used"




osmosis = 'osmosis -q'
read_xml = '--rx'
write_xml = '--wx'
derive_change = '--dc'
write_change = '--wxc'
tagfilter_highways = '--tf accept-ways highway=*'
tagfilter_relations = '--tf accept-relations type=restriction'
used_node = '--un'

old_file, old_ext = os.path.splitext(old_osm)
new_file, new_ext = os.path.splitext(new_osm)

old_highways = 'old_highways.osm'
new_highways = 'new_highways.osm'
change = 'change.osm'
final = new_file + "_" + "change.osm"



process_old = " ".join([osmosis, read_xml, old_osm, tagfilter_highways, \
			used_node, tagfilter_relations, write_xml, old_highways])
process_new = " ".join([osmosis, read_xml, new_osm, tagfilter_highways, \
			used_node, tagfilter_relations, write_xml, new_highways])
process_change = " ".join([osmosis, read_xml, new_highways, read_xml, \
			    old_highways, derive_change, write_change, change])

print "filtering out highway=* ways"
subprocess.call(process_old, shell=True)
subprocess.call(process_new, shell=True)

print "deriving change file"
subprocess.call(process_change, shell=True)

print "building osm file from change file"
results = change2osm.Identify(change, users)
change2osm.Build(results, old_osm, final)

print "cleaning up"
os.remove(old_highways)
os.remove(new_highways)
#os.remove(change)

print "process complete"


