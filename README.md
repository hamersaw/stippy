# stippy
## OVERVIEW
[stip](https://github.com/hamersaw/stip) python API.

## PROTOBUF GENERATION
    pip3 install grpcio grpcio-tools
    python3 -m grpc_tools.protoc -I../stip/impl/protobuf/proto/ --python_out=. --grpc_python_out=. ../stip/impl/protobuf/proto/stip.proto

## TODO
- everything
