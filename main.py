from dataclasses import dataclass
from enum import Enum, auto
from functools import partial
from io import DEFAULT_BUFFER_SIZE
from pathlib import Path
from typing import Any, Callable, Literal, Optional, Type

from pydantic import BaseModel, conint, constr, validator

from data import CHAR_ENCODING
from pokedex import get_pokedex


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


def _is_valid_pokemon_char(letter: str) -> bool:
    """Encodes a string to pokemon char encoding format in decimals"""
    for key, value in CHAR_ENCODING.items():
        if letter == value:
            return True
    return False


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


BEFORE_PATH = "before.dump"
AFTER_PATH = "after.dump"


def get_change_in_mem(
    before_path: str = BEFORE_PATH, after_path: str = AFTER_PATH
) -> list[str]:
    changes_in_mem: list[str] = []
    before = list(file_byte_iterator(before_path))
    after = list(file_byte_iterator(after_path))
    for i in range(len(before)):
        if before[i] == 78:
            if after[i] == 96:
                changes_in_mem.append(hex(i))
    return changes_in_mem


PokemonStatsType: Type[int] = conint(gt=0, lt=264)


class PokemonStats(BaseModel):
    level: PokemonStatsType
    health: PokemonStatsType
    attack: PokemonStatsType
    defence: PokemonStatsType
    speed: PokemonStatsType
    special: PokemonStatsType

    def _get_hex(self, stat: int) -> list[int]:
        first_hex = stat // 256  # 256 multiplier
        second_hex = stat % 256  # 1 multiplier
        return [first_hex, second_hex]

    def get_hex(self) -> list[int]:
        return [
            self.level,
            *self._get_hex(self.health),
            *self._get_hex(self.attack),
            *self._get_hex(self.defence),
            *self._get_hex(self.speed),
            *self._get_hex(self.special),
        ]


DUMMY_STRING_LOCATION = 0xD2EC

NEXT_PARTY_POKEMON_INDEX_STEP = 44
NEXT_PARTY_POKEMON_STATS_STEP = 1
NEXT_PARTY_POKEMON_NAME_STEP = 10

# MEMORY
MEM_FIRST_PARTY_POKEMON_INDEX_LOCATION = 0xD164
MEM_FIST_PARTY_POKEMON_NAME_LOCATION = 0xF2B5
MEM_FIRST_PARTY_POKEMON_STATS_LOCATION = 0xF18C

# SAVE FILE

SAVE_FILE_FIRST_PARTY_POKEMON_INDEX_LOCATION = None
SAVE_FILE_FIST_PARTY_POKEMON_NAME_LOCATION = None
SAVE_FILE_FIRST_PARTY_POKEMON_STATS_LOCATION = 0x2F55


def _get_pokemon_name(name: str) -> list[int]:
    """Pokemon names are stored in memory within exactly 10 hexadecimals"""
    name_in_pokemon_chars = get_pokemon_chars(name)
    while len(name_in_pokemon_chars) < 10:
        name_in_pokemon_chars.append(50)
    return name_in_pokemon_chars


save_file = list(file_byte_iterator("./PokemonRed.sav"))
subset = get_pokemon_chars("MOLTRES")
# print(subset)
# print(len(subset))

subset_location = get_subset_location(save_file, subset)
print(subset_location)
print(subset)
print(save_file[0x59A : 0x59A + 100])
# print(0x2F55)
# print(0xE2)
# print(save_file[0x2F55 : 0x2F55 + 100])


PartySlot = Literal[0, 1, 2, 3, 4, 5]


def _get_moded_party_pokemon_index(
    save_file: list[int], party_slot: PartySlot, moded_pokemon_index: int
) -> list[int]:
    start_mem_location = MEM_FIRST_PARTY_POKEMON_INDEX_LOCATION + (
        NEXT_PARTY_POKEMON_INDEX_STEP * party_slot
    )
    return [
        *save_file[:start_mem_location],
        moded_pokemon_index,
        *save_file[NEXT_PARTY_POKEMON_INDEX_STEP + start_mem_location :],
    ]


def _get_moded_party_pokemon_name(
    save_file: list[int], party_slot: PartySlot, moded_name: str
) -> list[int]:
    name_in_pokemon_chars = _get_pokemon_name(moded_name)

    start_mem_location = MEM_FIST_PARTY_POKEMON_NAME_LOCATION + (
        NEXT_PARTY_POKEMON_NAME_STEP * party_slot
    )
    return [
        *save_file[:start_mem_location],
        *name_in_pokemon_chars,
        *save_file[NEXT_PARTY_POKEMON_NAME_STEP + start_mem_location :],
    ]


def _get_moded_party_pokemon_stats(
    save_file: list[int], party_slot: PartySlot, moded_stats: PokemonStats
) -> list[int]:
    start_mem_location = MEM_FIRST_PARTY_POKEMON_STATS_LOCATION + (
        NEXT_PARTY_POKEMON_STATS_STEP * party_slot
    )
    return [
        *save_file[:start_mem_location],
        *moded_stats.get_hex(),
        *save_file[NEXT_PARTY_POKEMON_STATS_STEP + start_mem_location :],
    ]


class InvalidPokemonIndexError(Exception):
    pass


class InvalidPokemonCharacterError(Exception):
    pass


class PokemonMod(BaseModel):
    slot: PartySlot
    index: int
    name: str
    stats: PokemonStats

    @validator("index")
    def is_valid_pokemon_index(cls, v):
        pokedex = get_pokedex()
        pokemon_index = pokedex.get("index", v)
        if not pokemon_index:
            raise InvalidPokemonIndexError
        return v

    @validator("name")
    def is_valid_pokemon_name(cls, v):
        for letter in v:
            if not _is_valid_pokemon_char(letter):
                raise InvalidPokemonCharacterError
        return v


def get_moded_party(save_file: list[int], mod: PokemonMod) -> list[int]:
    res = _get_moded_party_pokemon_index(save_file, mod.slot, mod.index)
    res = _get_moded_party_pokemon_name(save_file, mod.slot, mod.name)
    res = _get_moded_party_pokemon_stats(save_file, mod.slot, mod.stats)
    return res
