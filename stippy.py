import grpc
import stip_pb2
import stip_pb2_grpc

def list_nodes(host_addr):
    # open ClusterManagementStub
    channel = grpc.insecure_channel(host_addr)
    stub = stip_pb2_grpc.ClusterManagementStub(channel)

    # initialize request
    request = stip_pb2.NodeListRequest()

    # submit request
    response = stub.NodeList(request)

    # return nodes
    return response.nodes

def list_images(host_addr, band=None, geohash=None,
        max_cloud_coverage=None, min_pixel_coverage=None,
        platform=None, source=None):
    # open DataManagementStub
    channel = grpc.insecure_channel(host_addr)
    stub = stip_pb2_grpc.DataManagementStub(channel)

    # initialize request
    list_request = stip_pb2.DataListRequest(
            band=band,
            geohash=geohash,
            maxCloudCoverage=max_cloud_coverage,
            minPixelCoverage=min_pixel_coverage,
            platform=platform,
            source=source,
        )

    request = stip_pb2.DataBroadcastRequest(
            messageType=stip_pb2.LIST,
            listRequest=list_request,
        )

    # submit request
    response = stub.Broadcast(request)

    # return images
    images={}
    for node_id in response.listReplies:
        images[node_id] = response.listReplies[node_id].images

    return images

def list_node_images(host_addr, band=None, geohash=None,
        max_cloud_coverage=None, min_pixel_coverage=None,
        platform=None, source=None):
    # open DataManagementStub
    channel = grpc.insecure_channel(host_addr)
    stub = stip_pb2_grpc.DataManagementStub(channel)

    # initialize request
    request = stip_pb2.DataListRequest(
            band=band,
            geohash=geohash,
            maxCloudCoverage=max_cloud_coverage,
            minPixelCoverage=min_pixel_coverage,
            platform=platform,
            source=source,
        )

    # submit request
    response = stub.List(request)

    # return images
    return response.images
