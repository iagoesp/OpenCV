import os
import cv2
import os.path
import matplotlib.pyplot as plt
import matplotlib
import nibabel as nib
import numpy as np
import glob as glob
import pydicom
from os.path import basename
from scipy import interpolate
from glob import glob


matplotlib.interactive(True)

#os.system("for i in `ls *.gz`; do gzip -d $i; done")
files = []
def encontrar_arq(caminho):
    print(caminho)
    for pastaAtual, subPasta, arq in os.walk(caminho):
        print("end da pasta atual: {}".format(pastaAtual))
        print("end da subPasta: {}".format(subPasta))
        for file in arq:
            if '.dcm' in file:
                files.append(os.path.join(pastaAtual, file))

    print("size = {}".format(len(files)))
    for arq in files:
        print("tem formato .nii: {}".format(arq))
#        print(arq)

    arquivos = files
#    print("glob: {}".format(arquivos))

    for arquivo in arquivos:
        print(arquivo)

    return arquivos

#Path Images
caminho = "dataset/Pattern1"

resp = encontrar_arq(caminho)
print("resp 0: {}".format(resp[0]))
print("resp 1: {}".format(resp[1]))

#Example for two images
img_filepath = pydicom.dcmread(resp[0])
img_mask_filepath = pydicom.dcmread(resp[1])
print(basename(resp[0]))
base = basename(resp[0]).split(".")
output_filepath = os.path.join('',''+ base[0], 'img')
try:
    os.makedirs(output_filepath)
except:
    os.rmdir(output_filepath)
    os.makedirs(output_filepath)


print(output_filepath)
print("done")
PC1 = 0.2
PC2 = 99.8

S1 = 1500
S2 = 9500

# Reads input image and mask
#input_img = nib.load(img_filepath)
input_data = img_filepath.pixel_array

input_mask = img_mask_filepath.pixel_array

# Separate brain
input_brain = input_data[input_mask.astype(np.bool)]

# Input percentiles
input_pcs = np.percentile(input_brain, [PC1, PC2])

# Standard percentiles
std_pcs = [S1, S2]

# Standardization function
f = interpolate.interp1d(input_pcs, std_pcs, kind="linear", bounds_error=False, fill_value="extrapolate")

# Applies function
std_input = f(input_data) * input_mask

# Saves image
#std_img = nib.Nifti1Image(std_input, input_img.affine, input_img.header)
#print(std_img)
#nib.save(std_img, output_filepath)

input_img = nib.load(img_filepath)
input_data = input_img.get_data()
input_data = np.rot90(input_data)
np.shape(input_data)

input_img2 = nib.load(output_filepath + ".nii")
input_data2 = input_img.get_data()
input_data2 = np.rot90(input_data2)
np.shape(input_data2)

height = input_data.shape[0]
windowScale = height/1000
print (windowScale)

newX,newY = input_data.shape[1]/windowScale, input_data.shape[0]/windowScale

imgID1 = cv2.resize(input_data, (int(newX), int(newY)))
imgID2 = cv2.resize(input_data2, (int(newX), int(newY)))


cv2.imshow("image", imgID1)
cv2.imshow("image2", imgID2)
cv2.waitKey(0)
cv2.destroyAllWindows()

#https://pydicom.github.io/pydicom/stable/auto_examples/input_output/plot_write_dicom.html

#Acknowledgment
#Eduardo Nigri
