import cv2
import datetime
import matplotlib.pyplot as plt
import numpy as np 
import pydicom
from pydicom.data import get_testdata_files
import os
import time
 
#s1 = "dataset/Pattern 1/b23.dcm"
#s2 = "dataset/Pattern 1/f27.dcm"

#d1 = pydicom.dcmread(s1)
#d2 = pydicom.dcmread(s2) 

# Open the image files. 
#img1_color = d1.pixel_array/255
#img2_color = d2.pixel_array/255

# Specify the .dcm folder path
dcmPath = "dataset\Pattern 3"

# Specify the output jpg/png folder path
jpgPath = ""

def convert_file(dcm_path, jpg_path):
    dicom_images = pydicom.read_file(dcm_path)
    images = dicom_images.pixel_array
    scale = cv2.convertScaleAbs(images-np.min(images), alpha=(255.0 / min(np.max(images)-np.min(images), 10000)))
    cv2.imwrite(jpg_path, scale)

#convert_file(dcmPath, jpgPath)

ir = True;
starttime = datetime.datetime.now()
list = os.listdir(dcmPath)
for i in range(0,len(list)):
    dcmFilePath = os.path.join(dcmPath,list[i])
    print (i)
    print (dcmFilePath)
    ID = dcmFilePath.split('/')[-1].split('.')[0]
    jpgFilePath = jpgPath+ID+'.jpg'
    convert_file(dcmFilePath, jpgFilePath)
    print(jpgFilePath)

    if(ir):
      # Wait for 5 seconds
      time.sleep(2)

      img1_color = cv2.imread(jpgFilePath)  # Image to be aligned. 
      img2_color = cv2.imread("22.jpg")    # Reference image. 

      print(jpgFilePath)
      # Convert to grayscale. 
      img1 = cv2.cvtColor(img1_color, cv2.COLOR_BGR2GRAY) 
      img2 = cv2.cvtColor(img2_color, cv2.COLOR_BGR2GRAY) 
      height, width = img2.shape 
        
      # Create ORB detector with 5000 features. 
      orb_detector = cv2.ORB_create(5000) 
        
      # Find keypoints and descriptors. 
      # The first arg is the image, second arg is the mask 
      #  (which is not reqiured in this case). 
      kp1, d1 = orb_detector.detectAndCompute(img1, None) 
      kp2, d2 = orb_detector.detectAndCompute(img2, None) 
        
      # Match features between the two images. 
      # We create a Brute Force matcher with  
      # Hamming distance as measurement mode. 
      matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck = True) 
        
      # Match the two sets of descriptors. 
      matches = matcher.match(d1, d2) 
        
      # Sort matches on the basis of their Hamming distance. 
      matches.sort(key = lambda x: x.distance) 
        
      # Take the top 90 % matches forward. 
      matches = matches[:int(len(matches)*90)] 
      no_of_matches = len(matches) 
        
      # Define empty matrices of shape no_of_matches * 2. 
      p1 = np.zeros((no_of_matches, 2)) 
      p2 = np.zeros((no_of_matches, 2)) 
        
      for i in range(len(matches)): 
        p1[i, :] = kp1[matches[i].queryIdx].pt 
        p2[i, :] = kp2[matches[i].trainIdx].pt 
        
      # Find the homography matrix. 
      homography, mask = cv2.findHomography(p1, p2, cv2.RANSAC) 
        
      # Use this matrix to transform the 
      # colored image wrt the reference image. 
      transformed_img = cv2.warpPerspective(img1_color, 
                          homography, (width, height)) 
        
      # Save the output. 
      cv2.imwrite(jpgPath+ID+'c.jpg', transformed_img) 
endtime = datetime.datetime.now()
print (endtime - starttime)
