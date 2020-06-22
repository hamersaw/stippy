#!/bin/python3
import os
import sys

# import realative 'stippy' python project
script_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(script_dir + '/../')
import stippy

def display(node, extent):
    print(str(node.id) + ' ' + extent.platform + ' ' + extent.geocode
        + ' ' + extent.source + ' ' + str(extent.count))

if __name__ == '__main__':
    host_addr = '127.0.0.1:15606'

    # print Sentinel-2 extents with > 90% pixel coverage
    #   and < 10% cloud coverage
    print('-----NODE EXTENTS 1-----')
    stip_iter = stippy.list_extents(host_addr, 'test', platform='Sentinel-2', 
        min_pixel_coverage=0.9, max_cloud_coverage=0.1)

    for (node, extent) in stip_iter:
        display(node, extent)

    # print extents from only the queried 
    #   node for all geohashes starting with '9q'
    print('-----NODE EXTENTS 2-----')
    stip_iter = stippy.list_node_extents(host_addr,
        'test', recurse=True, geocode='9q')

    for (node, extent) in stip_iter:
        display(node, extent)

    # print all extents from 2018 
    print('-----NODE EXTENTS 3-----')
    stip_iter = stippy.list_extents(host_addr, 'test',
        start_timestamp=1514764800, end_timestamp=1546300800)

    for (node, extent) in stip_iter:
        display(node, extent)
