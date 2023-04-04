from typing import Literal, Type

from pydantic import BaseModel, conint, validator

from constants import CHAR_ENCODING, PLAYER_PARTY_MAX_POKEMON
from pokedex import get_pokedex

PartySlot = Literal[0, 1, 2, 3, 4, 5]
PokemonStatsType: Type[int] = conint(gt=0, lt=264)


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
