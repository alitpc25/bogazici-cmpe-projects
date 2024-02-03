
# return img, nested list
def read_ppm_file(f):
    fp = open(f)
    fp.readline()  # reads P3 (assume it is P3 file)
    lst = fp.read().split()
    n = 0
    n_cols = int(lst[n])
    n += 1
    n_rows = int(lst[n])
    n += 1
    max_color_value = int(lst[n])
    n += 1
    img = []
    for r in range(n_rows):
        img_row = []
        for c in range(n_cols):
            pixel_col = []
            for i in range(3):
                pixel_col.append(int(lst[n]))
                n += 1
            img_row.append(pixel_col)
        img.append(img_row)
    fp.close()
    return img, max_color_value


# Works
def img_printer(img):
    row = len(img)
    col = len(img[0])
    cha = len(img[0][0])
    for i in range(row):
        for j in range(col):
            for k in range(cha):
                print(img[i][j][k], end=" ")
            print("\t|", end=" ")
        print()


filename = input()
operation = int(input())


# DO_NOT_EDIT_ANYTHING_ABOVE_THIS_LINE

(img, max_color_value) = read_ppm_file(filename)

# OPERATIONS
if operation == 1:
    newMin = int(input())
    newMax = int(input())
    for i in range(len(img)):
        for j in range(len(img[i])):
            for k in range(len(img[i][j])):
                img[i][j][k] = round((img[i][j][k] - 0) / (max_color_value - 0) * (newMax - newMin) + newMin, 4)
# COMPLETED 1


if operation == 2:

    n = len(img[0])
    for k in range(3):
        kthChannelSum = 0
        for i in range(len(img)):
            for j in range(len(img[i])):
                kthChannelSum += img[i][j][k]
        kthChannelMean = kthChannelSum / (n*n)
        kthChannelStandardDevSum = 0
        for i in range(len(img)):
            for j in range(len(img[i])):
                kthChannelStandardDevSum += (img[i][j][k] - kthChannelMean)**2
        kthChannelStandardDev = ((kthChannelStandardDevSum/(n*n))**(0.5)) + (10**(-6))
        for i in range(len(img)):
            for j in range(len(img[i])):
                normalized = (img[i][j][k] - kthChannelMean) / kthChannelStandardDev
                img[i][j][k] = round(normalized, 4)
# COMPLETED 2


if operation == 3:
    for i in range(len(img)):
        for j in range(len(img[i])):
            sum = 0
            for k in range(len(img[i][j])):
                sum+=img[i][j][k]
            sum/= 3
            sum = int(sum)
            img[i][j] = [sum, sum, sum]
# COMPLETED 3


def find_filter_length(f):
    fp = open(f)
    lst = fp.readline().strip().split()
    fp.close()
    return len(lst)

def read_txt_file(f):
    length = find_filter_length(f)
    fp = open(f)
    filter = []
    for r in range(length):
        lst = fp.readline().strip().split()
        filter_row = []
        for c in range(length):
            filter_row.append(float(lst[c]))
        filter.append(filter_row)
    fp.close()
    return filter

# EK

if operation >= 4:
    firstImg = []
    for r in range(len(img[0])):
        img_row = []
        for c in range(len(img[0])):
            pixel_col = []
            for i in range(3):
                pixel_col.append(img[r][c][i])
            img_row.append(pixel_col)
        firstImg.append(img_row)
#
if operation == 4:
    filterName = input()
    stride = int(input())
    kernelMatrix = read_txt_file(filterName)
    kernelHalfLength = int(len(kernelMatrix)/2)

    for k in range(3):
        for i in range(kernelHalfLength, len(firstImg)-kernelHalfLength, stride):
            for j in range(kernelHalfLength, len(firstImg[i])-kernelHalfLength, stride):

                sum = 0
                for r in range(len(kernelMatrix)):
                    for c in range(len(kernelMatrix[r])):
                        sum += firstImg[i-kernelHalfLength+r][j-kernelHalfLength+c][k] * kernelMatrix[r][c]
                if sum >= max_color_value:
                    img[i][j][k] = max_color_value
                elif sum < 0:
                    img[i][j][k] = 0
                else:
                    img[i][j][k] = int(sum)

    img = img[kernelHalfLength:-kernelHalfLength]
    for i in range(len(img)):
        img[i] = img[i][kernelHalfLength:-kernelHalfLength]

    lastImg = []
    for i in range(0,len(img),stride):
        img_row = []
        for j in range(0,len(img),stride):
            pixel_col = []
            for k in range(3):
                pixel_col.append(img[i][j][k])
            img_row.append(pixel_col)
        lastImg.append(img_row)

    img = lastImg

