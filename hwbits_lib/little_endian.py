# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

"""Little endian variants of common multi-byte types

Separated into a module so that you can simply do::

  from hwbits_lib.little_endian import ULong

and then use `ULong` in your code with implicit endianness
"""

from __future__ import annotations

import struct

from .hwstructs import DataStruct2Enum, DataStruct2Member, DynSizeBase, \
        HexFormat, GUID_base, MappedGUID_base, Static


class GUID(GUID_base):
    _big_endian = False


class MappedGUID(MappedGUID_base):
    _big_endian = False


class UShort(DataStruct2Member):
    _struct_fmt = "<H"


class ULong(DataStruct2Member):
    _struct_fmt = "<L"


class ULong64(DataStruct2Member):
    _struct_fmt = "<Q"


class Address32(HexFormat, ULong):
    """A 32-bit address"""


class Address64(HexFormat, ULong64):
    """A 64-bit address"""


class StaticUL(Static):
    def __init__(self, offset: int, expected: int):
        super().__init__(offset, expected=struct.pack("<L", expected))


class ULongEnum(DataStruct2Enum):
    _struct_fmt = "<L"


class DynSizeUL(ULong, DynSizeBase):
    """ULong, also used for size of the structure"""
