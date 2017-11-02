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