# COMPLETED 4


if operation == 5:
    filterName = input()
    stride = int(input())
    kernelMatrix = read_txt_file(filterName)
    kernelHalfLength = int(len(kernelMatrix)/2)

    paddedImg = []
    for i in range(len(firstImg)+kernelHalfLength*2):
        img_row = []
        for j in range(len(firstImg)+kernelHalfLength*2):
            pixel_col = []
            if i < kernelHalfLength or j < kernelHalfLength or i >= len(firstImg) + kernelHalfLength or j >= len(firstImg) + kernelHalfLength:
                for k in range(3):
                    pixel_col.append(0)
            else:
                for k in range(3):
                    pixel_col.append(firstImg[i-kernelHalfLength][j-kernelHalfLength][k])
            img_row.append(pixel_col)
        paddedImg.append(img_row)

    for k in range(3):
        for i in range(kernelHalfLength, len(paddedImg)-kernelHalfLength, stride):
            for j in range(kernelHalfLength, len(paddedImg[i])-kernelHalfLength, stride):
                sum = 0
                for r in range(len(kernelMatrix)):
                    for c in range(len(kernelMatrix[r])):
                        sum += (paddedImg[i-kernelHalfLength+r][j-kernelHalfLength+c][k] * kernelMatrix[r][c])
                if sum >= max_color_value:
                    img[i-kernelHalfLength][j-kernelHalfLength][k] = max_color_value
                elif sum < 0:
                    img[i-kernelHalfLength][j-kernelHalfLength][k] = 0
                else:
                    img[i-kernelHalfLength][j-kernelHalfLength][k] = int(sum)

    lastImg = []
    for i in range(0,len(img),stride):
        img_row = []
        for j in range(0,len(img),stride):
            pixel_col = []
            for k in range(3):
                pixel_col.append(img[i][j][k])
            img_row.append(pixel_col)
        lastImg.append(img_row)

    img = lastImg

# COMPLETED 5


def pixel(img,r,c):
    if r < 0 or r > len(img) - 1:
        pixel(img,0,c+1)
        return
    if c > len(img) - 1:
        return
    if c % 2 == 0:
        if r == 0:
            checkerLeft(img,r,c)
        checkerDown(img,r,c)
        pixel(img,r+1,c)
    else:
        if r == 0:
            checkerLeft(img,len(img)-r-1,c)
        checkerUp(img,len(img)-r-1,c)
        pixel(img,r+1,c)

def compare(pixel1,pixel2):
    isSame = True
    for k in range(3):
        if abs(pixel1[k] - pixel2[k]) >= myRange:
            isSame = False
            break
    return isSame

def checkerDown(img, i, j):
    if i < 0 or j < 0 or i > len(img)-1 or j > len(img)-1:
        return
    if 0 <= i <= len(img)-2:
        if compare(img[i][j], img[i+1][j]):
            for k in range(3):
                img[i+1][j][k] = img[i][j][k]

def checkerUp(img, i, j):
    if i < 0 or j < 0 or i > len(img)-1 or j > len(img)-1:
        return
    if 1 <= i <= len(img)-1:
        if compare(img[i][j], img[i-1][j]):
            for k in range(3):
                img[i-1][j][k] = img[i][j][k]

def checkerLeft(img, i, j):
    if i < 0 or j < 0 or i > len(img)-1 or j > len(img)-1:
        return
    if 1 <= j <= len(img)-1:
        if compare(img[i][j], img[i][j-1]):
            for k in range(3):
                img[i][j][k] = img[i][j-1][k]

