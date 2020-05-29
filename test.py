#!/bin/python3
import stippy

if __name__ == '__main__':
    host_addr = '127.0.0.1:15606'

    # print nodes
    print('-----NODES-----')
    nodes = stippy.list_nodes(host_addr)
    for node in nodes:
        print(str(node.id) + ' ' + node.rpcAddr + ' ' + node.xferAddr)

    # print images for geohash '9xj6t'
    print('-----IMAGES-----')
    image_iter = stippy.list_images(host_addr, geohash='9xj6t')
    for (node, image) in image_iter:
        print(str(node.id) + ' ' + image.platform + ' ' + image.geohash
            + ' ' + image.source + ' ' + str(image.timestamp))

        for file in image.files:
            print('    ' + file.path)

    # print images from only the queried 
    # node for all geohashes starting with '9xh'
    print('-----NODE IMAGES-----')
    image_iter = stippy.list_node_images(host_addr, recurse=True, geohash='9xh')
    for (node, image) in image_iter:
        print(str(node.id) + ' ' + image.platform + ' ' + image.geohash
            + ' ' + image.source + ' ' + str(image.timestamp))

        for file in image.files:
            print('    ' + file.description)
