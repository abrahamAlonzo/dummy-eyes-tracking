import pyzbar.pyzbar as pyzbar


def decode(im) : 
    # Find barcodes and QR codes
    decodedObjects = pyzbar.decode(im)

    # Print results
    for obj in decodedObjects:
        print('Type : ', obj.type)
        print('Data : ', obj.data,'\n')

    return decodedObjects

if __name__ == "__main__":
    pass
else:
    print("Decoder as library")