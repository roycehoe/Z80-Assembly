from enum import Enum, auto
from typing import Literal, Type

from pydantic import conint


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


BEFORE_PATH = "before.dump"
AFTER_PATH = "after.dump"
POKEDEX_PATH = "./pokedex.json"


DUMMY_STRING_LOCATION = 0xD2EC

NEXT_PARTY_POKEMON_INDEX_STEP = 44
NEXT_PARTY_POKEMON_STATS_STEP = 1
NEXT_PARTY_POKEMON_NAME_STEP = 10

# MEMORY
MEM_FIRST_PARTY_POKEMON_INDEX_LOCATION = 0xD164
MEM_FIST_PARTY_POKEMON_NAME_LOCATION = 0xF2B5
MEM_FIRST_PARTY_POKEMON_STATS_LOCATION = 0xF18C

# SAVE FILE

SAVE_FILE_FIRST_PARTY_POKEMON_INDEX_LOCATION = 0x2F2D
SAVE_FILE_FIST_PARTY_POKEMON_NAME_LOCATION = 0x307E
SAVE_FILE_FIRST_PARTY_POKEMON_STATS_LOCATION = 0x2F55


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
