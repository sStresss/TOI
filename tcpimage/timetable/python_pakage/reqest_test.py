import sys
import datetime
time = datetime.datetime.now()
output = "Hi %s current time is %s" % (sys.argv[1], time)

#print('3333333333', output)
new_line = str(sys.argv[1])
new_line = new_line.split(',')
k_l = []
for _ in new_line:
    img = _[9:]
    if len(img) > 1:
        k_l.append(img)
print(k_l, 'end')
