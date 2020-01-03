from Image_Steganography import np,MAX_VALUE

def encodeData(image, file_data):
    or_mask = file_data
    and_mask = np.zeros_like(or_mask)
    and_mask = (and_mask + MAX_VALUE - 1) + or_mask 
    res = np.bitwise_or(image, or_mask)
    res = np.bitwise_and(res, and_mask)
    return res

def decodeData(encoded_data):
    out_mask = np.ones_like(encoded_data)
    output = np.bitwise_and(encoded_data, out_mask)
    return output