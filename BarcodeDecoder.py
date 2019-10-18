import pyzbar.pyzbar as pyzbar


# def decode(im) : 
#     # Find barcodes and QR codes
#     decodedObjects = pyzbar.decode(im)

#     # Print results
#     for obj in decodedObjects:
#         print('Type : ', obj.type)
#         print('Data : ', obj.data,'\n')

#     return decodedObjects


def decode(im) : 
    # Find barcodes and QR codes
    decodedObjects = pyzbar.decode(im)

    # Print results
    data = []
    for obj in decodedObjects:
        print('Type : ', obj.type)
        print('Data : ', obj.data,'\n')
        data.append(obj.data.decode("utf-8") )
    if len(data) != 0:
        return data[0]
    else:
        return ''


if __name__ == "__main__":
    pass
else:
    print("Decoder as library")