#!/usr/bin/env python3

import argparse
import logging
import os.path

from hwbits_lib.hwstructs import DataStruct
from hwbits_lib.generic_cper import CPER

import hwbits_lib.cper_sections as _


def print_cper(fname: str):
    with open(os.path.expanduser(fname), 'rb') as fp:
        cp = CPER(fp)

    print(f"File: {fname}")
    print(f"CPER v{cp.revision} "
          + f"@{cp.timestamp}" if cp.valid_bits.timestamp else '')
    print(f"Severity: {cp.error_severity} Creator: {cp.creator_id}")
    if cp.valid_bits.platform_id:
        print(f"Platform: {cp.platform_id}")
    if cp.valid_bits.partition_id:
        print(f"Partition: {cp.partition_id}")

    print(f"  notification: {cp.notification_type}")
    for n, sec in enumerate(cp.sections):
        xx = ""
        if sec.valid_bits.FRU_text:
            xx = f" on {sec.FRU_text}"
        if sec.valid_bits.FRU_id:
            xx += f" [{sec.FRU_id}]"
        print(f"  section {n}: v{sec.revision} {sec.severity}{xx}")
        print(f"    type={sec.section_type} , flags={sec.flags}")

        print(f"    body type: {sec.body}")
        for key, val in vars(sec.body).items():
            print(f"      {key}={val!r}")
            if isinstance(val, DataStruct):
                for k2, v2 in vars(val).items():
                    if isinstance(v2, int) and not k2.endswith(('len', 'size')):
                        print(f"        {k2}=0x{v2:x}")
                    else:
                        print(f"        {k2}={v2!r}")

    print()


def main():
    parser = argparse.ArgumentParser(description="Analyze a number of CPER files")
    parser.add_argument("files", nargs="+")

    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)

    log = logging.getLogger('main')
    for fname in args.files:
        try:
            print_cper(fname)
        except Exception:
            log.exception("Cannot decode %s:", fname)


if __name__ == '__main__':
    main()
