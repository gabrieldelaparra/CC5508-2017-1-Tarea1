def getEncodedNbits(nbits):
    encodedNbits = []
    tmp = int(nbits)
    for i in range(0,4):
        encodedNbits.append(tmp & 1)
        tmp = tmp >> 1

    return encodedNbits
