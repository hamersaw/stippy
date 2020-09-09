#!/bin/python3
import os
import sys

# import realative 'stippy' python project
script_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(script_dir + '/../')
import stippy

if __name__ == '__main__':
    host_addr = '127.0.0.1:15606'

    # process Sentinel-2 images starting with geocode '9xjk'
    print('-----IMAGES-----')
    stip_iter = stippy.list_images(host_addr, 'test',
        geocode='9xjk', recurse=True)
    for (node, image) in stip_iter:
        if len(image.files) != 4:
            continue

        print(image.geocode)
        dataset = stippy.read_file(node.xferAddr, image.files[3].path)
