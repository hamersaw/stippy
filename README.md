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
The test.py file at the root of the projects contains a few examples outlining base functionality. Listing images within stip is facilitated by initializing instances of the ImageIterator class. This definition iterates over cluster nodes, leveraging the gRPC protobuf streaming API to return tuples of (node, image) where node and image are the Protobuf messages defined as

    message Node {
        required uint32 id = 1;
        required string rpcAddr = 2;
        required string xferAddr = 3;
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
        required string description = 1;
        required string path = 2;
        required double pixelCoverage = 3;
    }

## TODO
- include full protobuf RPC functinality: album list, image search, etc
