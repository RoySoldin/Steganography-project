from Image_Steganography import np
from imageio import imread, imwrite

def readImage(img_path):
    img = np.array(imread(img_path), dtype=np.uint8)
    orig_shape = img.shape
    return img.flatten(), orig_shape

def writeImage(img_path, img_data, shape):
    img_data = np.reshape(img_data, shape)
    imwrite(img_path, img_data)
