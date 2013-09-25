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

    old_highways = 'old_highways.osm'
    new_highways = 'new_highways.osm'
    change = 'change.osm'
    new_file, new_ext = os.path.splitext(new_osm)
    final = new_file + "_" + change

    filter_osm = 'osmosis -q --rx %s --tf accept-ways highway=* '\
                 '--un --tf accept-relations type=restriction '\
                 '--wx %s'

    derive_change = 'osmosis -q --rx %s --rx %s --dc --wxc %s'

    old_filter_command = filter_osm % (old_osm, old_highways)
    new_filter_command = filter_osm % (new_osm, new_highways)
    derive_change_command = derive_change % (new_highways, old_highways, change)
    
    try:
        print "Filtering out ways with highway tag from old .osm file"
        print "  executing: " + old_filter_command
        subprocess.check_call(old_filter_command, shell=True)
    except subprocess.CalledProcessError:
        print "failed to process old .osm file"
        sys.exit(2)

    try:
        print "Filtering out ways with highway tag from new .osm file"
        print "  executing: " + new_filter_command
        subprocess.check_call(new_filter_command, shell=True)
    except subprocess.CalledProcessError:
        print "failed to process new .osm file"
        sys.exit(2)

    try:
        print "Deriving change file"
        print "  executing: " + derive_change_command
        subprocess.check_call(derive_change_command, shell=True)
    except subprocess.CalledProcessError:
        print "failed to derive change file"
        sys.exit(2)


    print "Building .osm file from change file"
    results = change2osm.Identify(change, users)
    change2osm.Build(results, old_osm, final)

    print "Cleaning up"
    os.remove(old_highways)
    os.remove(new_highways)
    os.remove(change)

    print "Process complete"
    
if __name__ == "__main__":
    main(sys.argv[1:])
