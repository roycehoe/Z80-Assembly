from pathlib import Path
from typing import Callable, Literal

from constants import (
    NEXT_PARTY_POKEMON_INDEX_STEP,
    NEXT_PARTY_POKEMON_NAME_STEP,
    NEXT_PARTY_POKEMON_STATS_STEP,
    SAVE_FILE_FIRST_PARTY_POKEMON_INDEX_LOCATION,
    SAVE_FILE_FIRST_PARTY_POKEMON_STATS_LOCATION,
    SAVE_FILE_FIST_PARTY_POKEMON_NAME_LOCATION,
)
from schemas.PokemonPartyModIn import PlayerPartyMod
from schemas.PokemonStats import PokemonStats
from utils.byte_processor import file_byte_iterator, get_pokemon_chars

BLANK_POKEMON_CHAR = 0x50
PartySlot = Literal[0, 1, 2, 3, 4, 5]


def _get_pokemon_name(name: str) -> list[int]:
    """Pokemon names are stored in memory within exactly 10 hexadecimals"""
    name_in_pokemon_chars = get_pokemon_chars(name)
    while len(name_in_pokemon_chars) <= 10:
        name_in_pokemon_chars.append(BLANK_POKEMON_CHAR)
    return name_in_pokemon_chars


def _get_moded_party_pokemon_index(
    save_file: list[int], party_slot: PartySlot, moded_pokemon_index: int
) -> list[int]:
    start_mem_location = SAVE_FILE_FIRST_PARTY_POKEMON_INDEX_LOCATION + (
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

    start_mem_location = SAVE_FILE_FIST_PARTY_POKEMON_NAME_LOCATION + (
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
    start_mem_location = SAVE_FILE_FIRST_PARTY_POKEMON_STATS_LOCATION + (
        NEXT_PARTY_POKEMON_STATS_STEP * party_slot
    )
    return [
        *save_file[:start_mem_location],
        *moded_stats.get_hex(),
        *save_file[NEXT_PARTY_POKEMON_STATS_STEP + start_mem_location :],
    ]


def get_moded_party(save_file: list[int], mod: PlayerPartyMod) -> list[int]:
    res = _get_moded_party_pokemon_index(save_file, mod.slot, mod.index)
    res = _get_moded_party_pokemon_name(save_file, mod.slot, mod.name)
    res = _get_moded_party_pokemon_stats(save_file, mod.slot, mod.stats)
    return res


def write_moded_party(
    save_template_location: str,
    output_location: str,
    mod: PlayerPartyMod,
    moded_party_func: Callable[
        [list[int], PlayerPartyMod], list[int]
    ] = get_moded_party,
):
    save_file = list(file_byte_iterator(save_template_location))
    moded_party = moded_party_func(save_file, mod)
    path = Path(output_location)
    with path.open("w") as file:
        ...
    return
