import cv2
import numpy as np

count = 0
count = count + 1
print(count)
original = cv2.imread('carro3.jpg')
imagem2 = cv2.imread('carro4.jpg')
count = count + 1
print(count)
gray_original = cv2.cvtColor(original,cv2.COLOR_BGR2GRAY)
gray_imagem2 = cv2.cvtColor(imagem2,cv2.COLOR_BGR2GRAY)
count = count + 1
print(count)
_, escala = cv2.threshold(gray_original,127,255,cv2.THRESH_BINARY)

count = count + 1
print(count)

imgres = np.zeros(gray_original.shape,np.uint8)
imdilat = np.zeros( [escala.shape[0],escala.shape[1]], dtype=np.uint8)
imerosao = np.zeros([escala.shape[0],escala.shape[1]], dtype=np.uint8)
opening = np.zeros([escala.shape[0],escala.shape[1]], dtype=np.uint8)
count = count + 1
print(count)
closed = np.zeros([escala.shape[0],escala.shape[1]], dtype=np.uint8)
mascres = np.zeros([gray_imagem2.shape[0],escala.shape[1]], dtype=np.uint8)
mascarar = np.zeros([gray_imagem2.shape[0],escala.shape[1]], dtype=np.uint8)

count = count + 1
print(count)

print(gray_original.shape[0])
print(gray_original.shape[1])

for x in range(escala.shape[0] -1, escala.shape[1]-1):
    for y in range(escala.shape[0] -1, escala.shape[1] - 1):
        print ('{}, {}'.format(x, y))
        if escala[x, y] != 0:
            imdilat[x-1, y-1] = escala[x, y]
            imdilat[x, y-1] = escala[x, y]
            imdilat[x+1, y-1] = escala[x, y]
            imdilat[x-1, y] = escala[x, y]
            imdilat[x, y] = escala[x, y]
            imdilat[x+1, y] = escala[x, y]
            imdilat[x-1, y+1] = escala[x, y]
            imdilat[x, y+1] = escala[x, y]
            imdilat[x+1, y+1] = escala[x, y]

count = count + 1
print(count)
        
# erosao navegar em posicao dentro da matriz [w] = largura, [h] = altura
#Erosao


for x in range(escala.shape[0] -1):
    for y in range (escala.shape[1] -1):
        if (imerosao[x-1,y-1] != 0) and (imerosao[x, y-1] != 0) and (imerosao[x+1,y-1] != 0) and (imerosao[x-1,y]!= 0) and(imerosao[x-1,y]!=0) and (imerosao[x,y]!=0) and (imerosao[x+1,y]!=0) and (imerosao[x-1,y+1]!=0) and (imerosao[x,y+1]!=0) and (imerosao[x+1,y+1]!=0):
            imerosao[x, y] = 255
        #aplicando Dilatacao em cima do result da erosao = opening
        if imerosao[x,y] != 0:
            opening[x-1,y-1] = escala[x,y]
            opening[x,y-1] = escala[x,y]
            opening[x+1,y-1] = escala[x,y]
            opening[x-1,y] = escala[x,y]
            opening[x,y] = escala[x,y]
            opening[x+1,y] = escala[x,y]
            opening[x-1,y+1] = escala[x,y]
            opening[x,y+1] = escala[x,y]
            opening[x+1,y+1] = escala[x,y]
count = count + 1
print(count)

    #Aplicando Erosao em cima da Dilatacao = fechamento, apartir do result da dilatacao da escala[x,y]

for x in range (escala.shape[0] -1):
    for y in range (escala.shape[1] -1):
        if ((imdilat[x-1,y-1]!=0) and
            (imdilat[x,y-1]) and
            (imdilat[x+1,y-1]!=0) and
            (imdilat[x-1,y]!=0) and
            (imdilat[x,y]!=0) and
            (imdilat[x+1,y]!=0) and
            (imdilat[x-1,y+1]!=0) and
            (imdilat[x,y+1]!=0) and
            (imdilat[x+1,y+1]!=0)):

            closed[x-1, y-1] = escala[x,y]
            closed[x,   y-1] = escala[x,y]
            closed[x+1, y-1] = escala[x,y]
            closed[x-1, y] = escala[x,y]
            closed[x,   y] = escala[x,y]
            closed[x+1, y] = escala[x,y]
            closed[x-1, y+1] = escala[x,y]
            closed[x,   y+1] = escala[x,y]
            closed[x+1, y+1] = escala[x,y]
count = count + 1
print(count)    

#Roberts
"""
for
		rx1 = 0*gray_imagem2[i,j-1]
		rx2 = -1*gray_imagem2[i,j-1]
		rx3 = 1*gray_imagem2[i-1,j-1]
		rx4 = 0*gray_imagem2[]
		ry5 = 1*gray_imagem2[i+1,j-1]
		ry6 = 0*gray_imagem2[i-1,j-]
		ry7 = 0*gray_imagem2[]
		ry8 = -1*gray_imagem2[]

		pixelv = rx1+rx2+rx3+rx4
		pixelh = ry5+ry6+ry7+ry8

		g = sqrt(pixelv+pixelh)**2
		if g >pixelv or pixelh
		rbs = 255
#Robinson
"""
cv2.imshow('original', original)
cv2.imshow('deteccao',imgres)
cv2.imshow('dilatacao', imdilat)
cv2.imshow('erosao', imerosao)
cv2.imshow('opening', opening)
cv2.imshow('fechamento', closed)


cv2.waitKey(0)

