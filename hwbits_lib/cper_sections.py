# Copyright (c) Panos Christeas
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

"""Common CPER sections, as defined in the standard

"""

from uuid import UUID

from hwbits_lib.hwstructs import Reg, Array, UChar, MultiSectionsVar, DataStruct
from hwbits_lib.little_endian import GUID, ULong64
from hwbits_lib.registers import HwRegister, HwBits
from hwbits_lib.generic_cper import CPER_section_body


class ProcessorGeneric(CPER_section_body, uuid=UUID('9876ccad-47b4-4bdb-b65e-16f193c4f3db')):
    ...


class Proc_x86Valid(HwRegister):
    local_apic_id = HwBits(0)
    cpuid = HwBits(1)
    num_pei = HwBits(2, 7)
    num_pci = HwBits(8, 13)


class PEI_Valid_bits(HwRegister):
    check_info = HwBits(0)
    target_id = HwBits(1)
    request_id = HwBits(2)
    responder_id = HwBits(3)
    instruction_pointer = HwBits(4)


class Proc_x86PEI(DataStruct):
    structure_type = GUID(0)
    valid_bits = Reg(16, 8, PEI_Valid_bits)
    check_info = ULong64(24)
    target_id = ULong64(32)
    request_id = ULong64(40)
    responder_id = ULong64(48)
    instruction_pointer = ULong64(56)


# class ProcessorSpecific(CPER_section_body, uuid=UUID('')
class Processor_x86(CPER_section_body, uuid=UUID('dc3ea0b0-a144-4797-b95b-53fa242b6e1d')):
    valid_bits = Reg(0, 8, Proc_x86Valid)
    apic_id = Reg(8, 8, HwRegister)
    cpuid_info = Array(16, UChar, size=48)

    pei = MultiSectionsVar(64, 'valid_bits.num_pei', Proc_x86PEI)


class Processor_IPF(CPER_section_body, uuid=UUID('e429faf1-3cb7-11d4-bca7-0080c73c8881')):
    pass


class Processor_ARM(CPER_section_body, uuid=UUID('e19e3d16-bc11-11e4-9caa-c2051d5d46b0')):
    pass


class PlatformMemory(CPER_section_body, uuid=UUID('a5bc1114-6f64-4ede-b863-3e83ed7c83b1')):
    pass


class PCIe(CPER_section_body, uuid=UUID('D995E954-BBC1-430F-AD91-B44DCB3C6F35')):
    pass


class FirmwareErrorRecordReference(CPER_section_body, uuid=UUID('81212A96-09ED-4996-9471-8D729C8E69ED')):
    pass


class PCIBus(CPER_section_body, uuid=UUID('c5753963-3b84-4095-bf78-eddad3f9c9dd')):
    pass


class PCIComponent(CPER_section_body, uuid=UUID('eb5e4685-ca66-4769-b6a2-26068b001326')):
    pass


class DMArGeneric(CPER_section_body, uuid=UUID('5b51fef7-c79d-4434-8f1b-aa62de3e2c64')):
    pass


class IntelVT_specific_DMAr(CPER_section_body, uuid=UUID('71761d37-32b2-45cd-a7d0-b0fedd93e8cf')):
    pass


class IOMMU_DMAr(CPER_section_body, uuid=UUID('036f84e1-7f37-428c-a79e-575fdfaa84ec')):
    pass
