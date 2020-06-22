#!/bin/python3
import stippy

if __name__ == '__main__':
    host_addr = '127.0.0.1:15606'

    # print nodes
    print('-----NODES-----')
    nodes = stippy.list_nodes(host_addr)
    for node in nodes:
        print(str(node.id) + ' ' + node.rpcAddr + ' ' + node.xferAddr)

    # print albums
    print('-----ALBUMS-----')
    albums = stippy.list_albums(host_addr)
    for album in albums:
        print(album.id + ' ' + str(album.geocode) + ' ' + str(album.status))

    # close test album
    stippy.close_album(host_addr, 'test')

    # open test album
    stippy.open_album(host_addr, 'test')

    # print cluster extents starting with geohash '9q6'
    print('-----EXTENTS-----')
    extent_iter = stippy.list_extents(host_addr,
        'test', geocode='9q6', recurse=True)

    for (node, extent) in extent_iter:
        print(str(node.id) + ' ' + extent.platform + ' ' + extent.geocode
            + ' ' + extent.source + ' ' + str(extent.count))

    # print images from only the queried 
    #   node for all geohashes starting with '9xh'
    print('-----NODE IMAGES-----')
    image_iter = stippy.list_node_images(host_addr,
        'test', recurse=True, geocode='9q')

    for (node, image) in image_iter:
        print(str(node.id) + ' ' + image.platform + ' ' + image.geocode
            + ' ' + image.source + ' ' + str(image.timestamp))

        for file in image.files:
            print('    ' + str(file.subdataset))
