import numpy
import gdal
import socket
import struct

import gc
import grpc
import stip_pb2
import stip_pb2_grpc

GEOHASH=stip_pb2.GEOHASH
QUADTILE=stip_pb2.QUADTILE

class IteratorBuilder:
    def __init__(self, request):
        self.request = request

    def build(self, node):
        raise NotImplementedError("subclass must implement abstract method")

class ExtentIteratorBuilder(IteratorBuilder):
    def build(self, node):
        channel = grpc.insecure_channel(node.rpcAddr)
        stub = stip_pb2_grpc.ImageManagementStub(channel)
        it = stub.Search(self.request)

        return channel, stub, it

class ImageIteratorBuilder(IteratorBuilder):
    def build(self, node):
        channel = grpc.insecure_channel(node.rpcAddr)
        stub = stip_pb2_grpc.ImageManagementStub(channel)
        it = stub.List(self.request)

        return channel, stub, it

class StipIterator:
    def __init__(self, iterator_builder, nodes):
        self.iterator_builder = iterator_builder
        self.nodes = nodes
        self.node_index = 0
        self.next_item = None
        self.channel = None

    def __iter__(self):
        return self

    def __next__(self):
        # check if next items exists
        while self.next_item == None:
            # if open channel -> close
            if self.channel != None:
                self.channel.close()

            # if no more nodes -> return None
            if self.node_index == len(self.nodes):
                raise StopIteration

            # open iterator stream to next addr
            node = self.nodes[self.node_index]
            self.channel, stub, self.it = \
                self.iterator_builder.build(node)

            # read next item
            try:
                self.next_item = self.it.__next__()
            except StopIteration:
                self.next_item = None

            # increment self.addr_index
            self.node_index += 1

        # update self.next_item
        item = self.next_item
        try:
            self.next_item = self.it.__next__()
        except StopIteration:
            self.next_item = None

        return (self.nodes[self.node_index-1], item)

'''
ALBUM FUNCTIONS
'''
def close_album(host_addr, album):
    # open AlbumManagementStub
    channel = grpc.insecure_channel(host_addr)
    stub = stip_pb2_grpc.AlbumManagementStub(channel)

    # initialize request
    close_request = stip_pb2.AlbumCloseRequest(id=album)
    request = stip_pb2.AlbumBroadcastRequest(
        messageType=stip_pb2.ALBUM_CLOSE, closeRequest=close_request)

    # submit request
    response = stub.Broadcast(request)

    # close channel
    channel.close()

    # return replies
    return response.closeReplies

def list_albums(host_addr):
    # open AlbumManagementStub
    channel = grpc.insecure_channel(host_addr)
    stub = stip_pb2_grpc.AlbumManagementStub(channel)

    # initialize request
    request = stip_pb2.AlbumListRequest()

    # submit request
    response = stub.List(request)

    # close channel
    channel.close()

    # return albums
    return response.albums

def open_album(host_addr, album, thread_count=4):
    # open AlbumManagementStub
    channel = grpc.insecure_channel(host_addr)
    stub = stip_pb2_grpc.AlbumManagementStub(channel)

    # initialize request
    open_request = stip_pb2.AlbumOpenRequest(id=album,
        threadCount=thread_count)
    request = stip_pb2.AlbumBroadcastRequest(
        messageType=stip_pb2.ALBUM_OPEN, openRequest=open_request)

    # submit request
    response = stub.Broadcast(request)

    # close channel
    channel.close()

    # return replies
    return response.openReplies

'''
EXTENT FUNCTIONS
'''
def list_node_extents(host_addr, album, end_timestamp=None, geocode=None,
        max_cloud_coverage=None, min_pixel_coverage=None, platform=None,
        recurse=False, source=None, start_timestamp=None):
    # discover node metadata
    host_node = None
    for node in list_nodes(host_addr):
        if host_addr == node.rpcAddr:
            host_node = node

    if host_node == None:
        raise Exception('unable to identify node with rpc address ' + host_addr)

    # return StipIterator
    return _list_extents([host_node], album, end_timestamp,
        geocode, max_cloud_coverage, min_pixel_coverage, platform,
        recurse, source, start_timestamp)

def list_extents(host_addr, album, end_timestamp=None, geocode=None,
        max_cloud_coverage=None, min_pixel_coverage=None, platform=None,
        recurse=False, source=None, start_timestamp=None):
    # return StipIterator
    return _list_extents(list_nodes(host_addr), album, end_timestamp,
        geocode, max_cloud_coverage, min_pixel_coverage, platform,
        recurse, source, start_timestamp)

def _list_extents(nodes, album, end_timestamp, geocode,
        max_cloud_coverage, min_pixel_coverage, platform,
        recurse, source, start_timestamp):
    # initialize request
    filter = stip_pb2.Filter(
            endTimestamp=end_timestamp,
            geocode=geocode,
            maxCloudCoverage=max_cloud_coverage,
            minPixelCoverage=min_pixel_coverage,
            platform=platform,
            recurse=recurse,
            source=source,
            startTimestamp=start_timestamp,
        )

    request = stip_pb2.ImageSearchRequest(
            album=album,
            filter=filter,
        )

    # return new StipIterator
    iterator_builder = ExtentIteratorBuilder(request)
    return StipIterator(iterator_builder, nodes)

'''
IMAGE FUNCTIONS
'''
def list_node_images(host_addr, album, end_timestamp=None, geocode=None,
        max_cloud_coverage=None, min_pixel_coverage=None, platform=None,
        recurse=False, source=None, start_timestamp=None):
    # discover node metadata
    host_node = None
    for node in list_nodes(host_addr):
        if host_addr == node.rpcAddr:
            host_node = node

    if host_node == None:
        raise Exception('unable to identify node with rpc address ' + host_addr)

    # return StipIterator
    return _list_images([host_node], album, end_timestamp,
        geocode, max_cloud_coverage, min_pixel_coverage, platform,
        recurse, source, start_timestamp)

