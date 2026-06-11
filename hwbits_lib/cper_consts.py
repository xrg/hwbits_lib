"""Constants for CPER data

As taken from the standard:
"""

from enum import Enum
from typing import NamedTuple
from uuid import UUID


class Acronym(NamedTuple):
    short: str
    full: str

    def __str__(self):
        return self.full

    def __eq__(self, other):
        if isinstance(other, Acronym) and other.short == self.short:
            return True
        if isinstance(other, str) and other == self.short:
            return True
        return False


class Severity(Enum):
    Recoverable = 0
    Fatal = 1
    Corrected = 2
    Informational = 3


NotificationTypes = {
   UUID('{2dce8bb1-bdd7-450e-b9ad-9cf4ebd4f890}'): Acronym("CMC", "Corrected Machine Check"),
   UUID('{4e292f96-d843-4a55-a8c2-d481f27ebeee}'): Acronym("CPE", "Corrected Platform Error"),
   UUID('{e8f56ffe-919c-4cc5-ba88-65abe14913bb}'): Acronym("MCE", "Machine Check Exception"),
   UUID('{cf93c01f-1a16-4dfc-b8bc-9c4daf67c104}'): Acronym("PCIe", "PCIe Error"),
   UUID('{cc5263e8-9308-454a-89d0-340bd39bc98e}'): Acronym("INIT", "INIT Record"),
   UUID('{5bad89ff-b7e6-42c9-814a-cf2485d6e98a}'): Acronym("NMI", "Non-Maskable Interrupt"),
   UUID('{3d61a466-ab40-409a-a698-f362d464b38f}'): Acronym("Boot", "BOOT Error Record"),
   UUID('{667dd791-c6b3-4c27-8a6b-0f8e722deb41}'): Acronym("DMAr", "DMA Remapping Error"),
   UUID('{9a78788a-bbe8-11e4-809e-67611e5d46b0}'): Acronym("SEA", "Synchronous External Abort"),
   UUID('{5c284c81-b0ae-4e87-a322-b04c85624323}'): Acronym("SEI", "SError Interrupt"),
   UUID('{09a9d5ac-5204-4214-96e5-94992e752bcd}'): Acronym("PEI", "Platform Error Interrupt"),
   UUID('{69293bc9-41df-49a3-b4bd-4fb0db3041f6}'): Acronym("CXL Component", "CXL component"),
}
