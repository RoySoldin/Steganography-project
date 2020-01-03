from Image_Steganography import np


def bytesToArray(byte_data):
    byte_array = np.frombuffer(byte_data, dtype=np.uint8)
    return np.unpackbits(byte_array)

def arrayToBytes(bit_array):
    byte_array = np.packbits(bit_array)
    return byte_array.tobytes()

def readFile(file_path):
    file_bytes = open(file_path, "rb").read()
    return bytesToArray(file_bytes)

def writeFile(file_path, file_bit_array):
    bytes_data = arrayToBytes(file_bit_array)
    f = open(file_path, 'wb')
    f.write(bytes_data)
    f.close()