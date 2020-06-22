#!/bin/python3
import os
import sys

# import realative 'stippy' python project
script_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(script_dir + '/../')
import stippy

if __name__ == '__main__':
    host_addr = '127.0.0.1:15606'

    # print nodes
    print('-----NODES-----')
    nodes = stippy.list_nodes(host_addr)
    for node in nodes:
        print(str(node.id) + ' ' + node.rpcAddr + ' ' + node.xferAddr)
