import gc
import grpc
import stip_pb2
import stip_pb2_grpc

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

class ImageIterator:
    def __init__(self, request, nodes):
        self.request = request
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
            self.channel = grpc.insecure_channel(node.rpcAddr)
            stub = stip_pb2_grpc.DataManagementStub(self.channel)
            self.it = stub.List(self.request)

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

def list_node_images(host_addr, album, end_timestamp=None, geohash=None,
        max_cloud_coverage=None, min_pixel_coverage=None, platform=None,
        recurse=False, source=None, start_timestamp=None):
    # initialize request
    filter = stip_pb2.Filter(
            endTimestamp=end_timestamp,
            geohash=geohash,
            maxCloudCoverage=max_cloud_coverage,
            minPixelCoverage=min_pixel_coverage,
            platform=platform,
            recurse=recurse,
            source=source,
            startTimestamp=start_timestamp,
        )

    request = stip_pb2.DataListRequest(
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

    # return new ImageIterator
    return ImageIterator(request, [host_node])

def list_images(host_addr, album, end_timestamp=None, geohash=None,
        max_cloud_coverage=None, min_pixel_coverage=None, platform=None,
        recurse=False, source=None, start_timestamp=None):
    # initialize request
    filter = stip_pb2.Filter(
            endTimestamp=end_timestamp,
            geohash=geohash,
            maxCloudCoverage=max_cloud_coverage,
            minPixelCoverage=min_pixel_coverage,
            platform=platform,
            recurse=recurse,
            source=source,
            startTimestamp=start_timestamp,
        )

    request = stip_pb2.DataListRequest(
            album=album,
            filter=filter,
        )

    # return new ImageIterator
    return ImageIterator(request, list_nodes(host_addr))
