"""Streaming reader for R .rda/.rds files that keeps only the columns you ask for.

Why this exists: the GSS cumulative file (gssr's gss_all.rda) is ~75,700 rows x
~6,900 columns. Loading all of it needs well over the RAM of a laptop or a
small cloud box. This walks the R serialization stream once to list the column
names, then again keeping only the requested columns (with their variable
label and value labels).

Only the subset of the R serialization format that data frames use is
implemented fully; closures/bytecode/environments are parsed just enough to skip.
"""
from __future__ import annotations

import bz2
import gzip
import lzma
import struct
from typing import Any, Iterable

import numpy as np

NILVALUE, GLOBALENV, UNBOUND, MISSINGARG, BASENS = 254, 253, 252, 251, 250
NAMESPACESXP, PACKAGESXP, PERSISTSXP = 249, 248, 247
EMPTYENV, BASEENV, ATTRLANG, ATTRLIST, ALTREP = 242, 241, 240, 239, 238
REFSXP = 255
NA_INT = -2147483648


def _open(path: str):
    with open(path, "rb") as f:
        magic = f.read(6)
    if magic.startswith(b"\xfd7zXZ"):
        return lzma.open(path, "rb")
    if magic.startswith(b"BZh"):
        return bz2.open(path, "rb")
    if magic.startswith(b"\x1f\x8b"):
        return gzip.open(path, "rb")
    return open(path, "rb")


class _Reader:
    def __init__(self, stream, keep: set[str] | None):
        self.s = stream
        self.refs: list[Any] = []
        self.keep = keep  # None = names-only pass

    # --- primitives ---------------------------------------------------
    def read(self, n: int) -> bytes:
        b = self.s.read(n)
        if len(b) != n:
            raise EOFError("unexpected end of R stream")
        return b

    def skip(self, n: int) -> None:
        while n > 0:
            chunk = self.s.read(min(n, 1 << 24))
            if not chunk:
                raise EOFError
            n -= len(chunk)

    def int(self) -> int:
        return struct.unpack(">i", self.read(4))[0]

    def length(self) -> int:
        n = self.int()
        if n == -1:
            hi, lo = self.int(), self.int()
            n = (hi << 32) + lo
        return n

    # --- items --------------------------------------------------------
    def item(self, want_data: bool = True) -> Any:
        flags = self.int()
        t = flags & 0xFF
        has_attr = bool(flags & (1 << 9))
        has_tag = bool(flags & (1 << 10))

        if t == REFSXP:
            idx = flags >> 8
            if idx == 0:
                idx = self.int()
            return self.refs[idx - 1]
        if t in (NILVALUE, GLOBALENV, UNBOUND, MISSINGARG, BASENS, EMPTYENV, BASEENV):
            return None
        if t in (PERSISTSXP, NAMESPACESXP, PACKAGESXP):
            self.int()  # 0
            n = self.int()
            for _ in range(n):
                self.item()
            self.refs.append(None)
            return None
        if t == 1:  # SYMSXP
            name = self.item()
            self.refs.append(name)
            return name
        if t in (2, 3, 5, 6, 17, ATTRLANG, ATTRLIST):  # pairlist-like
            out = []
            while True:
                attr = self.item() if has_attr else None
                tag = self.item() if has_tag else None
                car = self.item(want_data)
                out.append((tag, car))
                # cdr: peek next flags
                flags = self.int()
                t2 = flags & 0xFF
                if t2 in (2, ATTRLIST):
                    has_attr = bool(flags & (1 << 9))
                    has_tag = bool(flags & (1 << 10))
                    continue
                # not a pairlist continuation: decode the cdr item normally
                self._item_from_flags(flags)
                break
            return out
        return self._item_from_flags(flags, want_data)

    def _item_from_flags(self, flags: int, want_data: bool = True) -> Any:
        t = flags & 0xFF
        has_attr = bool(flags & (1 << 9))
        has_tag = bool(flags & (1 << 10))
        if t in (NILVALUE, GLOBALENV, UNBOUND, MISSINGARG, BASENS, EMPTYENV, BASEENV):
            return None
        if t == REFSXP:
            idx = flags >> 8
            if idx == 0:
                idx = self.int()
            return self.refs[idx - 1]
        if t == 1:
            name = self.item()
            self.refs.append(name)
            return name
        if t in (2, 3, 5, 6, 17, ATTRLANG, ATTRLIST):
            attr = self.item() if has_attr else None
            tag = self.item() if has_tag else None
            car = self.item()
            cdr = self.item()
            return [(tag, car)] + (cdr if isinstance(cdr, list) else [])
        if t == 4:  # ENVSXP
            self.refs.append(None)
            self.int()
            self.item(); self.item(); self.item(); self.item()
            return None
        if t == 9:  # CHARSXP
            n = self.int()
            if n == -1:
                return None
            return self.read(n).decode("utf-8", "replace")
        if t in (10, 13):  # LGLSXP / INTSXP
            n = self.length()
            if want_data:
                arr = np.frombuffer(self.read(4 * n), dtype=">i4").astype(np.float64)
                arr[arr == NA_INT] = np.nan
            else:
                self.skip(4 * n)
                arr = None
            attrs = self.attrs() if has_attr else {}
            return ("vec", arr, attrs)
        if t == 14:  # REALSXP
            n = self.length()
            if want_data:
                arr = np.frombuffer(self.read(8 * n), dtype=">f8").astype(np.float64)
            else:
                self.skip(8 * n)
                arr = None
            attrs = self.attrs() if has_attr else {}
            return ("vec", arr, attrs)
        if t == 15:
            n = self.length()
            self.skip(16 * n)
            attrs = self.attrs() if has_attr else {}
            return ("vec", None, attrs)
        if t == 16:  # STRSXP
            n = self.length()
            vals = [self.item() for _ in range(n)]
            attrs = self.attrs() if has_attr else {}
            return ("str", vals, attrs)
        if t in (19, 20):  # VECSXP / EXPRSXP
            n = self.length()
            elems = [self._col(i) for i in range(n)] if t == 19 else [self.item() for _ in range(n)]
            attrs = self.attrs() if has_attr else {}
            return ("list", elems, attrs)
        if t == 24:
            n = self.length()
            self.skip(n)
            attrs = self.attrs() if has_attr else {}
            return ("raw", None, attrs)
        if t == 25:  # S4
            attrs = self.attrs() if has_attr else {}
            return ("s4", None, attrs)
        if t == 22:  # EXTPTR
            self.refs.append(None)
            self.item(); self.item()
            if has_attr:
                self.attrs()
            return None
        if t == 23:
            self.refs.append(None)
            if has_attr:
                self.attrs()
            return None
        if t == ALTREP:
            info = self.item(); state = self.item(); attr = self.item()
            return ("altrep", state, attr)
        raise ValueError(f"unsupported R SEXP type {t}")

    # Columns of the top-level list: decide whether to keep data.
    def _col(self, i: int):
        want = self.keep is not None and i in self.keep_idx
        return self.item(want_data=want)

    def attrs(self) -> dict:
        pl = self.item()
        out = {}
        if isinstance(pl, list):
            for tag, val in pl:
                out[tag] = val
        return out


