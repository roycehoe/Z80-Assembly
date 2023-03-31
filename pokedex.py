import json
from pathlib import Path

from pydantic import BaseModel, Field


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


def _is_missingno_info(pokemon: dict):
    return pokemon["Index"] is None


def get_pokemon_level(level: int) -> str:
    """Obtains pokemon level in hex"""
    if level <= 100:
        return hex(level)
    raise InvalidPokemonLevel


def get_pokedex():
    path = Path("./pokedex.json")
    pokemons: list[Pokemon] = []
    with path.open("r") as file:
        pokemon_file = json.load(file)
        for i in range(0, len(pokemon_file) - 1):
            current_pokemon = pokemon_file[i]
            next_pokemon = pokemon_file[i]
            if _is_missingno_info(current_pokemon):
                continue
            if _is_missingno_info(next_pokemon):
                current_pokemon["Pokemon"] += next_pokemon["Pokemon"]
            pokemon_base = PokemonBase(**current_pokemon)
            pokemon = Pokemon(**pokemon_base.dict(), hex=hex(pokemon_base.index))
            pokemons.append(pokemon)

    return Pokedex(pokemon=pokemons)
