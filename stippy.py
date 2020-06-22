import gc
import grpc
import stip_pb2
import stip_pb2_grpc

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
EXTENT FUNCTIONS
'''
def list_node_extents(host_addr, album, end_timestamp=None, geocode=None,
        max_cloud_coverage=None, min_pixel_coverage=None, platform=None,
        recurse=False, source=None, start_timestamp=None):
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

    # discover node metadata
    host_node = None
    for node in list_nodes(host_addr):
        if host_addr == node.rpcAddr:
            host_node = node

    if host_node == None:
        raise Exception('unable to identify node with rpc address ' + host_addr)

    # return new StipIterator
    iterator_builder = ExtentIteratorBuilder(request)
    return StipIterator(iterator_builder, [host_node])

def list_extents(host_addr, album, end_timestamp=None, geocode=None,
        max_cloud_coverage=None, min_pixel_coverage=None, platform=None,
        recurse=False, source=None, start_timestamp=None):
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
    return StipIterator(iterator_builder, list_nodes(host_addr))

'''
IMAGE FUNCTIONS
'''
def list_node_images(host_addr, album, end_timestamp=None, geocode=None,
        max_cloud_coverage=None, min_pixel_coverage=None, platform=None,
        recurse=False, source=None, start_timestamp=None):
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

    # discover node metadata
    host_node = None
    for node in list_nodes(host_addr):
        if host_addr == node.rpcAddr:
            host_node = node

    if host_node == None:
        raise Exception('unable to identify node with rpc address ' + host_addr)

    # return new ExtentIterator
    iterator_builder = ImageIteratorBuilder(request)
    return StipIterator(iterator_builder, [host_node])

def list_images(host_addr, album, end_timestamp=None, geocode=None,
        max_cloud_coverage=None, min_pixel_coverage=None, platform=None,
        recurse=False, source=None, start_timestamp=None):
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

    # return new ExtentIterator
    iterator_builder = ImageIteratorBuilder(request)
    return StipIterator(iterator_builder, list_nodes(host_addr))

'''
NODE FUNCTIONS
'''
def list_nodes(host_addr):
    # open ClusterManagementStub
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
