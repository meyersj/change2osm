import subprocess, sys, os, csv, change2osm, getopt

def usage():
    print "Usage:"
    print "Script creates .osm file showing changes between two .osm files"
    print "python extract.py -o <old> -n <new> [-u <users>]"
    print "-o specify old .osm file"
    print "-n specify new .osm file"
    print "-u include a list of preapproved users whose edits are ignored"
    print "    users list should be csv or text file with names seperated by carrige return"

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "o:n:u:", ["old", "new", "users"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-o", "--old"):
            old_osm = arg
        elif opt in ("-n", "--new"):
            new_osm = arg
        elif opt in ("-u", "--users"):
            users_path = arg

    users = []

    try:
        approved_users = csv.reader(open(users_path, 'rb'))
        for user in approved_users:
            users.append(str(user)[2:-2])
    except:
        print "pre-approved users list not being used"

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


    try:
        print "filtering out highway=* ways"
        subprocess.check_call(process_old, shell=True)
    except subprocess.CalledProcessError:
        print "failed to process old .osm file"
        sys.exit(2)

    try:
        subprocess.check_call(process_new, shell=True)
    except subprocess.CalledProcessError:
        print "failed to process new .osm file"
        sys.exit(2)

    try:
        print "deriving change file"
        subprocess.check_call(process_change, shell=True)
    except subprocess.CalledProcessError:
        print "failed to derive change file"
        sys.exit(2)


    print "building osm file from change file"
    results = change2osm.Identify(change, users)
    change2osm.Build(results, old_osm, final)

    print "cleaning up"
    os.remove(old_highways)
    os.remove(new_highways)
    os.remove(change)

    print "process complete"
    
if __name__ == "__main__":
    main(sys.argv[1:])
