import json
from functools import partial
from inspect import EndOfBlock
from io import DEFAULT_BUFFER_SIZE
from pathlib import Path
from typing import Any, Optional
from uu import encode

from pydantic import BaseModel, Field

CHAR_ENCODING = {
    128: "A",
    129: "B",
    130: "C",
    131: "D",
    132: "E",
    133: "F",
    134: "G",
    135: "H",
    136: "I",
    137: "J",
    138: "K",
    139: "L",
    140: "M",
    141: "N",
    142: "O",
    143: "P",
    144: "Q",
    145: "R",
    146: "S",
    147: "T",
    148: "U",
    149: "V",
    150: "W",
    151: "X",
    152: "Y",
    153: "Z",
    154: "(",
    155: ")",
    156: ":",
    157: ";",
    158: "[",
    159: "]",
    160: "a",
    161: "b",
    162: "c",
    163: "d",
    164: "e",
    165: "f",
    166: "g",
    167: "h",
    168: "i",
    169: "j",
    170: "k",
    171: "l",
    172: "m",
    173: "n",
    174: "o",
    175: "p",
    176: "q",
    177: "r",
    178: "s",
    179: "t",
    180: "u",
    181: "v",
    182: "w",
    183: "x",
    184: "y",
    185: "z",
}


class InvalidPokemonLevel(Exception):
    pass


class PokemonBase(BaseModel):
    index: int = Field(..., alias="Index")
    pokedex: str = Field(..., alias="Pokedex")
    pokemon: str = Field(..., alias="Pokemon")
    type_1: str = Field(..., alias="Type 1")
    type_2: str = Field(..., alias="Type 2")


class Pokemon(PokemonBase):
    hex: str

    class Config:
        allow_population_by_field_name = True


class Pokedex(BaseModel):
    pokemon: list[Pokemon]

    def get(self, key: str, value: str):
        return [pokemon for pokemon in self.pokemon if getattr(pokemon, key) == value]


def is_missingno_info(pokemon: dict):
    return pokemon["Index"] is None


def get_pokedex():
    path = Path("./pokedex.json")
    pokemons: list[Pokemon] = []
    with path.open("r") as file:
        pokemon_file = json.load(file)
        for i in range(0, len(pokemon_file) - 1):
            current_pokemon = pokemon_file[i]
            next_pokemon = pokemon_file[i]
            if is_missingno_info(current_pokemon):
                continue
            if is_missingno_info(next_pokemon):
                current_pokemon["Pokemon"] += next_pokemon["Pokemon"]
            pokemon_base = PokemonBase(**current_pokemon)
            pokemon = Pokemon(**pokemon_base.dict(), hex=hex(pokemon_base.index))
            pokemons.append(pokemon)

    return Pokedex(pokemon=pokemons)


def file_byte_iterator(path):
    """given a path, return an iterator over the file
    that lazily loads the file
    """
    path = Path(path)
    with path.open("rb") as file:
        reader = partial(file.read1, DEFAULT_BUFFER_SIZE)
        file_iterator = iter(reader, bytes())
        for chunk in file_iterator:
            # for byte in chunk:
            #     yield hex(byte)
            yield from chunk


def get_pokemon_level(level: int) -> str:
    """Obtains pokemon level in hex"""
    if level <= 100:
        return hex(level)
    raise InvalidPokemonLevel


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
        return None

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
        if before[i] == 36:
            if after[i] == 34:
                return changes_in_mem.append(hex(i))
    return changes_in_mem


def filter_bewteen(int_list: list[int], start: int, end: int) -> list[int]:
    result = []
    for i in result:
        if i > start and i < end:
            result.append(i)
    return result


FIRST_PARTY_POKEMON_LOCATION = 0xD164
DUMMY_STRING_LOCATION = 0xD2EC
FIST_PARTY_POKEMON_NAME_LOCATION = 0xF2B6

encoded_str = get_encoded_str("KANGASKHAN")
# encoded_str = get_encoded_str("ONIX")
# encoded_str = get_encoded_str("PIDGEY")
# encoded_str = get_encoded_str("PARASECT")
# encoded_str = get_encoded_str("TENTACOOL")
set = list(file_byte_iterator(BEFORE_PATH))
# print(list(map(lambda x: int(x, 16), get_subset_location(set, encoded_str))))
print(get_subset_location(set, encoded_str))
