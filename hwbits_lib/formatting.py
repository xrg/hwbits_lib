# Copyright (c) Panos Christeas
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from __future__ import annotations

from textwrap import TextWrapper

from .hwstructs import Array, DataStruct, SparseArray
from .registers import FieldValidBits


def format_obj(obj, name: str = "", **wrap_kwargs):
    wrap_kwargs.setdefault('width', 100)
    wrapper = TextWrapper(**wrap_kwargs)

    out = list(_inner_format(obj, name, wrapper))
    return '\n'.join(out)


def print_obj(obj, name: str = "", **wrap_kwargs):
    wrap_kwargs.setdefault('width', 100)
    wrapper = TextWrapper(**wrap_kwargs)

    for line in _inner_format(obj, name, wrapper):
        print(line)


def _dummy_fmt(name, val):
    return f"{name}={val!r}"


def _sub_wrap(wrapper: TextWrapper) -> TextWrapper:
    # make a copy
    r = wrapper.__class__(**vars(wrapper))
    r.initial_indent += "  "
    r.subsequent_indent += "  "
    return r


def _inner_format(obj, name: str, wrapper: TextWrapper):

    if isinstance(obj, DataStruct):
        yield from wrapper.wrap(f"{name}: {obj}")
        sw = _sub_wrap(wrapper)
        valid_fields = {}

        for iname, ival in vars(obj).items():
            if not valid_fields.get(iname, True):
                # field has 'valid.<field>==0'
                # this assumes that the validity bits are enumerated before this
                continue
            if isinstance(ival, DataStruct):
                yield from _inner_format(ival, iname, sw)
                continue

            try:
                fmt = getattr(obj.__class__, iname)._format
            except AttributeError as e:
                # *-*
                print(f"No formatting for {obj.__class__.__name__}.{iname}: {e}")
                fmt = _dummy_fmt

            yield from sw.wrap(fmt(iname, ival))

            if isinstance(ival, Array._Slicer):
                sw = _sub_wrap(sw)
                sparse = False
                try:
                    sparse = isinstance(ival._parent, SparseArray)
                    ifmt = ival._parent._type_inst._format
                except AttributeError:
                    ifmt = _dummy_fmt

                for n, lval in enumerate(ival):
                    if sparse and not lval:
                        continue
                    yield from sw.wrap(ifmt(f"{iname}[{n}]", lval))

            elif isinstance(ival, list):
                # this is in addition to the "header" of the list above
                sw = _sub_wrap(sw)  # one more indent
                for n, lval in enumerate(ival):
                    yield from _inner_format(lval, f"{iname}[{n}]", sw)
                continue

            if isinstance(ival, FieldValidBits):
                for k in ival:
                    valid_fields[k] = getattr(ival, k)

    elif isinstance(obj, list):
        yield from wrapper.wrap(f"{name}: list[{len(obj)}]")
        sw = _sub_wrap(wrapper)
        for n, lval in enumerate(obj):
            yield from _inner_format(lval, f"{name}#{n}", sw)
    else:
        yield from wrapper.wrap(f"{name}: {obj!r}")

