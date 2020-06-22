#!/bin/python3
import os
import sys

# import realative 'stippy' python project
script_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(script_dir + '/../')
import stippy

def process_pair(a_image, b_image):
    print('  ' + a_image.geocode + ' ' + str(a_image.timestamp)
        + ' ' + str(b_image.timestamp))

if __name__ == '__main__':
    host_addr = '127.0.0.1:15606'

    # print nodes
    nodes = stippy.list_nodes(host_addr)
    for node in nodes:
        # initailize image iterators
        a_iter = stippy.list_node_images(node.rpcAddr,
            'test', platform='MODIS')
        b_iter = stippy.list_node_images(node.rpcAddr,
            'test', platform='Sentinel-2')

        try:
            # initialize images
            (_, a_image) = a_iter.__next__()
            (_, b_image) = b_iter.__next__()

            while True:
                if abs(a_image.timestamp - b_image.timestamp) < 86400:
                    if a_image.geocode == b_image.geocode:
                        process_pair(a_image, b_image);

                        (_, b_image) = b_iter.__next__()
                    elif a_image.geocode < b_image.geocode:
                        (_, a_image) = a_iter.__next__()
                    else:
                        (_, b_image) = b_iter.__next__()
                elif a_image.timestamp < b_image.timestamp:
                    (_, a_image) = a_iter.__next__()
                else:
                    (_, b_image) = b_iter.__next__()

        except StopIteration:
            pass
