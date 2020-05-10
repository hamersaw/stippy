#!/bin/python3
import stippy

if __name__ == '__main__':
    host_addr = '127.0.0.1:15606'

    # print images
    #images = stippy.list_images(host_addr, band='TCI')
    #for node_id in images:
    #    for image in images[node_id]:
    #        print(image.path + ' ' + image.geohash + ' '
    #            + image.platform + ' ' + image.band + ' ' + image.source)

    # print node images
    #images = stippy.list_node_images(host_addr, geohash='9xnp0')
    #for image in images:
    #    print(image.path + ' ' + image.geohash + ' ' + image.platform
    #        + ' ' + image.band + ' ' + image.source)
