# stippy
## OVERVIEW
[stip](https://github.com/hamersaw/stip) python API.

## USAGE
#### PROTOBUF GENERATION
This project uses [gRPC](https://grpc.io/) and [Protocol Buffers](https://developers.google.com/protocol-buffers/) to present a language agnostic RPC interface. The stip_pb2.py and stip_pb2_grpc.py files at the root of this project are pre-compiled protobuf definition files for the latest release. Therefore, each user does not need to compile them separately. Below are the necessary commands to compile python protobuf files.

    # install grpcio-tools library
    pip3 install grpcio-tools

    # compile python protobuf definitions from stip source files
    python3 -m grpc_tools.protoc -I../stip/impl/protobuf/proto/ --python_out=. --grpc_python_out=. ../stip/impl/protobuf/proto/stip.proto
#### INSTALLATION
The only python dependency required for this library is grpcio, a python gRPC implementation. It may be installed using pip with the command

    # install the grpcio library
    pip3 install grpcio

To use this library from another project, the path must be importing by the executing python code.
#### EXAMPLES
The 'examples' folder in the root directory contains a variety of library usafe illustrations. Most functionality is driven by performing stip requests (using both synchronous as streaming API's) and iteratring over results. Thankfully, this process is abstracted through API functions. Resulting objects are defined by Protobufs as follows

    message Album {
        required int32 dhtKeyLength = 1;
        required Geocode geocode = 2;
        required string id = 3;
        required AlbumStatus status = 4;
    }

    enum AlbumStatus {
        CLOSED = 0;
        OPEN = 1;
    }

    message Extent {
        required uint32 count = 1;
        required string geocode = 2;
        required string platform = 3;
        required uint32 precision = 4;
        required string source = 5;
    }

    message Image {
        optional double cloudCoverage = 1;
        required string geocode = 2;
        repeated File files = 3;
        required string platform = 4;
        required string source = 5;
        required int64 timestamp = 6;
    }

    message File {
        required string path = 1;
        required double pixelCoverage = 2;
        required int32 subdataset = 3;
    }

    message Node {
        required uint32 id = 1;
        required string rpcAddr = 2;
        required string xferAddr = 3;
    }

## TODO
- temporarily fully functional
