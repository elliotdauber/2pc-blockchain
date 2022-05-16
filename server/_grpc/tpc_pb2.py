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




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\ttpc.proto\x12\x03tpc\")\n\x0eSQLTransaction\x12\n\n\x02pk\x18\x01 \x01(\t\x12\x0b\n\x03sql\x18\x02 \x01(\t\"R\n\x0bWorkRequest\x12!\n\x04work\x18\x01 \x03(\x0b\x32\x13.tpc.SQLTransaction\x12\x0f\n\x07\x61\x64\x64ress\x18\x02 \x01(\t\x12\x0f\n\x07timeout\x18\x03 \x01(\x05\"?\n\x0cWorkResponse\x12\x0f\n\x07\x61\x64\x64ress\x18\x01 \x01(\t\x12\x0f\n\x07timeout\x18\x02 \x01(\x05\x12\r\n\x05\x65rror\x18\x03 \x01(\t\"G\n\x04Node\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x0b\n\x03url\x18\x02 \x01(\t\x12\r\n\x05\x63olor\x18\x03 \x01(\t\x12\x0b\n\x03log\x18\x04 \x01(\t\x12\n\n\x02\x64\x62\x18\x05 \x01(\t\"N\n\x0bJoinRequest\x12\x17\n\x04node\x18\x01 \x01(\x0b\x32\t.tpc.Node\x12\x0c\n\x04keys\x18\x02 \x03(\t\x12\x10\n\x03idx\x18\x03 \x01(\x05H\x00\x88\x01\x01\x42\x06\n\x04_idx\"\x17\n\x08url_list\x12\x0b\n\x03url\x18\x01 \x03(\t\"\xe3\x01\n\x0cJoinResponse\x12!\n\x04work\x18\x01 \x03(\x0b\x32\x13.tpc.SQLTransaction\x12\x0f\n\x07success\x18\x02 \x01(\x08\x12\x1e\n\x06\x63onfig\x18\x03 \x01(\x0b\x32\t.tpc.NodeH\x00\x88\x01\x01\x12\x33\n\tdirectory\x18\x04 \x03(\x0b\x32 .tpc.JoinResponse.DirectoryEntry\x1a?\n\x0e\x44irectoryEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x1c\n\x05value\x18\x02 \x01(\x0b\x32\r.tpc.url_list:\x02\x38\x01\x42\t\n\x07_config\"0\n\x0bMoveRequest\x12!\n\x04work\x18\x01 \x03(\x0b\x32\x13.tpc.SQLTransaction\" \n\x0cMoveResponse\x12\x10\n\x08\x63omplete\x18\x01 \x01(\x08\x32@\n\x0b\x43oordinator\x12\x31\n\x08SendWork\x12\x10.tpc.WorkRequest\x1a\x11.tpc.WorkResponse\"\x00\x32\xd5\x01\n\x05XNode\x12\x31\n\x08SendWork\x12\x10.tpc.WorkRequest\x1a\x11.tpc.WorkResponse\"\x00\x12\x34\n\x0bReceiveWork\x12\x10.tpc.WorkRequest\x1a\x11.tpc.WorkResponse\"\x00\x12\x30\n\x07\x41\x64\x64Node\x12\x10.tpc.JoinRequest\x1a\x11.tpc.JoinResponse\"\x00\x12\x31\n\x08MoveData\x12\x10.tpc.MoveRequest\x1a\x11.tpc.MoveResponse\"\x00\x42(\n\x14io.grpc.examples.tpcB\x08TPCProtoP\x01\xa2\x02\x03TPCb\x06proto3')



