#!/bin/python3
import stippy

if __name__ == '__main__':
    host_addr = '127.0.0.1:15606'

    # print nodes
    #nodes = stippy.list_nodes(host_addr)
    #for node in nodes:
    #    print(str(node.id) + ' ' + node.rpcAddr + ' ' + node.xferAddr)

    # print images
    #image_iter = stippy.list_images(host_addr, band='TCI')
    #for (node, image) in image_iter:
    #    print(str(node.id) + ' ' + image.path + ' ' + image.geohash
    #        + ' ' + image.platform + ' ' + image.band + ' ' 
    #        + image.source + ' ' + str(image.timestamp))

    # print node images
    #image_iter = stippy.list_images(host_addr, geohash='9xnp0')
    #for (node, image) in image_iter:
    #    print(str(node.id) + ' ' + image.path + ' ' + image.geohash
    #        + ' ' + image.platform + ' ' + image.band + ' ' 
    #        + image.source + ' ' + str(image.timestamp))
