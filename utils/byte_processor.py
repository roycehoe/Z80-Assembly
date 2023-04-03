from dataclasses import dataclass
from enum import Enum, auto
from functools import partial
from io import DEFAULT_BUFFER_SIZE
from pathlib import Path
from typing import Any, Callable, Literal, Optional, Type

from pydantic import BaseModel, conint, constr, validator

from constants import (
    AFTER_PATH,
    BEFORE_PATH,
    CHAR_ENCODING,
    GAMEBOY_MEM_LOCATION_TO_RANGE_MAP,
    NEXT_PARTY_POKEMON_INDEX_STEP,
    NEXT_PARTY_POKEMON_NAME_STEP,
    NEXT_PARTY_POKEMON_STATS_STEP,
    PLAYER_PARTY_MAX_POKEMON,
    SAVE_FILE_FIRST_PARTY_POKEMON_INDEX_LOCATION,
    SAVE_FILE_FIRST_PARTY_POKEMON_STATS_LOCATION,
    SAVE_FILE_FIST_PARTY_POKEMON_NAME_LOCATION,
    GameboyMemLocation,
)
from pokedex import get_pokedex
from schemas.PokemonPartyModIn import PlayerPartyMod
from schemas.PokemonStats import PokemonStats


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
