from LSB_Steganography import np


def bytes_to_array(byte_data):
    byte_array = np.frombuffer(byte_data, dtype=np.uint8)
    return np.unpackbits(byte_array)


def array_to_bytes(bit_array):
    byte_array = np.packbits(bit_array)
    return byte_array.tobytes()


def file_reader(file_path):
    file_bytes = open(file_path, "rb").read()
    return bytes_to_array(file_bytes)


def file_writer(file_path, file_bit_array):
    bytes_data = array_to_bytes(file_bit_array)
    f = open(file_path, 'wb')
    f.write(bytes_data)
    f.close()