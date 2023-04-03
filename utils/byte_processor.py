from functools import partial
from io import DEFAULT_BUFFER_SIZE
from pathlib import Path
from typing import Any, Optional

from constants import (
    AFTER_PATH,
    BEFORE_PATH,
    CHAR_ENCODING,
    GAMEBOY_MEM_LOCATION_TO_RANGE_MAP,
    GameboyMemLocation,
)


def get_gameboy_mem_location(hex: int) -> Optional[GameboyMemLocation]:
    for key, value in GAMEBOY_MEM_LOCATION_TO_RANGE_MAP.items():
        if hex in value:
            return key
    return None


def file_byte_iterator(path):
    """given a path, return an iterator over the file
    that lazily loads the file
    """
    path = Path(path)
    with path.open("rb") as file:
        reader = partial(file.read1, DEFAULT_BUFFER_SIZE)
        file_iterator = iter(reader, bytes())
        for chunk in file_iterator:
            yield from chunk


def get_pokemon_chars(raw_str: str) -> list[int]:
    """Encodes a string to pokemon char encoding format in decimals"""
    encoded_str: list[int] = []
    for i in raw_str:
        for key, value in CHAR_ENCODING.items():
            if i == value:
                encoded_str.append(key)
                continue
    return encoded_str


def get_subset_location(set: list[Any], subset: list[Any]) -> list[int]:
    subset_locations = []
    if not all(x in set for x in subset):
        return subset_locations

    for i in range(len(set) - len(subset) + 1):
        if set[i : i + len(subset)] == subset:
            subset_locations.append(hex(i))

    return subset_locations


def get_change_in_mem(
    before_value: int,
    after_value: int,
    before_path: str = BEFORE_PATH,
    after_path: str = AFTER_PATH,
) -> list[str]:
    changes_in_mem: list[str] = []
    before = list(file_byte_iterator(before_path))
    after = list(file_byte_iterator(after_path))
    for i in range(len(before)):
        if before[i] == before_value:
            if after[i] == after_value:
                changes_in_mem.append(hex(i))
    return changes_in_mem
