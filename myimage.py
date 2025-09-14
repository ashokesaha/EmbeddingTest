import sys
import numpy as np
import matplotlib.pyplot as plt

np.set_printoptions(threshold=sys.maxsize)

fig, axes = plt.subplots(2, 2, figsize=(8, 8))

image = np.zeros((32, 32), dtype=np.uint8)
image[16, 4:28] = 200 

plt.sca(axes[0,0])
plt.imshow(image, cmap="gray", vmin=0, vmax=255)

MAT = np.identity(32, dtype=np.uint8)
MAT[0][16] = 1
MAT[0][0] = 0
img2 = MAT @ image
plt.sca(axes[0,1])
plt.imshow(img2, cmap="gray", vmin=0, vmax=255)



plt.show()
