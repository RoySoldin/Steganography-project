from LSB_Steganography import np
from imageio import imread, imwrite


def image_reader(path):
    img = np.array(imread(path), dtype=np.uint8)
    orig_shape = img.shape
    return img.flatten(), orig_shape


def image_writer(path, data, shape):
    data = np.reshape(data, shape)
    imwrite(path, data)
