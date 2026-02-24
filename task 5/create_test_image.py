import cv2
import numpy as np

img = np.zeros((500,500,3),np.uint8)

for i in range(500):
    for j in range(500):
        img[i][j][0] = i % 256
        img[i][j][1] = j % 256
        img[i][j][2] = (i+j) % 256

cv2.imwrite('image.jpg',img)

print('test image created')
