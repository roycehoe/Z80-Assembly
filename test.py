from dataclasses import dataclass, field
from pathlib import Path
from functools import partial
from io import DEFAULT_BUFFER_SIZE


class InvalidPokemonLevel(Exception):
    pass

@dataclass
class Pokemon:
    index: int
    pokedex_no: str
    name: str
    type_1: str
    type_2: str

@dataclass
class Pokedex:
    pokemon: list[Pokemon]


def file_byte_iterator(path = './Pokemon_red.dump'):
    """given a path, return an iterator over the file
    that lazily loads the file
    """
    path = Path(path)
    with path.open('rb') as file:
        reader = partial(file.read1, DEFAULT_BUFFER_SIZE)
        file_iterator = iter(reader, bytes())
        for chunk in file_iterator:
            for byte in chunk:
                yield hex(byte)
            # yield from chunk

def get_pokemon_level(level: int) -> str:
    """Obtains pokemon level in hex"""
    if level <= 100:
        return hex(level)
    raise InvalidPokemonLevel




CURRENT_PARTY: list[int] = []

print(list(file_byte_iterator()))