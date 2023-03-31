from enum import Enum, auto
from functools import partial
from io import DEFAULT_BUFFER_SIZE
from pathlib import Path
from typing import Any

from data import CHAR_ENCODING


class GameboyMemLocation(Enum):
    ROM0 = auto()
    ROM3 = auto()
    VRA0 = auto()
    SRA1 = auto()
    WRA0 = auto()
    WRA1 = auto()
    ECH0 = auto()
    ECH1 = auto()
    OAM = auto()
    UNLABELED = auto()
    IO = auto()
    HRAM = auto()


GAMEBOY_MEM_LOCATION_TO_RANGE_MAP: dict[GameboyMemLocation, range] = {
    GameboyMemLocation.ROM0: range(0, 0x4000),
    GameboyMemLocation.ROM3: range(0x4000, 0x8000),
    GameboyMemLocation.VRA0: range(0x8000, 0xA000),
    GameboyMemLocation.SRA1: range(0xA000, 0xC000),
    GameboyMemLocation.WRA0: range(0xC000, 0xD000),
    GameboyMemLocation.WRA1: range(0xD000, 0xE000),
    GameboyMemLocation.ECH0: range(0xE000, 0xF000),
    GameboyMemLocation.ECH1: range(0xF000, 0xFE00),
    GameboyMemLocation.OAM: range(0xFE00, 0xFEA0),
    GameboyMemLocation.UNLABELED: range(0xFEA0, 0xFF00),
    GameboyMemLocation.IO: range(0xFF00, 0xFF80),
    GameboyMemLocation.HRAM: range(0xFF80, 0xFFFF),
}


def get_gameboy_mem_location(hex: int):
    ...


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
