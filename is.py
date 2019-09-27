#VERSION 0.0.0
print ("------ AUTHOR: NaTaN ANDRADE ------")
print ("Universidade Federal de Sao Paulo (UNIFESP)")
print ("Instituto de Ciencia e Tecnologia (ICT)") 
print ("Sao Jose dos Campos (SJC)")
print ("Estado de Sao Paulo (SP) ")
print ("BRASIL")

import os
import os.path
import matplotlib.pyplot as plt
import matplotlib
import nibabel as nib
import numpy as np
import glob as glob
from os.path import basename
from scipy import interpolate
from glob import glob
matplotlib.interactive(True)

#os.system("for i in `ls *.gz`; do gzip -d $i; done")
files = []
def encontrar_arq(caminho):
    for r, d, f in os.walk(caminho):
        for file in f:
            if '.txt' in file:
                files.append(os.path.join(r, file))

    for f in files:
        print(f)

    print(caminho)
    arquivos = glob(caminho + '*.nii')
    print(arquivos)

    for arquivo in arquivos:
        print(arquivo)
        return arquivos

#Path Images
caminho ="c:\\Users\\Iago.LabCG-PC\\Documents\\OpenCV\\dataset\\Pattern1/"  
    
resp = encontrar_arq(caminho)
print(resp[0])

#Example for two images
img_filepath = "../dataset/Pattern1/Pattern1__20160409103459_24.nii"
img_mask_filepath = "../dataset/Pattern1/Pattern1__20160409103459_23.nii"
output_filepath = os.path.join('../dataset','Pattern1'+ basename(resp[0]), "")

PC1 = 0.2
PC2 = 99.8

S1 = 1500
S2 = 9500

# Reads input image and mask
input_img = nib.load(img_filepath)
input_data = input_img.get_data()

input_mask = nib.load(img_mask_filepath).get_data()

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
std_img = nib.Nifti1Image(std_input, input_img.affine, input_img.header)
nib.save(std_img, output_filepath)

input_img = nib.load(img_filepath)
input_data = input_img.get_data()
input_data = np.rot90(input_data)
np.shape(input_data)

input_img2 = nib.load(output_filepath)
input_data2 = input_img.get_data()
input_data2 = np.rot90(input_data2)
np.shape(input_data2)

plt.figure()
plt.subplot(1,2,1)
plt.title('Input')
#Choose Layer Brain
plt.imshow(input_data[:,:,115])
plt.gray()
plt.subplot(1,2,2)
plt.title('standardization of intensity')
plt.imshow(input_data2[:,:,115])
plt.gray()
plt.show()


#Acknowledgment
#Eduardo Nigri 

