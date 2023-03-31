from dataclasses import dataclass, field
import json
from pathlib import Path
from functools import partial
from io import DEFAULT_BUFFER_SIZE


class InvalidPokemonLevel(Exception):
    pass




@dataclass
class Pokemon:
    hex: str = field(init=False)
    index: int = field(metadata={"alias": 'Index'})
    pokedex_no: str = field(metadata={"alias": 'Pokedex'})
    name: str = field(metadata={"alias": 'Pokemon'})
    type_1: str = field(metadata={"alias": 'Type 1'})
    type_2: str = field(metadata={"alias": 'Type 2'})

    def __post_init__(self):
        self.hex = hex(self.index)


@dataclass
class Pokedex:
    pokemon: list[Pokemon]


def get_pokedex():
    path = Path('./pokedex.json')
    pokemons = []
    with path.open('r') as file:
        pokemon_file = json.load(file)
        for pokemon in pokemon_file:
            del pokemon["Hex"] # Hex in json is in string. Prefer to calculate this in Pokemon class
            pokemons.append(Pokemon(**pokemon))
    return Pokedex(pokemon=pokemons)

print(get_pokedex())






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