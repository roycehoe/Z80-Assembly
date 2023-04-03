import json
from pathlib import Path

from constants import POKEDEX_PATH
from schemas.Pokedex import Pokedex, Pokemon, PokemonBase


class InvalidPokemonLevel(Exception):
    pass


def _is_missingno_info(pokemon: dict):
    return pokemon.get("Index") is None


def get_pokemon_level(level: int) -> str:
    """Obtains pokemon level in hex"""
    if level <= 100:
        return hex(level)
    raise InvalidPokemonLevel


def _get_pokemon_bases(pokedex_path: str = POKEDEX_PATH) -> list[PokemonBase]:
    pokemon_base: list[PokemonBase] = []

    path = Path(pokedex_path)
    with path.open("r") as file:
        pokemon_file = json.load(file)
        for i in range(
            0, len(pokemon_file) - 1
        ):  # cleans dirty data in pokedex.json file
            current_pokemon = pokemon_file[i]
            next_pokemon = pokemon_file[i]
            if _is_missingno_info(current_pokemon):
                continue
            if _is_missingno_info(next_pokemon):
                current_pokemon["Pokemon"] += next_pokemon["Pokemon"]
            pokemon = PokemonBase(**current_pokemon)
            pokemon_base.append(pokemon)
    return pokemon_base


def get_pokedex():
    pokemon_base = _get_pokemon_bases()
    pokedex_pokemon = [
        Pokemon(**pokemon_base.dict(), hex=hex(pokemon_base.index))
        for pokemon_base in pokemon_base
    ]
    return Pokedex(pokemon=pokedex_pokemon)
