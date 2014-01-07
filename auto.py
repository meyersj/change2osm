import subprocess, glob, sys, os
from datetime import datetime

# set directory paths
cur_dir = 'G:/PUBLIC/OpenStreetMap/data/osm/'
old_dir = 'G:/PUBLIC/OpenStreetMap/data/osm/bkup/'
out_dir = 'G:/PUBLIC/OpenStreetMap/data/OSM_update/review_edits/output/'
script_dir = 'G:/PUBLIC/OpenStreetMap/data/OSM_update/review_edits/script/'

out_file = datetime.now().strftime('%m%d%Y') + '_edits_'
regions = ['clackamas.osm', 'multnomah.osm', 'washington.osm']

#get the date of the oldest osm file used to build -o argument
old_date = os.path.split(min(glob.glob(old_dir + '*.osm'), key=os.path.getctime))[1][0:9]

#build list of tuples for each region with old, new and out file names
files = []
for region in regions:
  files.append( (old_dir + old_date + region, cur_dir + region, out_dir + out_file + region) )

#unformatted python command to run change2osm.py script
change = 'python %s -o %s -n %s -u %s -f %s'

#for each region tuple run change2osm.py script
for old, new, out in files:
  change_command = change % (script_dir + 'change2osm.py', old, new, 
                             script_dir + 'approved_users_example.txt', out)
  
  try:
    subprocess.check_call(change_command, shell=True)
  except subprocess.CalledProcessError:
    print 'failed to run change script on %s and %s' % (old, new)
  
