from typing import Type

from pydantic import BaseModel, conint

PokemonStatsType: Type[int] = conint(gt=0, lt=264)


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
