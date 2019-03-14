import csv
import h5py
import datetime
import numpy
import pytz
import scipy
from scipy import signal
import matplotlib.pyplot as plt

#task 1

file_name = "1541962108935000000_167_838.h5"
timestamp = int(file_name[:18])/1000000000

utc_time = datetime.datetime.utcfromtimestamp(timestamp)

utc_time = utc_time.replace(tzinfo=pytz.UTC)#timezone aware
print("The UTC time is : "+str(utc_time))
cern_tz = pytz.timezone('Europe/Zurich')
cern_time = utc_time.astimezone(cern_tz)
print("The CERN time is : "+str(cern_time))

#task2 uses this visitor func

def visitor_func(name,node):
    if isinstance(node,h5py.Dataset):
            with open('data.csv', 'a', newline='') as csvfile:
                fieldnames = ['Dataset','Size','Shape','Type']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                print(name)
                print(node.size)
                print(node.shape)
                try:
                  print(node.dtype)
                  writer.writerow({'Dataset':name, 'Size':node.size,'Shape':node.shape,'Type':node.dtype})
                except:
                    print("This datatype is not supported")
    else:
            with open('data.csv', 'a', newline='') as csvfile:
                fieldnames = ['Group','Size','Shape','Type']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writerow({'Group':name, 'Size':'','Shape':'','Type':''})



with h5py.File(file_name,'r') as hdf_file:
    hdf_file.visititems(visitor_func)

#task 3
hdf_file = h5py.File(file_name,'r')

img_group = '/AwakeEventData/XMPP-STREAK/StreakImage/streakImageData'
dset = numpy.array(hdf_file[img_group])
img_width_group = '/AwakeEventData/XMPP-STREAK/StreakImage/streakImageHeight'
img_width = numpy.array(hdf_file[img_width_group])
img_height_group = '/AwakeEventData/XMPP-STREAK/StreakImage/streakImageWidth'
img_height = numpy.array(hdf_file[img_height_group])
new_image = dset.reshape(img_width[0],img_height[0])
filtered_image = scipy.signal.medfilt(new_image)
plt.imshow(filtered_image)
plt.savefig("image.png")
