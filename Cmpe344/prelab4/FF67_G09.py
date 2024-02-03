import cache_module
import numpy

# Prepare an RGB image containing 3 colour channels.
ROW = 1024
COL = 2048
Channel = 3
image = numpy.random.randint(0, 256, size=(ROW, COL, Channel), dtype=numpy.int64)

# Prepare a mask for the convolution operation.
mask_size = 3
up = 10
down = -10
mask = numpy.random.randint(down, up + 1, size=(mask_size, mask_size), dtype=numpy.int64)

# Prepare an empty result image. You will fill this empty array with your code.
result = numpy.zeros([ROW, COL, Channel], dtype=numpy.int64)

# Configuration for the cache simulator module.
l3 = ["L3", 16384, 16, 64, "LRU"]
l2 = ["L2", 4096, 8, 64, "LRU"]
l1 = ["L1", 1024, 4, 64, "LRU"]
m = 256 * 1024 * 1024
cm = cache_module.cache_module(l1, l2, l3, m)

###### WRITE YOUR CODE BELOW. ######

# 1. Load the image into the memory
ind = 0;
val = 0;
for r in range(0, ROW):
    for c in range(0, COL):
        for ch in range(0, Channel):
            val = image[r][c][ch];
            cm.write(ind+7, val) #put the last cell of the memory, since 256 = 2^8.
            ind+=8


# 2. Traverse the image array and apply the mask. Write the results into the memory through the write function. Do not fill the result array in this step.
ind = 0;
r = 0;
c = 0;
while(ind<ROW*COL*Channel*8):
    val = 0;
    mask_r = 0;
    for nr in range(-1, 2):
        mask_c=0
        for nc in range(-1, 2):
            if(nr+r>=0 and nr+r<ROW and nc+c>=0 and nc+c<COL):
                val+=cm.read(ind+7+nr*COL*Channel*8+nc*8*Channel) * mask[mask_r][mask_c]
            mask_c+=1
        mask_r+=1
    numbers = list((val >> i) & 0xFF for i in range(0,64,8))
    numbers.reverse()
    for i in range(0,8):
        cm.write(ind+ROW*COL*Channel*8+i, numbers[i])
    ind+=8
    r = ind // (COL*Channel*8)
    c = ((ind - r*COL*Channel*8) // (Channel*8))

# 3. Load the result image from memory through the read function.
ind = ROW*COL*Channel*8;
val = 0;

for r in range(0, ROW):
    for c in range(0, COL):
        for ch in range(0, Channel):
            val = 0;
            for i in range(0,8):
                val += cm.read(ind+i)*(2**((7-i)*8))
            result[r][c][ch] = val%256;
            ind+=8

###### WRITE YOUR CODE ABOVE. ######

cm.finish()