if operation == 6:
    myRange = int(input())
    pixel(img,0,0)
#     COMPLETED 6

#
def channel(img,r,c,k):
    if k == 0:
        if r < 0 or r > len(img) - 1:
            channel(img,0,c+1,k)
            return
        if c > len(img) - 1:
            channel(img,0,len(img)-1,k+1)
            return
        if c % 2 == 0:
            if r == 0:
                checkerLeftChannel(img,r,c,k)
            checkerDownChannel(img,r,c,k)
            channel(img,r+1,c,k)
        else:
            if r == 0:
                checkerLeftChannel(img,len(img)-r-1,c,k)
            checkerUpChannel(img,len(img)-r-1,c,k)
            channel(img,r+1,c,k)
    elif k == 1:
        if r < 0 or r > len(img) - 1:
            if c % 2 == 0:
                channel(img,0,c-1,k)
            else:
                channel(img,len(img)-1,c-1,k)
            return
        if c < 0:
            channel(img,0,0,k+1)
            return
        if r == 0 and c == len(img)-1:
            checkerOutChannel(img,r,c,k)
        if c % 2 == 0:
            if r == len(img)-1:
                checkerRightChannel(img,r,c,k)
            checkerUpChannel(img,r,c,k)
            channel(img,r-1,c,k)
        else:
            if r == 0:
                checkerRightChannel(img,r,c,k)
            checkerDownChannel(img,r,c,k)
            channel(img,r+1,c,k)
    else:
        if r < 0 or r > len(img) - 1:
            channel(img,0,c+1,k)
            return
        if c > len(img) - 1:
            return
        if r == 0 and c == 0:
            checkerOutChannel(img,r,c,k)
        if c % 2 == 0:
            if r == 0:
                checkerLeftChannel(img,r,c,k)
            checkerDownChannel(img,r,c,k)
            channel(img,r+1,c,k)
        else:
            if r == 0:
                checkerLeftChannel(img,len(img)-r-1,c,k)
            checkerUpChannel(img,len(img)-r-1,c,k)
            channel(img,r+1,c,k)

def comparePixel(pixel1,pixel2,channel):
    isSame = True
    if abs(pixel1[channel] - pixel2[channel]) >= myRange:
        isSame = False
    return isSame

def compareChannel(pixel,channel1,channel2):
    isSame = True
    if abs(pixel[channel1] - pixel[channel2]) >= myRange:
        isSame = False
    return isSame

def checkerDownChannel(img, i, j, k):
    if i < 0 or j < 0 or i > len(img)-1 or j > len(img)-1:
        return
    if 0 <= i <= len(img)-2:
        if comparePixel(img[i][j], img[i+1][j],k):
            img[i+1][j][k] = img[i][j][k]

def checkerUpChannel(img, i, j, k):
    if i < 0 or j < 0 or i > len(img)-1 or j > len(img)-1:
        return
    if 1 <= i <= len(img)-1:
        if comparePixel(img[i][j], img[i-1][j],k):
            img[i-1][j][k] = img[i][j][k]

def checkerLeftChannel(img, i, j, k):
    if i < 0 or j < 0 or i > len(img)-1 or j > len(img)-1:
        return
    if 1 <= j <= len(img)-1:
        if comparePixel(img[i][j], img[i][j-1], k):
            img[i][j][k] = img[i][j-1][k]

def checkerRightChannel(img, i, j, k):
    if i < 0 or j < 0 or i > len(img)-1 or j > len(img)-1:
        return
    if 0 <= j <= len(img)-2:
        if comparePixel(img[i][j], img[i][j+1], k):
            img[i][j][k] = img[i][j+1][k]

def checkerOutChannel(img, i, j, k):
    if compareChannel(img[i][j], k, k-1):
        img[i][j][k] = img[i][j][k-1]

if operation == 7:
    myRange = int(input())
    channel(img,0,0,0)
#  COMPLETED 7

img_printer(img)

# DO_NOT_EDIT_ANYTHING_BELOW_THIS_LINE

