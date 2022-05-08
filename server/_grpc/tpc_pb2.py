# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tpc.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\ttpc.proto\x12\x03tpc\"I\n\x0bTransaction\x12\x0e\n\x06\x61\x63\x63\x65ss\x18\x01 \x01(\t\x12\n\n\x02pk\x18\x02 \x01(\t\x12\x0e\n\x06\x63olumn\x18\x03 \x01(\t\x12\x0e\n\x06\x61\x63tion\x18\x04 \x01(\t\">\n\x0bWorkRequest\x12\x1e\n\x04work\x18\x01 \x03(\x0b\x32\x10.tpc.Transaction\x12\x0f\n\x07\x61\x64\x64ress\x18\x02 \x01(\t\"?\n\x0cWorkResponse\x12\x0f\n\x07\x61\x64\x64ress\x18\x01 \x01(\t\x12\x0f\n\x07timeout\x18\x02 \x01(\x05\x12\r\n\x05\x65rror\x18\x03 \x01(\t2@\n\x0b\x43oordinator\x12\x31\n\x08SendWork\x12\x10.tpc.WorkRequest\x1a\x11.tpc.WorkResponse\"\x00\x32<\n\x04Node\x12\x34\n\x0bReceiveWork\x12\x10.tpc.WorkRequest\x1a\x11.tpc.WorkResponse\"\x00\x32p\n\x05XNode\x12\x31\n\x08SendWork\x12\x10.tpc.WorkRequest\x1a\x11.tpc.WorkResponse\"\x00\x12\x34\n\x0bReceiveWork\x12\x10.tpc.WorkRequest\x1a\x11.tpc.WorkResponse\"\x00\x42(\n\x14io.grpc.examples.tpcB\x08TPCProtoP\x01\xa2\x02\x03TPCb\x06proto3')



_TRANSACTION = DESCRIPTOR.message_types_by_name['Transaction']
_WORKREQUEST = DESCRIPTOR.message_types_by_name['WorkRequest']
_WORKRESPONSE = DESCRIPTOR.message_types_by_name['WorkResponse']
Transaction = _reflection.GeneratedProtocolMessageType('Transaction', (_message.Message,), {
  'DESCRIPTOR' : _TRANSACTION,
  '__module__' : 'tpc_pb2'
  # @@protoc_insertion_point(class_scope:tpc.Transaction)
  })
_sym_db.RegisterMessage(Transaction)

WorkRequest = _reflection.GeneratedProtocolMessageType('WorkRequest', (_message.Message,), {
  'DESCRIPTOR' : _WORKREQUEST,
  '__module__' : 'tpc_pb2'
  # @@protoc_insertion_point(class_scope:tpc.WorkRequest)
  })
_sym_db.RegisterMessage(WorkRequest)

WorkResponse = _reflection.GeneratedProtocolMessageType('WorkResponse', (_message.Message,), {
  'DESCRIPTOR' : _WORKRESPONSE,
  '__module__' : 'tpc_pb2'
  # @@protoc_insertion_point(class_scope:tpc.WorkResponse)
  })
_sym_db.RegisterMessage(WorkResponse)

_COORDINATOR = DESCRIPTOR.services_by_name['Coordinator']
_NODE = DESCRIPTOR.services_by_name['Node']
_XNODE = DESCRIPTOR.services_by_name['XNode']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\024io.grpc.examples.tpcB\010TPCProtoP\001\242\002\003TPC'
  _TRANSACTION._serialized_start=18
  _TRANSACTION._serialized_end=91
  _WORKREQUEST._serialized_start=93
  _WORKREQUEST._serialized_end=155
  _WORKRESPONSE._serialized_start=157
  _WORKRESPONSE._serialized_end=220
  _COORDINATOR._serialized_start=222
  _COORDINATOR._serialized_end=286
  _NODE._serialized_start=288
  _NODE._serialized_end=348
  _XNODE._serialized_start=350
  _XNODE._serialized_end=462
# @@protoc_insertion_point(module_scope)