_SQLTRANSACTION = DESCRIPTOR.message_types_by_name['SQLTransaction']
_WORKREQUEST = DESCRIPTOR.message_types_by_name['WorkRequest']
_WORKRESPONSE = DESCRIPTOR.message_types_by_name['WorkResponse']
_NODE = DESCRIPTOR.message_types_by_name['Node']
_JOINREQUEST = DESCRIPTOR.message_types_by_name['JoinRequest']
_URL_LIST = DESCRIPTOR.message_types_by_name['url_list']
_JOINRESPONSE = DESCRIPTOR.message_types_by_name['JoinResponse']
_JOINRESPONSE_DIRECTORYENTRY = _JOINRESPONSE.nested_types_by_name['DirectoryEntry']
_MOVEREQUEST = DESCRIPTOR.message_types_by_name['MoveRequest']
_MOVERESPONSE = DESCRIPTOR.message_types_by_name['MoveResponse']
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

url_list = _reflection.GeneratedProtocolMessageType('url_list', (_message.Message,), {
  'DESCRIPTOR' : _URL_LIST,
  '__module__' : 'tpc_pb2'
  # @@protoc_insertion_point(class_scope:tpc.url_list)
  })
_sym_db.RegisterMessage(url_list)

JoinResponse = _reflection.GeneratedProtocolMessageType('JoinResponse', (_message.Message,), {

  'DirectoryEntry' : _reflection.GeneratedProtocolMessageType('DirectoryEntry', (_message.Message,), {
    'DESCRIPTOR' : _JOINRESPONSE_DIRECTORYENTRY,
    '__module__' : 'tpc_pb2'
    # @@protoc_insertion_point(class_scope:tpc.JoinResponse.DirectoryEntry)
    })
  ,
  'DESCRIPTOR' : _JOINRESPONSE,
  '__module__' : 'tpc_pb2'
  # @@protoc_insertion_point(class_scope:tpc.JoinResponse)
  })
_sym_db.RegisterMessage(JoinResponse)
_sym_db.RegisterMessage(JoinResponse.DirectoryEntry)

MoveRequest = _reflection.GeneratedProtocolMessageType('MoveRequest', (_message.Message,), {
  'DESCRIPTOR' : _MOVEREQUEST,
  '__module__' : 'tpc_pb2'
  # @@protoc_insertion_point(class_scope:tpc.MoveRequest)
  })
_sym_db.RegisterMessage(MoveRequest)

MoveResponse = _reflection.GeneratedProtocolMessageType('MoveResponse', (_message.Message,), {
  'DESCRIPTOR' : _MOVERESPONSE,
  '__module__' : 'tpc_pb2'
  # @@protoc_insertion_point(class_scope:tpc.MoveResponse)
  })
_sym_db.RegisterMessage(MoveResponse)

_COORDINATOR = DESCRIPTOR.services_by_name['Coordinator']
_XNODE = DESCRIPTOR.services_by_name['XNode']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\024io.grpc.examples.tpcB\010TPCProtoP\001\242\002\003TPC'
  _JOINRESPONSE_DIRECTORYENTRY._options = None
  _JOINRESPONSE_DIRECTORYENTRY._serialized_options = b'8\001'
  _SQLTRANSACTION._serialized_start=18
  _SQLTRANSACTION._serialized_end=59
  _WORKREQUEST._serialized_start=61
  _WORKREQUEST._serialized_end=143
  _WORKRESPONSE._serialized_start=145
  _WORKRESPONSE._serialized_end=208
  _NODE._serialized_start=210
  _NODE._serialized_end=281
  _JOINREQUEST._serialized_start=283
  _JOINREQUEST._serialized_end=361
  _URL_LIST._serialized_start=363
  _URL_LIST._serialized_end=386
  _JOINRESPONSE._serialized_start=389
  _JOINRESPONSE._serialized_end=616
  _JOINRESPONSE_DIRECTORYENTRY._serialized_start=542
  _JOINRESPONSE_DIRECTORYENTRY._serialized_end=605
  _MOVEREQUEST._serialized_start=618
  _MOVEREQUEST._serialized_end=666
  _MOVERESPONSE._serialized_start=668
  _MOVERESPONSE._serialized_end=700
  _COORDINATOR._serialized_start=702
  _COORDINATOR._serialized_end=766
  _XNODE._serialized_start=769
  _XNODE._serialized_end=982
# @@protoc_insertion_point(module_scope)
