import grpc

# import the generated classes
import main_pb2_grpc
import main_pb2

# open a gRPC channel
channel = grpc.insecure_channel('localhost:50051')

# create a stub (client)
stub = main_pb2_grpc.ThreeBodyServiceStub(channel)

# create a valid request message

for i in range(10):
    print(f'step {i}')
    empty = main_pb2.Empty()
    response = stub.get_state(empty)
    print(response.names)

    empty = main_pb2.Empty()
    response = stub.start(empty)
    print(response.names)
