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




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\ttpc.proto\x12\x03tpc\")\n\x0eSQLTransaction\x12\n\n\x02pk\x18\x01 \x01(\t\x12\x0b\n\x03sql\x18\x02 \x01(\t\"e\n\x0bWorkRequest\x12!\n\x04work\x18\x01 \x03(\x0b\x32\x13.tpc.SQLTransaction\x12\x0f\n\x07\x61\x64\x64ress\x18\x02 \x01(\t\x12\x0f\n\x07timeout\x18\x03 \x01(\x05\x12\x11\n\tclienturl\x18\x04 \x01(\t\"R\n\x0cWorkResponse\x12\x0f\n\x07\x61\x64\x64ress\x18\x01 \x01(\t\x12\x0f\n\x07timeout\x18\x02 \x01(\x05\x12\r\n\x05\x65rror\x18\x03 \x01(\t\x12\x11\n\tthreshold\x18\x04 \x01(\x05\"y\n\x04Node\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x0b\n\x03url\x18\x02 \x01(\t\x12\x19\n\x0cpk_range_low\x18\x03 \x01(\tH\x00\x88\x01\x01\x12\x1a\n\rpk_range_high\x18\x04 \x01(\tH\x01\x88\x01\x01\x42\x0f\n\r_pk_range_lowB\x10\n\x0e_pk_range_high\"\'\n\x0bJoinRequest\x12\x18\n\x05nodes\x18\x01 \x03(\x0b\x32\t.tpc.Node\"\'\n\x0cLeaveRequest\x12\x17\n\x04node\x18\x01 \x01(\x0b\x32\t.tpc.Node\" \n\rLeaveResponse\x12\x0f\n\x07removed\x18\x01 \x01(\x08\"=\n\x0bWorkOutcome\x12\x0f\n\x07\x61\x64\x64ress\x18\x01 \x01(\t\x12\x0f\n\x07outcome\x18\x02 \x01(\t\x12\x0c\n\x04\x64\x61ta\x18\x03 \x01(\t\"\x07\n\x05\x45mpty2\xd6\x01\n\x05XNode\x12\x31\n\x08SendWork\x12\x10.tpc.WorkRequest\x1a\x11.tpc.WorkResponse\"\x00\x12\x34\n\x0bReceiveWork\x12\x10.tpc.WorkRequest\x1a\x11.tpc.WorkResponse\"\x00\x12/\n\x07JoinSys\x12\x10.tpc.JoinRequest\x1a\x10.tpc.JoinRequest\"\x00\x12\x33\n\x08LeaveSys\x12\x11.tpc.LeaveRequest\x1a\x12.tpc.LeaveResponse\"\x00\x32:\n\x06\x43lient\x12\x30\n\x0eReceiveOutcome\x12\x10.tpc.WorkOutcome\x1a\n.tpc.Empty\"\x00\x42(\n\x14io.grpc.examples.tpcB\x08TPCProtoP\x01\xa2\x02\x03TPCb\x06proto3')



_SQLTRANSACTION = DESCRIPTOR.message_types_by_name['SQLTransaction']
_WORKREQUEST = DESCRIPTOR.message_types_by_name['WorkRequest']
_WORKRESPONSE = DESCRIPTOR.message_types_by_name['WorkResponse']
_NODE = DESCRIPTOR.message_types_by_name['Node']
_JOINREQUEST = DESCRIPTOR.message_types_by_name['JoinRequest']
_LEAVEREQUEST = DESCRIPTOR.message_types_by_name['LeaveRequest']
_LEAVERESPONSE = DESCRIPTOR.message_types_by_name['LeaveResponse']
_WORKOUTCOME = DESCRIPTOR.message_types_by_name['WorkOutcome']
_EMPTY = DESCRIPTOR.message_types_by_name['Empty']
SQLTransaction = _reflection.GeneratedProtocolMessageType('SQLTransaction', (_message.Message,), {
  'DESCRIPTOR' : _SQLTRANSACTION,
  '__module__' : 'tpc_pb2'
  # @@protoc_insertion_point(class_scope:tpc.SQLTransaction)
  })
_sym_db.RegisterMessage(SQLTransaction)

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

Node = _reflection.GeneratedProtocolMessageType('Node', (_message.Message,), {
  'DESCRIPTOR' : _NODE,
  '__module__' : 'tpc_pb2'
  # @@protoc_insertion_point(class_scope:tpc.Node)
  })
_sym_db.RegisterMessage(Node)

JoinRequest = _reflection.GeneratedProtocolMessageType('JoinRequest', (_message.Message,), {
  'DESCRIPTOR' : _JOINREQUEST,
  '__module__' : 'tpc_pb2'
  # @@protoc_insertion_point(class_scope:tpc.JoinRequest)
  })
_sym_db.RegisterMessage(JoinRequest)

LeaveRequest = _reflection.GeneratedProtocolMessageType('LeaveRequest', (_message.Message,), {
  'DESCRIPTOR' : _LEAVEREQUEST,
  '__module__' : 'tpc_pb2'
  # @@protoc_insertion_point(class_scope:tpc.LeaveRequest)
  })
_sym_db.RegisterMessage(LeaveRequest)

LeaveResponse = _reflection.GeneratedProtocolMessageType('LeaveResponse', (_message.Message,), {
  'DESCRIPTOR' : _LEAVERESPONSE,
  '__module__' : 'tpc_pb2'
  # @@protoc_insertion_point(class_scope:tpc.LeaveResponse)
  })
_sym_db.RegisterMessage(LeaveResponse)

WorkOutcome = _reflection.GeneratedProtocolMessageType('WorkOutcome', (_message.Message,), {
  'DESCRIPTOR' : _WORKOUTCOME,
  '__module__' : 'tpc_pb2'
  # @@protoc_insertion_point(class_scope:tpc.WorkOutcome)
  })
_sym_db.RegisterMessage(WorkOutcome)

Empty = _reflection.GeneratedProtocolMessageType('Empty', (_message.Message,), {
  'DESCRIPTOR' : _EMPTY,
  '__module__' : 'tpc_pb2'
  # @@protoc_insertion_point(class_scope:tpc.Empty)
  })
_sym_db.RegisterMessage(Empty)

_XNODE = DESCRIPTOR.services_by_name['XNode']
_CLIENT = DESCRIPTOR.services_by_name['Client']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\024io.grpc.examples.tpcB\010TPCProtoP\001\242\002\003TPC'
  _SQLTRANSACTION._serialized_start=18
  _SQLTRANSACTION._serialized_end=59
  _WORKREQUEST._serialized_start=61
  _WORKREQUEST._serialized_end=162
  _WORKRESPONSE._serialized_start=164
  _WORKRESPONSE._serialized_end=246
  _NODE._serialized_start=248
  _NODE._serialized_end=369
  _JOINREQUEST._serialized_start=371
  _JOINREQUEST._serialized_end=410
  _LEAVEREQUEST._serialized_start=412
  _LEAVEREQUEST._serialized_end=451
  _LEAVERESPONSE._serialized_start=453
  _LEAVERESPONSE._serialized_end=485
  _WORKOUTCOME._serialized_start=487
  _WORKOUTCOME._serialized_end=548
  _EMPTY._serialized_start=550
  _EMPTY._serialized_end=557
  _XNODE._serialized_start=560
  _XNODE._serialized_end=774
  _CLIENT._serialized_start=776
  _CLIENT._serialized_end=834
# @@protoc_insertion_point(module_scope)
