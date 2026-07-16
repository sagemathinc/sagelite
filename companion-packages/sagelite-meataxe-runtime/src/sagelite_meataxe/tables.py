from __future__ import annotations

import os
import struct
from pathlib import Path


FIELD_SIZES = (
    2, 3, 4, 5, 7, 8, 9, 11, 13, 16, 17, 19, 23, 25, 27, 29, 31, 32, 37,
    41, 43, 47, 49, 53, 59, 61, 64, 67, 71, 73, 79, 81, 83, 89, 97, 101,
    103, 107, 109, 113, 121, 125, 127, 128, 131, 137, 139, 149, 151, 157,
    163, 167, 169, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229,
    233, 239, 241, 243, 251,
)

# SharedMeatAxe 1.0.2 writes one fixed-size FieldData_t in format version 6.
TABLE_SIZE = 139_364
TABLE_FORMAT_VERSION = 6
_HEADER = struct.Struct("<5I")


def table_name(field_size: int) -> str:
    return f"p{field_size:03d}.zzz"


def validate_table(path: str | os.PathLike[str], field_size: int) -> str | None:
    """Return an explanation when ``path`` is not a usable field table."""
    table = Path(path)
    try:
        size = table.stat().st_size
    except OSError as error:
        return f"{table.name} is unavailable: {error}"

    if size != TABLE_SIZE:
        return f"{table.name} has size {size}, expected {TABLE_SIZE}"

    try:
        with table.open("rb") as handle:
            header = handle.read(_HEADER.size)
    except OSError as error:
        return f"{table.name} is unreadable: {error}"
    if len(header) != _HEADER.size:
        return f"{table.name} has a truncated header"

    characteristic, _generator, order, _packing, version = _HEADER.unpack(header)
    if order != field_size:
        return f"{table.name} declares GF({order}), expected GF({field_size})"
    expected_characteristic = next(
        divisor
        for divisor in range(2, field_size + 1)
        if field_size % divisor == 0
    )
    if characteristic != expected_characteristic:
        return (
            f"{table.name} declares characteristic {characteristic}, "
            f"expected {expected_characteristic} for GF({field_size})"
        )
    if version != TABLE_FORMAT_VERSION:
        return (
            f"{table.name} uses table format {version}, "
            f"expected {TABLE_FORMAT_VERSION}"
        )
    return None


def table_errors(
    directory: str | os.PathLike[str],
    field_sizes: tuple[int, ...] = FIELD_SIZES,
) -> list[str]:
    """Return all invalid or missing SharedMeatAxe tables in ``directory``."""
    root = Path(directory)
    return [
        error
        for field_size in field_sizes
        if (error := validate_table(root / table_name(field_size), field_size))
    ]


__all__ = [
    "FIELD_SIZES",
    "TABLE_FORMAT_VERSION",
    "TABLE_SIZE",
    "table_errors",
    "table_name",
    "validate_table",
]
