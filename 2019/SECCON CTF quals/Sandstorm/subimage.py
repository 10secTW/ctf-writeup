#!/usr/bin/env python3
from PIL import Image

orig = Image.open('imgs/sandstorm.png')
pixelMap = orig.load()

for level in range(1, 8):

    img = Image.new(orig.mode, orig.size)
    pixelsNew = img.load()
    for block_i in range(0, img.size[0]//8):
        for block_j in range(0, img.size[1]//8):
            for i in range(8):
                for j in range(8):
                    idx_i = block_i*8+i
                    idx_j = block_j*8+j
                    if level == 1:
                        if j == 0 and i == 0:
                            pixelsNew[idx_i,idx_j] = pixelMap[idx_i,idx_j]
                        else: pixelsNew[idx_i,idx_j] = (0,0,0,255)
                    elif level == 2:
                        if j == 0 and (i == 4 or i == 0):
                            pixelsNew[idx_i,idx_j] = pixelMap[idx_i,idx_j]
                        else: pixelsNew[idx_i,idx_j] = (0,0,0,255)
                    elif level == 3:
                        if j % 4 == 0 and i % 4 == 0:
                            pixelsNew[idx_i,idx_j] = pixelMap[idx_i,idx_j]
                        else: pixelsNew[idx_i,idx_j] = (0,0,0,255)
                    elif level == 4:
                        if j % 4 == 0 and i % 2 == 0:
                            pixelsNew[idx_i,idx_j] = pixelMap[idx_i,idx_j]
                        else: pixelsNew[idx_i,idx_j] = (0,0,0,255)
                    elif level == 5:
                        if j % 2 == 0 and i % 2 == 0:
                            pixelsNew[idx_i,idx_j] = pixelMap[idx_i,idx_j]
                        else: pixelsNew[idx_i,idx_j] = (0,0,0,255)
                    elif level == 6:
                        if j % 2 == 0:
                            pixelsNew[idx_i,idx_j] = pixelMap[idx_i,idx_j]
                        else: pixelsNew[idx_i,idx_j] = (0,0,0,255)
                    else:
                        pixelsNew[idx_i,idx_j] = pixelMap[idx_i,idx_j]

    img.save('imgs/level'+str(level)+'.png')
    #img.show()
