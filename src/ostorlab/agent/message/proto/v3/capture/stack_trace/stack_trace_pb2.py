# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ostorlab/agent/message/proto/v3/capture/stack_trace/stack_trace.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\nEostorlab/agent/message/proto/v3/capture/stack_trace/stack_trace.proto\x12\x33ostorlab.agent.message.proto.v3.capture.stack_trace\"0\n\x03\x41rg\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x0c\x12\x0c\n\x04type\x18\x03 \x01(\t\"\xc9\x01\n\x05\x46rame\x12\x11\n\tfile_path\x18\x01 \x01(\t\x12\x15\n\rfunction_name\x18\x02 \x01(\t\x12\x12\n\nclass_name\x18\x03 \x01(\t\x12\x14\n\x0cpackage_name\x18\x04 \x01(\t\x12\x13\n\x0breturn_type\x18\x05 \x01(\t\x12\x0f\n\x07\x61\x64\x64ress\x18\x06 \x01(\x04\x12\x46\n\x04\x61rgs\x18\x07 \x03(\x0b\x32\x38.ostorlab.agent.message.proto.v3.capture.stack_trace.Arg\"2\n\x05Input\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x0c\x12\x0c\n\x04type\x18\x03 \x01(\t\"\xc2\x01\n\x07Message\x12J\n\x06\x66rames\x18\x01 \x03(\x0b\x32:.ostorlab.agent.message.proto.v3.capture.stack_trace.Frame\x12\x11\n\tthread_id\x18\x02 \x01(\t\x12\x0c\n\x04time\x18\x03 \x01(\x02\x12J\n\x06inputs\x18\x04 \x03(\x0b\x32:.ostorlab.agent.message.proto.v3.capture.stack_trace.Input')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'ostorlab.agent.message.proto.v3.capture.stack_trace.stack_trace_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _ARG._serialized_start=126
  _ARG._serialized_end=174
  _FRAME._serialized_start=177
  _FRAME._serialized_end=378
  _INPUT._serialized_start=380
  _INPUT._serialized_end=430
  _MESSAGE._serialized_start=433
  _MESSAGE._serialized_end=627
# @@protoc_insertion_point(module_scope)
