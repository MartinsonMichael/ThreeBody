import grpc

import main_pb2_grpc
import main_pb2


class ThreeBodyService(main_pb2_grpc.ThreeBodyServiceServicer):

    def __init__(self):
        self.cnt = 0

    def start(self, request, context):
        return main_pb2.SystemState(names=['a', 'b', 'c'])

    def get_state(self, request, context):
        self.cnt += 1
        return main_pb2.SystemState(names=['micael', str(self.cnt)])
