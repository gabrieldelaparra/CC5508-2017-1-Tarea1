    #Convertir cada caracter a bits y agregarlos a una lista:
    for char in text:
        byte = []
        tmp = ord(char)
        for i in range(0,8):
            byte.append(tmp & 1)
            tmp = tmp >> 1
        # Agregar byts a la lista:
        [encodedText.append(i) for i in byte[::-1]]