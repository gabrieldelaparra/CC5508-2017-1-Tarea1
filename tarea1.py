from argparse import ArgumentParser, RawTextHelpFormatter
from skimage import io

END_OF_FILE = "$EOF"

def getMask(nbits):
    return 255-(2**(int(nbits)-1))

def getEncodedNbits(nbits):
    encodedNbits = []
    tmp = int(nbits)
    for i in range(0,4):
        encodedNbits.append(tmp & 1)
        tmp = tmp >> 1

    return encodedNbits

def getEncodedTextLength(text):
    return ""

def getEncodedText(nbits, text):
    encodedText = []

    #Convertir cada caracter a bits y agregarlos a una lista:
    for char in text:
        byte = []
        tmp = ord(char)
        for i in range(0,8):
            byte.append(tmp & 1)
            tmp = tmp >> 1
        # Agregar byts a la lista:
        [encodedText.append(i) for i in byte[::-1]]

    # Convertir cada caracter a bits y agregarlos a una lista:
    for char in END_OF_FILE:
        byte = []
        tmp = ord(char)
        for i in range(0, 8):
            byte.append(tmp & 1)
            tmp = tmp >> 1
        # Agregar byts a la lista:
        [encodedText.append(i) for i in byte[::-1]]

    #Insertar al inicio los NBits para poder después decriptar:
    [encodedText.insert(0, i) for i in getEncodedNbits(nbits)]

    return encodedText

def bitstring_to_bytes(s):
    return int(s, 2).to_bytes(len(s) // 8, byteorder='big')

def decodeText(encodedText):
    encodedTextNoBits = encodedText
    bitString = "".join([str(i) for i in encodedTextNoBits])
    decodedText = str(bitstring_to_bytes(bitString))[2:-1]
    return decodedText

def decode(imageFilename):
    image = io.imread(imageFilename)
    encodedText = []
    textCount = 0
    nbits = 0
    for row in range(0,len(image)):
        for column in range(0,len(image[row])):
            if textCount < 4:
                encodedText.append(image[row][column] & 1)
            else:
                if textCount == 4:
                    nbits = 8*encodedText[0] + 4*encodedText[1] + 2*encodedText[2]+ 1*encodedText[3]

                encodedText.append((image[row][column] >> (nbits-1)) & 1)
                if((textCount+5)%8 == 0 and textCount > 36):
                    if(decodeText(encodedText[-32:]) == END_OF_FILE):
                        return decodeText(encodedText[4:-32])

            textCount += 1

def encode(imageFilename, textFilename, nbits):
    image = io.imread(imageFilename)
    text = open(textFilename,'r').read()
    mask = getMask(nbits)
    encodedText = getEncodedText(nbits, text)

    textCount = 0
    for row in range(0,len(image)):
        for column in range(0,len(image[row])):
            #TODO: Check que el texto entre en la imagen; Tirar exception;
            if(textCount < len(encodedText)):
                if(textCount < 4):
                    image[row][column] = (image[row][column] & getMask(1)) | (encodedText[textCount])
                else:
                    image[row][column] = (image[row][column] & mask) | (encodedText[textCount] << int(nbits)-1)

                textCount += 1

    io.imsave(imageFilename.replace(".png","_out.png"),image)

def main():
    parser = ArgumentParser(prog="Esteganografía",
        formatter_class=RawTextHelpFormatter,
        description="Esteganografía: Codificar texto dentro de una imágen."
        "\n\nCodificar text.txt en image.jpg usando 2 LSB será:\n"
        ">> python tarea_1.py --encode --image image.jpg --text text.txt --nbits 2"
        "\n\nPara decodificar será:\n"
        ">>python tarea_1.py --decode --image imagen.jpg")

    parser.add_argument('-e', '--encode',
                        dest='encode',
                        action='store_true',
                        help='Codificar texto dentro de una imagen')

    parser.add_argument('-d', '--decode',
                        dest='decode',
                        action='store_true',
                        help='Decodificar el texto de una imagen')

    parser.add_argument('-n', '--nbits',
                        dest='nbits',
                        action='store',
                        help='Número de bits menos significativos a ser usados')

    parser.add_argument('-i', '--image',
                        dest='imageFilename',
                        action='store',
                        help='Imágen sobre la cual se codificará el texto')

    parser.add_argument('-t', '--text',
                        dest='textFilename',
                        action='store',
                        help='Texto para codificar')

    args = parser.parse_args()
    
    print(args)

    if args.encode:
        encode(args.imageFilename, args.textFilename, args.nbits)
    if args.decode:
        print(decode(args.imageFilename))

if __name__ == "__main__":
    main()
