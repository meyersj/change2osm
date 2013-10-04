"""
File: change2osm.py
Created by: Jeffrey Meyers
Email: jeffrey dot meyers at pdx dot edu
Created on: 10/4/2013
Modified: 10/4/2013

Description:
	
	This file is run as command line tool that takes an old osm file
	and a new osm file a generates an osm file that shows changes between the two files.
	The final output is a .osm file that can be viewed in an editor such as josm.

	The output will be an osm file containing an additional 'change' tag specifying if that
	object was created, modified, or deleted. You have the option of including a
	new line seperated list of usernames as an argument that you would like to have removed 
	from the final output. Any object that is created or modified by these users will not show up, 
	but features deleted by these users will still be present.

Arguments:

	-o <old osm file> (required)
	-n <new osm file> (required)
	-u <text file of each user to exlude on new line> (optional)
	-f <output path and file name> (optional)
        -q quiet mode

Example Usage:

	python change2osm.py -o old_osm_file.osm -n new_osm_file.osm -u users_to_exclude.txt -f change.osm

Dependencies: 
	
	osmosis

Notes:
	Currently osmosis is used to filter out only ways containing a highway tag. To change
	this modify the 'filter_osm' variable.

	Changes to relations are not currently implemented.

"""


import subprocess, sys, os, csv, osc2osm, getopt


# usage()
# prints out how to help for how to use command
def usage():
    print "Usage:"
    print "	Script creates .osm file showing changes between two .osm files"
    print ""
    print "Arguments:"
    print "	-o <specify old .osm file> (required)" 
    print "	-n <specify new .osm file> (required)"
    print "	-u <text file with one username per line for user edits to be ignored>"
    print "	-f <output name>"
    print "     -q quite mode"
    print ""
    print "Example:" 
    print "	python change2osm.py -q -o old_osm_file.osm"
    print "                          -n new_osm_file.osm"
    print "                          -u users_to_exclude.txt"
    print "                          -f change.osm"

# main function
def main(argv):
    final = ""
    old_osm = ""
    new_osm = ""
    users_path = ""
    QUIET = False

    # process parameters passed from command line
    # -o <old osm file path>
    # -n <new osm file path>
    # -u <text file with user names to exclude>
    # -f <output for final file>
    try:
        opts, args = getopt.getopt(argv, "o:n:u:f:q", ["old", "new", "users", "file", "quiet"])

    # run usage function and exit of parameters are not correct
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    # assign argument to correct variable
    for opt, arg in opts:
        if opt in ("-o", "--old"):
            old_osm = arg
        elif opt in ("-n", "--new"):
            new_osm = arg
        elif opt in ("-u", "--users"):
            users_path = arg
	elif opt in ("-f", "--file"):
	    final = arg
	elif opt in ("-q", "--quiet"):
	    QUIET = True
            

    if QUIET == True:
        sys.stdout = open(os.devnull, 'a')
	sys.stderr = open(os.devnull, 'a')

    if new_osm == "" or old_osm == "":
	print "Error: old osm file and new osm file arguments are required.\n"
	usage()
	sys.exit(2)

    print "\n"

    # build list of users to exclude
    users = []
    
    if users_path == "":
        print "Pre-approved users list not being used"
    else:
        try:
            approved_users = csv.reader(open(users_path, 'rb'))
            for user in approved_users:
                users.append(str(user)[2:-2])
        except:
            print "Warning: Could not read users list. List is not being used"

    old_highways = 'old_highways.osm'
    new_highways = 'new_highways.osm'
    change = 'change.osc'
    new_file, new_ext = os.path.splitext(new_osm)
    if final == "":
        final = new_file + "_change.osm"

    # osmosis command used to filter out highways from osm file
    filter_osm = 'osmosis -q --rx %s --tf accept-ways highway=* '\
                 '--un --tf accept-relations type=restriction '\
                 '--wx %s'

    # osmosis command used to derive change file from 
    derive_change = 'osmosis -q --rx %s --rx %s --dc --wxc %s'

    # format osmosis commands with correct file names
    old_filter_command = filter_osm % (old_osm, old_highways)
    new_filter_command = filter_osm % (new_osm, new_highways)
    derive_change_command = derive_change % (new_highways, old_highways, change)
    #derive_change_command = derive_change % (new_osm, old_osm, change)


    
    # execute osmosis commands to filter then derive change file
    try:
        print "Filtering out ways with highway tag from old .osm file"
        print "  Executing: " + old_filter_command
        subprocess.check_call(old_filter_command, shell=True)
    except subprocess.CalledProcessError:
        print "Failed to process old .osm file"
        sys.exit(2)

    try:
        print "Filtering out ways with highway tag from new .osm file"
        print "  Executing: " + new_filter_command
        subprocess.check_call(new_filter_command, shell=True)
    except subprocess.CalledProcessError:
        print "Failed to process new .osm file"
        os.remove(old_highways)
        sys.exit(2)

    
    try:
        print "Deriving change file"
        print "  Executing: " + derive_change_command
        subprocess.check_call(derive_change_command, shell=True)
    except subprocess.CalledProcessError:
        print "Failed to derive change file"
	os.remove(new_highways)
	os.remove(old_highways)
        sys.exit(2)


    # uses functions from osc2osm.py file to generate osm file from osc change file
    print "Building .osm file from change file"
    results = osc2osm.Identify(change, users)
    osc2osm.Build(results, old_osm, final)

    # remove files not needed
    print "Cleaning up"
    os.remove(old_highways)
    os.remove(new_highways)
    os.remove(change)

    print "Process complete"
    
if __name__ == "__main__":
    main(sys.argv[1:])

