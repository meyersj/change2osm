### Description:
	
	This file is run as command line tool that takes an old osm file
	and a new osm file a generates an osm file that shows changes between the two files.
	The final output is a .osm file that can be viewed in an editor such as josm.

	The output will be an osm file containing an additional 'change' tag specifying if that
	object was created, modified, or deleted. You have the option of including a
	new line seperated list of usernames as an argument that you would like to have removed 
	from the final output. Any object that is created or modified by these users will not show up, 
	but features deleted by these users will still be present.

### Arguments:

	-o <old osm file> (required)
	-n <new osm file> (required)
	-u <text file of each user to exlude on new line> (optional)
	-f <output path and file name> (optional)
	-q quiet mode

### Example Usage:

	python change2osm.py -o old_osm_file.osm -n new_osm_file.osm -u users_to_exclude.txt -f change.osm

### Dependencies: 
	
	osmosis

### Notes:

	Currently osmosis is used to filter out only ways containing a highway tag. To change
	this modify the 'filter_osm' variable.

	Changes to relations are not currently implemented