def list_images(host_addr, album, end_timestamp=None, geocode=None,
        max_cloud_coverage=None, min_pixel_coverage=None, platform=None,
        recurse=False, source=None, start_timestamp=None):
    # return StipIterator
    return _list_images(list_nodes(host_addr), album, end_timestamp,
        geocode, max_cloud_coverage, min_pixel_coverage, platform,
        recurse, source, start_timestamp)

def _list_images(nodes, album, end_timestamp, geocode,
        max_cloud_coverage, min_pixel_coverage, platform,
        recurse, source, start_timestamp):
    # initialize request
    filter = stip_pb2.Filter(
            endTimestamp=end_timestamp,
            geocode=geocode,
            maxCloudCoverage=max_cloud_coverage,
            minPixelCoverage=min_pixel_coverage,
            platform=platform,
            recurse=recurse,
            source=source,
            startTimestamp=start_timestamp,
        )

    request = stip_pb2.ImageListRequest(
            album=album,
            filter=filter,
        )

    # return new StipIterator
    iterator_builder = ImageIteratorBuilder(request)
    return StipIterator(iterator_builder, nodes)

'''
NODE FUNCTIONS
'''
def list_nodes(host_addr):
    # open NodeManagementStub
    channel = grpc.insecure_channel(host_addr)
    stub = stip_pb2_grpc.NodeManagementStub(channel)

    # initialize request
    request = stip_pb2.NodeListRequest()

    # submit request
    response = stub.List(request)

    # close channel
    channel.close()

    # return nodes
    return response.nodes

'''
READ FUNCTIONS
'''
def read_file(host_addr, path, subgeocode=None):
    # parse address fields
    fields = host_addr.split(':')

    # open socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((fields[0], int(fields[1])))

        # write read op
        sock.sendall(struct.pack('B', 0))

        # write path
        path_bytes = path.encode('utf-8')
        sock.sendall(struct.pack('B', len(path_bytes)))
        sock.sendall(path_bytes)

        # write split geocode
        if subgeocode == None:
            sock.sendall(struct.pack('B', 0))
        else:
            sock.sendall(struct.pack('B', 1))
            sock.sendall(struct.pack('B', subgeocode[0]))
            subgeocode_bytes = subgeocode[1].encode('utf-8')
            sock.sendall(struct.pack('B', len(subgeocode_bytes)))
            sock.sendall(subgeocode_bytes)

        # recv process result
        process_result = sock.recv(1, socket.MSG_WAITALL)
        if process_result[0]:
            # if error -> read message and raise
            error_len_buf = sock.recv(1, socket.MSG_WAITALL)
            error_len = struct.unpack('>B', error_len_buf)[0]
            error_buf = sock.recv(error_len)
            error = error_buf.decode('utf-8')

            raise ValueError(error);

        # read image dimensions
        width_buf = sock.recv(4, socket.MSG_WAITALL)
        width = struct.unpack('>I', width_buf)[0]

        height_buf = sock.recv(4, socket.MSG_WAITALL)
        height = struct.unpack('>I', height_buf)[0]

        # read image transform
        transform = []
        for i in range(0, 6):
            value_buf = sock.recv(8, socket.MSG_WAITALL)
            value = struct.unpack('>d', value_buf)[0]

            transform.append(value)

        # read image projection
        projection_len_buf = sock.recv(4, socket.MSG_WAITALL)
        projection_len = struct.unpack('>I', projection_len_buf)[0]
        projection_buf = sock.recv(projection_len)
        projection = projection_buf.decode('utf-8')

        # read gdal type
        gdal_type_buf = sock.recv(4, socket.MSG_WAITALL)
        gdal_type = struct.unpack('>I', gdal_type_buf)[0]

        # read no data value
        no_data_value_ind_buf = sock.recv(1, socket.MSG_WAITALL)
        no_data_value_ind = \
            struct.unpack('>B', no_data_value_ind_buf)[0]
        if no_data_value_ind != 0:
            no_data_value_buf = sock.recv(8, socket.MSG_WAITALL)
            no_data_value = struct.unpack('>d', no_data_value_buf)[0]
        else:
            no_data_value = None

        # read rasterband count
        rasterband_count_buf = sock.recv(1, socket.MSG_WAITALL)
        rasterband_count = struct.unpack('>B', rasterband_count_buf)[0]

        # create image
        driver = gdal.GetDriverByName('Mem')
        dataset = driver.Create('unreachable', xsize=width,
            ysize=height, bands=rasterband_count, eType=gdal_type)

        dataset.SetGeoTransform(transform)
        dataset.SetProjection(projection)

        # read image rasters
        pixel_count = width * height
        for i in range(0, rasterband_count):
            # read gdal type
            gdal_type_buf = sock.recv(4, socket.MSG_WAITALL)
            gdal_type = struct.unpack('>I', gdal_type_buf)[0]

            buf_size = pixel_count
            if gdal_type == 2 or gdal_type == 3:
                buf_size *= 2

            data_buf = sock.recv(buf_size, socket.MSG_WAITALL)
            
            data = []
            for j in range(0, pixel_count):
                if gdal_type == 1:
                    value = data_buf[j]
                elif gdal_type == 2:
                    value = struct.unpack('>h',
                        data_buf[j * 2:j * 2 + 2])[0]
                elif gdal_type == 3:
                    value = struct.unpack('>H',
                        data_buf[j * 2:j * 2 + 2])[0]

                data.append(value)

            dataset.GetRasterBand(i+1) \
                .WriteRaster(0, 0, width, height, data_buf)

        sock.close()

    return dataset
