from PIL import Image
import numpy as np

name = "uAcc_Drg1AF_c051_Albedo.png"
image = Image.open(name)

temp = np.asarray(image)
temp = temp.copy()
temp.setflags(write=1)


print(temp.shape)

def swap(img, first, second):
    temp = img[first[0]:first[1], first[2]:first[3]].copy()
    img[first[0]:first[1], first[2]:first[3]] = img[second[0]:second[1], second[2]:second[3]]
    img[second[0]:second[1], second[2]:second[3]] = temp


def getblock(data):
    block1 = data[0:8, 0:8]
    block2 = data[0:8, 8:16]
    block3 = data[0:8, 16:24]
    block4 = data[0:8, 24:32]

    newblock = np.vstack((np.hstack((block2, block4)), np.hstack((block1, block3))))
    return newblock

def getbigblock(data):
    block1 = getblock(data[0:8, 0:32])
    block2 = getblock(data[0:8, 32:64])
    block3 = getblock(data[0:8, 64:96])
    block4 = getblock(data[0:8, 96:128])

    newblock = np.vstack((np.vstack((block4, block3)), np.vstack((block2, block1))))
    
    return newblock

def combinelineblock(data):
    block1 = getbigblock(data[0:8, 0:128])
    block2 = getbigblock(data[0:8, 128:256])
    block3 = getbigblock(data[0:8, 256:384])
    block4 = getbigblock(data[0:8, 384:512])
    block5 = getbigblock(data[0:8, 512:640])
    block6 = getbigblock(data[0:8, 640:768])
    block7 = getbigblock(data[0:8, 768:896])
    block8 = getbigblock(data[0:8, 896:1024])

    newblock_1 = np.vstack((np.hstack((block3, block4)), np.hstack((block1, block2))))
    newblock_2 = np.vstack((np.hstack((block7, block8)), np.hstack((block5, block6))))

    newblock = np.vstack((newblock_2, newblock_1))

    return newblock


def combineVblock(data):
    block1 = combinelineblock(data[0:8, 0:1024])
    block2 = combinelineblock(data[8:16, 0:1024])
    block3 = combinelineblock(data[16:24, 0:1024])
    block4 = combinelineblock(data[24:32, 0:1024])

    newblock = np.vstack((np.vstack((block1, block2)), np.vstack((block3, block4))))
    return newblock


replace = temp.copy()

for i in range(1024):
    if i % 32 == 0:
        block = combineVblock(temp[i:i+32, 0:1024])

        replace[0:1024, 1024-i-32:1024-i] = block            
        


image = Image.fromarray(replace)
image.save("new_"+name)

