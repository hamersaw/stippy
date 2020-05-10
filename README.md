# stippy
## OVERVIEW
STIP (TODO - ref) python API.

## TODO
- everything



pip3 install grpcio grpcio-tools
python3 -m grpc_tools.protoc -I../STIP/impl/protobuf/proto/ --python_out=. --grpc_python_out=. ../STIP/impl/protobuf/proto/stip.proto
