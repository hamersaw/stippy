#!/bin/python3
import os
import sys

# import realative 'stippy' python project
script_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(script_dir + '/../')
import stippy

if __name__ == '__main__':
    host_addr = '127.0.0.1:15606'

    # print albums
    print('-----ALBUMS-----')
    albums = stippy.list_albums(host_addr)
    for album in albums:
        print(album.id + ' ' + str(album.geocode) + ' ' + str(album.status))

    # close test album
    print('closing album \'test\'')
    stippy.close_album(host_addr, 'test')

    # open test album
    print('opening album \'test\'')
    stippy.open_album(host_addr, 'test')