def _header(r: _Reader) -> None:
    head = r.read(5)
    if head in (b"RDX2\n", b"RDX3\n"):
        fmt = r.read(2)
    else:
        fmt = head[:2]
        # rds: no RDX header; we already consumed 3 extra bytes of the version int
        raise ValueError("pass an .rda file saved with save()")
    if fmt != b"X\n":
        raise ValueError("only XDR (big-endian) R files are supported")
    version = r.int(); r.int(); r.int()
    if version == 3:
        n = r.int(); r.read(n)


def _top_dataframe(r: _Reader):
    flags = r.int()  # LISTSXP of (name -> object)
    has_attr = bool(flags & (1 << 9))
    if has_attr:
        r.attrs()
    tag = r.item()
    obj = r.item()
    return tag, obj


def column_names(path: str) -> list[str]:
    with _open(path) as s:
        r = _Reader(s, keep=None)
        r.keep_idx = set()
        _header(r)
        _, obj = _top_dataframe(r)
    kind, elems, attrs = obj
    return list(attrs["names"][1])


def read_columns(path: str, cols: Iterable[str], names: list[str] | None = None):
    """Return (DataFrame, meta) for the requested columns.

    meta[col] = {"label": variable label, "labels": {code: text}}
    """
    import pandas as pd

    names = names or column_names(path)
    cols = list(cols)
    missing = [c for c in cols if c not in names]
    if missing:
        raise KeyError(f"not in file: {missing}")
    idx = {names.index(c): c for c in cols}
    with _open(path) as s:
        r = _Reader(s, keep=set(cols))
        r.keep_idx = set(idx)
        _header(r)
        _, obj = _top_dataframe(r)
    _, elems, _ = obj
    data, meta = {}, {}
    for i, c in idx.items():
        kind, arr, attrs = elems[i]
        data[c] = arr
        label = attrs.get("label")
        labels = attrs.get("labels")
        lab = {}
        if labels and labels[0] == "vec" and labels[1] is not None:
            nm = labels[2].get("names")
            if nm:
                lab = {float(v): t for v, t in zip(labels[1], nm[1])}
        meta[c] = {
            "label": label[1][0] if label and label[0] == "str" else None,
            "labels": lab,
        }
    return pd.DataFrame(data), meta
