# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

"""Parser of Common Platform Error Record (CPER)
"""

import time

from .hwstructs import (
    DataStruct,
    HwBytes,
    MultiSectionsVar,
    Nested,
    ParentBody,
    Reg,
    Static,
    Text,
    UChar,
)
from .little_endian import DynSizeUL, GUID, MappedGUID, \
        StaticUL, ULong, ULong64, ULongEnum, UShort
from .registers import HwBits, HwRegister

from .cper_consts import NotificationTypes, Severity


class CPER_valid_bits(HwRegister):
    platform_id = HwBits(0)
    timestamp = HwBits(1)
    partition_id = HwBits(2)


class CPER_flags(HwRegister):
    recovered = HwBits(0)
    preverr = HwBits(1, doc="Qualifies an error condition as one "
                            "that occurred during a previous session.")
    simulated = HwBits(2, doc="Intentionally simulated/injected")


class CPER_revision(DataStruct):
    minor = UChar(0)
    major = UChar(1)

    def __str__(self):
        return f"{self.major}.{self.minor}"


class CPER_section_valid(HwRegister):
    FRU_id = HwBits(0)
    FRU_text = HwBits(1)


class CPER_section_flags(HwRegister):
    primary = HwBits(0)
    containment_warning = HwBits(1)
    reset = HwBits(2)
    threshold_exceeded = HwBits(3)
    unaccessible = HwBits(4)
    latent = HwBits(5)
    propagated = HwBits(6)
    overflow = HwBits(7)


class CPER_section_descr(DataStruct):
    _name_var = "section_type"

    offset = ULong(0)
    length = ULong(4)
    revision = Nested(8, CPER_revision)
    valid_bits = Reg(10, 1, CPER_section_valid)
    flags = Reg(12, 4, CPER_section_flags)

    section_type = GUID(16)
    FRU_id = GUID(32)
    severity = ULongEnum(48, Severity)
    FRU_text = Text(52, 20)

    body = ParentBody("offset", "length")


class CPER_tstamp_bits(HwRegister):
    precise = HwBits(0)


class CPER_timestamp(DataStruct):
    seconds = UChar(0)
    minutes = UChar(1)
    hours = UChar(2)
    flags = Reg(3, 1, CPER_tstamp_bits)
    day = UChar(4)
    month = UChar(5)
    year = UChar(6)
    century = UChar(7)

    def __str__(self):
        return f"{self.century-1}{self.year:02d}-{self.month:02d}-{self.day:02d} " \
                f"{self.hours:02d}:{self.minutes:02d}:{self.seconds:02d}"

    @property
    def datetime(self) -> int:
        return self.__int__()

    def __int__(self):
        year = (self.century - 1) * 100 + self.year
        ts = time.mktime((year, self.month, self.day,
                          self.hours, self.minutes, self.seconds,
                          -1, -1, -1))
        return int(ts)


class CPER(DataStruct):
    _name_var = "notification_type"

    head = Static(0, b"CPER")
    revision = Nested(4, CPER_revision)
    head_end = StaticUL(6, 0xFFFFFFFF)
    section_count = UShort(10)
    error_severity = ULongEnum(12, Severity)
    valid_bits = Reg(16, 4, CPER_valid_bits)

    rec_length = DynSizeUL(20)

    timestamp = Nested(24, CPER_timestamp)
    platform_id = GUID(32)
    partition_id = GUID(48)
    creator_id = GUID(64)
    notification_type = MappedGUID(80, NotificationTypes)

    record_id = ULong64(96)
    flags = Reg(104, 4, CPER_flags)
    persistence_info = HwBytes(108, 8)

    sections = MultiSectionsVar(128, "section_count", CPER_section_descr)
