from export_recent_highways import recent_highways
from datetime import datetime

start = datetime.now()

#date (inclusive)
year = 2013
month = 4

left = -123.2
bottom = 45.3
right = -122.3
top = 45.8

#left = 0.0
#bottom = 0.0
#right = 1.0
#top = 1.0



print "start"

#recent_highways(sub_left, sub_bottom, sub_right, sub_top, year, month, 1)



count = 1
inc = 0.1

row = top
sub_left = left
sub_right = left + inc
sub_top = top
sub_bottom = top - inc

while row > bottom:
    print str(count) + ": " + \
          str(round(sub_left, 1)) + ", " + \
          str(round(sub_bottom, 1)) + ", " + \
          str(round(sub_right, 1)) + ", " + \
          str(round(sub_top, 1))
    
    recent_highways(sub_left, sub_bottom, sub_right, sub_top, year, month, count)

    sub_left = sub_left + inc
    sub_right = sub_right + inc

    if(sub_right >= right):
        sub_left = left
        sub_right = left + inc
        row = row - inc
        sub_top = row
        sub_bottom = sub_top - inc
        
    count += 1


print "finished"

finish = datetime.now()
print finish - start
    
#sub_left
#sub_right
#sub_top
#sub_bottom
