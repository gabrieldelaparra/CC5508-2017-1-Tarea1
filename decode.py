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