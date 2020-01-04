import numpy as np
import encode_decoder as encodeDecode
import imageHandler as imgHandler
import fileHandler as fileHandler
import os

import argparse

MAX_VALUE = 255
HEADER_LEN = 4*8


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

            image, shape_orig = imgHandler.image_reader(img_path)
            file = fileHandler.file_reader(file_path)
            file_len = file.shape[0]
            len_array = np.array([file_len], dtype=np.uint32).view(np.uint8)
            len_array = np.unpackbits(len_array)
            img_len = image.shape[0]

            if file_len >= img_len - HEADER_LEN:  # 4 bytes are used to store file length
                print("File too big, error")
                return
            else:
                tmp = file
                file = np.random.randint(2, size=img_len, dtype=np.uint8)
                file[HEADER_LEN:HEADER_LEN+file_len] = tmp

            file[:HEADER_LEN] = len_array
            encoded_data = encodeDecode.data_encoder(image, file)

            imgHandler.image_writer(output_path, encoded_data, shape_orig)
            print("Image encoded")
            return

        if args.decode:
            img_path = args.image
            if not os.path.isfile(img_path):
                print("Image file does not exist")
                return
            file_path = args.file
            encoded_data, shape_orig = imgHandler.image_reader(img_path)
            data = encodeDecode.data_decoder(encoded_data)
            el_array = np.packbits(data[:HEADER_LEN])
            extracted_len = el_array.view(np.uint32)[0]
            data = data[HEADER_LEN:extracted_len+HEADER_LEN]
            fileHandler.file_writer(file_path, data)
            print("Image decoded")
            return

        print("Error, no action specified!")
        return

    print("Error, image or file not specified")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Hide files inside a PNG image and extract them back')
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '--encode',
        action="store_true")
    group.add_argument(
        '--decode',
        action="store_true")
    parser.add_argument(
        '--image',
        help='Path to an image to use for hiding or file extraction')
    parser.add_argument(
        '--file',
        help='Path to the file with the data to hide or to extract')
    parser.add_argument(
        '--output',
        help='Path where to save the encoded image.',
        default='encoded.png')

    _main(parser.parse_args())