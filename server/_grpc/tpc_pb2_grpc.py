# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import _grpc.tpc_pb2 as tpc__pb2


class XNodeStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.SendWork = channel.unary_unary(
                '/tpc.XNode/SendWork',
                request_serializer=tpc__pb2.WorkRequest.SerializeToString,
                response_deserializer=tpc__pb2.WorkResponse.FromString,
                )
        self.ReceiveWork = channel.unary_unary(
                '/tpc.XNode/ReceiveWork',
                request_serializer=tpc__pb2.WorkRequest.SerializeToString,
                response_deserializer=tpc__pb2.WorkResponse.FromString,
                )
        self.AddNode = channel.unary_unary(
                '/tpc.XNode/AddNode',
                request_serializer=tpc__pb2.JoinRequest.SerializeToString,
                response_deserializer=tpc__pb2.JoinResponse.FromString,
                )
        self.MoveData = channel.unary_unary(
                '/tpc.XNode/MoveData',
                request_serializer=tpc__pb2.MoveRequest.SerializeToString,
                response_deserializer=tpc__pb2.MoveResponse.FromString,
                )
        self.Kill = channel.unary_unary(
                '/tpc.XNode/Kill',
                request_serializer=tpc__pb2.Empty.SerializeToString,
                response_deserializer=tpc__pb2.Empty.FromString,
                )


class XNodeServicer(object):
    """Missing associated documentation comment in .proto file."""

    def SendWork(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ReceiveWork(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def AddNode(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def MoveData(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Kill(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_XNodeServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'SendWork': grpc.unary_unary_rpc_method_handler(
                    servicer.SendWork,
                    request_deserializer=tpc__pb2.WorkRequest.FromString,
                    response_serializer=tpc__pb2.WorkResponse.SerializeToString,
            ),
            'ReceiveWork': grpc.unary_unary_rpc_method_handler(
                    servicer.ReceiveWork,
                    request_deserializer=tpc__pb2.WorkRequest.FromString,
                    response_serializer=tpc__pb2.WorkResponse.SerializeToString,
            ),
            'AddNode': grpc.unary_unary_rpc_method_handler(
                    servicer.AddNode,
                    request_deserializer=tpc__pb2.JoinRequest.FromString,
                    response_serializer=tpc__pb2.JoinResponse.SerializeToString,
            ),
            'MoveData': grpc.unary_unary_rpc_method_handler(
                    servicer.MoveData,
                    request_deserializer=tpc__pb2.MoveRequest.FromString,
                    response_serializer=tpc__pb2.MoveResponse.SerializeToString,
            ),
            'Kill': grpc.unary_unary_rpc_method_handler(
                    servicer.Kill,
                    request_deserializer=tpc__pb2.Empty.FromString,
                    response_serializer=tpc__pb2.Empty.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'tpc.XNode', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class XNode(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def SendWork(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/tpc.XNode/SendWork',
            tpc__pb2.WorkRequest.SerializeToString,
            tpc__pb2.WorkResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ReceiveWork(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/tpc.XNode/ReceiveWork',
            tpc__pb2.WorkRequest.SerializeToString,
            tpc__pb2.WorkResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def AddNode(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/tpc.XNode/AddNode',
            tpc__pb2.JoinRequest.SerializeToString,
            tpc__pb2.JoinResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def MoveData(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/tpc.XNode/MoveData',
            tpc__pb2.MoveRequest.SerializeToString,
            tpc__pb2.MoveResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Kill(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/tpc.XNode/Kill',
            tpc__pb2.Empty.SerializeToString,
            tpc__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)


class ClientStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ReceiveOutcome = channel.unary_unary(
                '/tpc.Client/ReceiveOutcome',
                request_serializer=tpc__pb2.WorkOutcome.SerializeToString,
                response_deserializer=tpc__pb2.Empty.FromString,
                )


class ClientServicer(object):
    """Missing associated documentation comment in .proto file."""

    def ReceiveOutcome(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ClientServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'ReceiveOutcome': grpc.unary_unary_rpc_method_handler(
                    servicer.ReceiveOutcome,
                    request_deserializer=tpc__pb2.WorkOutcome.FromString,
                    response_serializer=tpc__pb2.Empty.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'tpc.Client', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Client(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def ReceiveOutcome(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/tpc.Client/ReceiveOutcome',
            tpc__pb2.WorkOutcome.SerializeToString,
            tpc__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
