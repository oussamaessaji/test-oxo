# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: v3/fingerprint/ip/v6/library/library.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='v3/fingerprint/ip/v6/library/library.proto',
  package='v3.fingerprint.ip.v6.library',
  syntax='proto2',
  serialized_options=None,
  serialized_pb=_b('\n*v3/fingerprint/ip/v6/library/library.proto\x12\x1cv3.fingerprint.ip.v6.library\"\xbf\x01\n\x07Message\x12\x0c\n\x04host\x18\x01 \x01(\t\x12\x0c\n\x04mask\x18\x02 \x01(\t\x12\x12\n\x07version\x18\x03 \x01(\x05:\x01\x36\x12\x14\n\x0clibrary_type\x18\x04 \x01(\t\x12\x14\n\x0clibrary_name\x18\x05 \x01(\t\x12\x17\n\x0flibrary_version\x18\x06 \x01(\t\x12\x0e\n\x06\x64\x65tail\x18\x07 \x01(\t\x12\x0f\n\x07service\x18\x08 \x01(\t\x12\x0c\n\x04port\x18\t \x01(\r\x12\x10\n\x08protocol\x18\n \x01(\t')
)




_MESSAGE = _descriptor.Descriptor(
  name='Message',
  full_name='v3.fingerprint.ip.v6.library.Message',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='host', full_name='v3.fingerprint.ip.v6.library.Message.host', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='mask', full_name='v3.fingerprint.ip.v6.library.Message.mask', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='version', full_name='v3.fingerprint.ip.v6.library.Message.version', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=True, default_value=6,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='library_type', full_name='v3.fingerprint.ip.v6.library.Message.library_type', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='library_name', full_name='v3.fingerprint.ip.v6.library.Message.library_name', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='library_version', full_name='v3.fingerprint.ip.v6.library.Message.library_version', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='detail', full_name='v3.fingerprint.ip.v6.library.Message.detail', index=6,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='service', full_name='v3.fingerprint.ip.v6.library.Message.service', index=7,
      number=8, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='port', full_name='v3.fingerprint.ip.v6.library.Message.port', index=8,
      number=9, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='protocol', full_name='v3.fingerprint.ip.v6.library.Message.protocol', index=9,
      number=10, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=77,
  serialized_end=268,
)

DESCRIPTOR.message_types_by_name['Message'] = _MESSAGE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Message = _reflection.GeneratedProtocolMessageType('Message', (_message.Message,), dict(
  DESCRIPTOR = _MESSAGE,
  __module__ = 'v3.fingerprint.ip.v6.library.library_pb2'
  # @@protoc_insertion_point(class_scope:v3.fingerprint.ip.v6.library.Message)
  ))
_sym_db.RegisterMessage(Message)


# @@protoc_insertion_point(module_scope)
