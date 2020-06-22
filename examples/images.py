#!/bin/python3
import os
import sys

# import realative 'stippy' python project
script_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(script_dir + '/../')
import stippy

def display(node, image):
    print(str(node.id) + ' ' + image.platform + ' ' + image.geocode
        + ' ' + image.source + ' ' + str(image.timestamp))

    for file in image.files:
        print('    ' + str(file.subdataset))

if __name__ == '__main__':
    host_addr = '127.0.0.1:15606'

    # print Sentinel-2 images with > 90% pixel coverage
    #   and < 10% cloud coverage
    print('-----NODE IMAGES 1-----')
    stip_iter = stippy.list_images(host_addr, 'test', platform='Sentinel-2', 
        min_pixel_coverage=0.9, max_cloud_coverage=0.1)

    for (node, image) in stip_iter:
        display(node, image)

    # print images from only the queried 
    #   node for all geohashes starting with '9q'
    print('-----NODE IMAGES 2-----')
    stip_iter = stippy.list_node_images(host_addr,
        'test', recurse=True, geocode='9q')

    for (node, image) in stip_iter:
        display(node, image)

    # print all images from 2018 
    print('-----NODE IMAGES 3-----')
    stip_iter = stippy.list_images(host_addr, 'test',
        start_timestamp=1514764800, end_timestamp=1546300800)

    for (node, image) in stip_iter:
        display(node, image)
