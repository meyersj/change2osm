import subprocess, glob, sys, os
from datetime import datetime

# set directory paths
cur_dir = 'G:/PUBLIC/OpenStreetMap/data/osm/'
old_dir = 'G:/PUBLIC/OpenStreetMap/data/osm/bkup/'
out_dir = 'G:/PUBLIC/OpenStreetMap/data/RLIS_update_2013/edit_reviews/output/'
script_dir = 'C:/Users/meyersj/Documents/GitHub/change2osm/' 

out_file = datetime.now().strftime('%m%d%Y') + '_edits_'
regions = ['clackamas.osm', 'multnomah.osm', 'washington.osm']
old_files = glob.glob(old_dir + '*.osm')

#extract file names from old directory
files = []
for f in old_files:
  head, tail = os.path.split(f)
  files.append(tail)

#sort then extract oldest dated file
files.sort()
date = files[0][0:9]

#build list of tuples for each region with old, new and out file names
files= []
for region in regions:
  files.append( (old_dir + date + region, cur_dir + region, out_dir + out_file + region) )

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
