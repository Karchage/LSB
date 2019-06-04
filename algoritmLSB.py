from PIL import Image, ImageDraw, ImageFile
def hide(imagePath, text):
    image = readImage(imagePath)
    if (not image):
        return False
    pix = image.load()
    draw = ImageDraw.Draw(image)
    i = 0
    j = 0
    k = 0
    rgb = [-1, -1, -1]
    for item in text:
        bitItem = textToBits(item)
        for bit in bitItem:
            rgb[k] = changeLastBit(pix[i,j][k], bit)

            k += 1
            if( k == 3):
                draw.point((i,j), (rgb[0], rgb[1], rgb[2]))
                rgb = [-1, -1, -1]
                k = 0
                j += 1
            if(j == image.size[1]):
                i += 1
                j = 0
                if(i == image.size[0]):
                    return True

        if(i == image.size[0]):
                return True
    
    if(k != 0):
        if(rgb[1] != -1):
            draw.point((i,j), (rgb[0], rgb[1], changeLastBit(pix[i,j][2], 1)))
            k = 0
        elif(rgb[2] != -1):
            draw.point((i,j), (rgb[0], changeLastBit(pix[i,j][1], 1), pix[i,j][2]))
            k = 0
    else:
        draw.point((i,j), (changeLastBit(pix[i,j][0], 1), pix[i,j][1], pix[i,j][2]))

    image.save("crypt.png", "PNG", quality=100, optimize = False, progressive = False)
    del draw


def show(imagePath):
    image = readImage(imagePath)
    if (not image):
        return None
    pix = image.load()
    text = ''
    bitText = ''
    for i in range(0, image.size[0]):
        for j in range(0, image.size[1]) :
            for k in range(0, 3):
                bits = intToBits(pix[i,j][k])
                for item in bits:
                    pass
                bitText += item
                if(len(bitText) == 8):
                    try:
                        text += textFromBits(bitText)
                        bitText = ''
                    except:
                        return text
    return text

def readImage(img):
    try:
        ImageFile.MAXBLOCK = 2 ** 20
        image = Image.open(img)
    except:
        return None
    return image

def changeLastBit(color, bit):
    return int(intFromBits(changeLastBits(intToBits(color), bit)))

def textToBits(text, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int.from_bytes(text.encode(encoding, errors), 'big'))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))

def textFromBits(bits, encoding='utf-8', errors='surrogatepass'):
    n = int(bits, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(encoding, errors) or '\0'

def intToBits(number):
    return '{0:b}'.format(number)

def intFromBits(bits):
    return int(bits, 2)

def changeLastBits(bits, bitToReplace):
    i = -1
    for item in bits:
        i += 1
    return str(bits[:i] + str(bitToReplace))