import numpy as np
from imageio import imread, imwrite
import encode_decoder as encodeDecode
import imageHandler as imgHandler
import fileHandler as fileHandler
import os

import argparse

MAX_VALUE = 255 # max uint value per pixel per channel
HEADER_LEN = 4*8 # uint32 bit length


def _main(args):
    if args.image is not None and args.file is not None:
        if args.encode:
            img_path = args.image
            file_path = args.file
            if not os.path.isfile(img_path):
                print("Image file does not exist")
                return
            if not os.path.isfile(file_path):
                print("File does not exist")
                return

            output_path = args.output
            extension = os.path.splitext(output_path)[1][1:]
            if extension == '':  # if no extension, append png
                output_path = output_path + '.png'
            elif extension != 'png':  # replace the wrong extension with png
                li = output_path.rsplit(extension, 1)
                output_path = 'png'.join(li)

            image, shape_orig = imgHandler.readImage(img_path)
            file = fileHandler.readFile(file_path)
            file_len = file.shape[0]
            len_array = np.array([file_len], dtype=np.uint32).view(np.uint8)
            len_array = np.unpackbits(len_array)
            img_len = image.shape[0]

            if file_len >= img_len - HEADER_LEN:  # 4 bytes are used to store file length
                print("File too big, error")
                return
            else:  #  Insert padding. Using random padding, otherwise values would all be even if padding with zeros (could be noticed in histogram).
                tmp = file
                file = np.random.randint(2, size=img_len, dtype=np.uint8)
                file[HEADER_LEN:HEADER_LEN+file_len] = tmp
                # file = np.pad(file, (HEADER_LEN,img_len - file_len - HEADER_LEN), 'constant', constant_values=(0, 0))

            file[:HEADER_LEN] = len_array
            encoded_data = encodeDecode.encodeData(image, file)

            imgHandler.writeImage(output_path, encoded_data, shape_orig)
            print("Image encoded")
            return

        if args.decode:
            img_path = args.image
            if not os.path.isfile(img_path):
                print("Image file does not exist")
                return
            file_path = args.file
            encoded_data, shape_orig = imgHandler.readImage(img_path)
            data = encodeDecode.decodeData(encoded_data)
            el_array = np.packbits(data[:HEADER_LEN])
            extracted_len = el_array.view(np.uint32)[0]
            data = data[HEADER_LEN:extracted_len+HEADER_LEN]
            fileHandler.writeFile(file_path, data)
            print("Image decoded")
            return

        print("Error, no action specified!")
        return

    print("Error, image or file not specified")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Conceal small files inside a PNG image and extract them back')
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '-e',
        '--encode',
        help='If present the script will conceal the file in the image and produce a new encoded image',
        action="store_true")
    group.add_argument(
        '-d',
        '--decode',
        help='If present the script will decode the concealed data in the image and produce a new file with this data',
        action="store_true")
    parser.add_argument(
        '-i',
        '--image',
        help='Path to an image to use for concealing or file extraction')
    parser.add_argument(
        '-f',
        '--file',
        help='Path to the file to conceal or to extract')
    parser.add_argument(
        '-o',
        '--output',
        help='Path where to save the encoded image. Specify only the file name, or use .png extension; png extension will be added automatically',
        default='encoded.png')

    _main(parser.parse_args())