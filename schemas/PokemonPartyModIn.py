from typing import Literal

from pydantic import BaseModel, validator

from constants import CHAR_ENCODING
from pokedex import get_pokedex
from schemas.PokemonStats import PokemonStats

PartySlot = Literal[0, 1, 2, 3, 4, 5]
PLAYER_PARTY_MAX_POKEMON = 6


def _is_valid_pokemon_char(letter: str) -> bool:
    for key, value in CHAR_ENCODING.items():
        if letter == value:
            return True
    return False


class InvalidPokemonIndexError(Exception):
    pass


class InvalidPokemonCharacterError(Exception):
    pass


class InvalidPokemonPartySize(Exception):
    pass


class PlayerPartyMod(BaseModel):
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


class PlayerPartyModIn(BaseModel):
    data: list[PlayerPartyMod]

    @validator("data")
    def is_valid_pokemon_party_size(cls, v):
        if len(v) > PLAYER_PARTY_MAX_POKEMON:
            raise InvalidPokemonPartySize
        return v
