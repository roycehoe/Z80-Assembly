from functools import partial
from io import DEFAULT_BUFFER_SIZE
from pathlib import Path
from typing import Any

from data import CHAR_ENCODING


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


def get_encoded_str(raw_str: str) -> list[int]:
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


BEFORE_PATH = "before.dump"
AFTER_PATH = "after.dump"
TAKE_FROM = 49152
TAKE_TO = 57344


def get_change_in_mem() -> list[str]:
    changes_in_mem: list[str] = []
    before = list(file_byte_iterator(BEFORE_PATH))
    after = list(file_byte_iterator(AFTER_PATH))
    for i in range(len(before)):
        if before[i] == 78:
            if after[i] == 96:
                changes_in_mem.append(hex(i))
    return changes_in_mem


def filter_bewteen(int_list: list[int], start: int, end: int) -> list[int]:
    result = []
    for i in result:
        if i > start and i < end:
            result.append(i)
    return result


FIRST_PARTY_POKEMON_LOCATION = 0xD164
DUMMY_STRING_LOCATION = 0xD2EC
FIST_PARTY_POKEMON_NAME_LOCATION = 0xF2B6  # +10 for subsequent pokemon in party
LAST_PARTY_LEVEL = (
    0xF268  # followed by max health. # Subsequent 44 hex belongs to the pokemon somehow
)

print(get_change_in_mem())
