from PIL import Image
import numpy as np

name = "uBody_Drg1AF_c051_Albedo.png"
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

    block9 = getbigblock(data[0:8, 1024:1152])
    block10 = getbigblock(data[0:8, 1152:1280])
    block11 = getbigblock(data[0:8, 1280:1408])
    block12 = getbigblock(data[0:8, 1408:1536])
    block13 = getbigblock(data[0:8, 1536:1664])
    block14 = getbigblock(data[0:8, 1664:1792])
    block15 = getbigblock(data[0:8, 1792:1920])
    block16 = getbigblock(data[0:8, 1920:2048])

    newblock_1 = np.vstack((np.hstack((block3, block4)), np.hstack((block1, block2))))
    newblock_2 = np.vstack((np.hstack((block7, block8)), np.hstack((block5, block6))))

    newblock_3 = np.vstack((np.hstack((block11, block12)), np.hstack((block9, block10))))
    newblock_4 = np.vstack((np.hstack((block15, block16)), np.hstack((block13, block14))))

    newblock = np.vstack((np.vstack((newblock_4, newblock_3)), np.vstack((newblock_2, newblock_1))))

    return newblock


def combineVblock(data):
    block1 = combinelineblock(data[0:8, 0:2048])
    block2 = combinelineblock(data[8:16, 0:2048])
    block3 = combinelineblock(data[16:24, 0:2048])
    block4 = combinelineblock(data[24:32, 0:2048])

    newblock = np.hstack((np.vstack((block3, block4)), np.vstack((block1, block2))))
    return newblock


replace = temp.copy()


'''
block1 = combineVblock(temp[0:32, 0:2048])
block2 = combineVblock(temp[1024:1056, 0:2048])
block = np.vstack((block1, block2))
test = Image.fromarray(block)
test.show()

'''

for i in range(1024):
    if i % 32 == 0:
        block1 = combineVblock(temp[i:i+32, 0:2048])
        block2 = combineVblock(temp[1024+i:1024+i+32, 0:2048])
        block = np.vstack((block1, block2))

        replace[0:2048, 2048-i*2-64:2048-i*2] = block            
       


image = Image.fromarray(replace)
image.save("new_"+name)
