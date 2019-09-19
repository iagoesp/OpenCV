# authors : Guillaume Lemaitre <g.lemaitre58@gmail.com>
# license : MIT

import cv2
import matplotlib.pyplot as plt
import pydicom
from pydicom.data import get_testdata_files

#print(__doc__)

name = "dataset/28.dcm"
#name = "OBXXXX1A.dcm"

split = name.split("/")
if(len(split) == 1):
    filePydicom = get_testdata_files(name)[0]
    dataset = pydicom.dcmread(filePydicom)

else:
    filePydicom = name
    dataset = pydicom.dcmread(name)

# Normal mode:
print(" ")
print("Filename.........:", filePydicom)
print("Storage type.....:", dataset.SOPClassUID)
print()

if 'PixelData' in dataset:
    rows = int(dataset.Rows)
    cols = int(dataset.Columns)
    print("Image size.......: {rows:d} x {cols:d}, {size:d} bytes".format(
        rows=rows, cols=cols, size=len(dataset.PixelData)))
    if 'PixelSpacing' in dataset:
        print("Pixel spacing....:", dataset.PixelSpacing)

# use .get() if not sure the item exists, and want a default value if missing
print("Slice location...:", dataset.get('SliceLocation', "(missing)"))

# plot the image using matplotlib
maxvalue = -100000
minvalue = 100000
for n, val in enumerate(dataset.pixel_array.flat):
    if maxvalue < val:
        maxvalue = val

    if minvalue > val:
        minvalue = val

print (minvalue)
print (maxvalue)

# plot the image using matplotlib
pixels = dataset.pixel_array/maxvalue

height, width = pixels.shape

M = cv2.getRotationMatrix2D((height/2, width/2), 0, 1)
newImage = cv2.warpAffine(pixels,M,(width,height))

height, width = newImage.shape
windowScale = height/1000
print (windowScale)

newX,newY = newImage.shape[1]/windowScale, newImage.shape[0]/windowScale

imgf = cv2.resize(newImage, (int(newX), int(newY)))   

cv2.imshow("image", imgf)  
cv2.waitKey(0)
cv2.destroyAllWindows()