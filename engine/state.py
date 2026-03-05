from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class Card:
    name: str
    cost: int = 0


@dataclass(frozen=True)
class Minion:
    name: str
    attack: int
    health: int


@dataclass(frozen=True)
class Hero:
    health: int = 30
    armor: int = 0


@dataclass(frozen=True)
class GameState:
    mana: int
    my_hand: list[Card]
    my_board: list[Minion]
    enemy_board: list[Minion]
    my_hero: Hero
    enemy_hero: Hero

    @property
    def hand(self) -> list[Card]:
        return self.my_hand

    @classmethod
    def from_json(cls, path_or_dict: str | Path | dict[str, Any]) -> "GameState":
        if isinstance(path_or_dict, (str, Path)):
            raw = json.loads(Path(path_or_dict).read_text(encoding="utf-8-sig"))
        elif isinstance(path_or_dict, dict):
            raw = path_or_dict
        else:
            raise TypeError("path_or_dict must be a path or dict")

        if not isinstance(raw, dict):
            raise ValueError("GameState JSON must be an object")

        mana = _as_non_negative_int(raw.get("mana", 0), "mana")
        my_hand = [_parse_card(item) for item in raw.get("my_hand", [])]
        my_board = [_parse_minion(item, "my_board") for item in raw.get("my_board", [])]
        enemy_board = [_parse_minion(item, "enemy_board") for item in raw.get("enemy_board", [])]
        my_hero = _parse_hero(raw.get("my_hero", {}), "my_hero")
        enemy_hero = _parse_hero(raw.get("enemy_hero", {}), "enemy_hero")

        return cls(
            mana=mana,
            my_hand=my_hand,
            my_board=my_board,
            enemy_board=enemy_board,
            my_hero=my_hero,
            enemy_hero=enemy_hero,
        )


def _as_non_negative_int(value: Any, field_name: str) -> int:
    try:
        out = int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{field_name} must be an integer") from exc
    if out < 0:
        raise ValueError(f"{field_name} must be >= 0")
    return out


def _parse_card(item: Any) -> Card:
    if isinstance(item, str):
        name = item.strip()
        if not name:
            raise ValueError("card name cannot be empty")
        return Card(name=name)

    if not isinstance(item, dict):
        raise ValueError("card must be a string or object")

    name = str(item.get("name", "")).strip()
    if not name:
        raise ValueError("card.name is required")
    cost = _as_non_negative_int(item.get("cost", 0), f"card {name}.cost")
    return Card(name=name, cost=cost)


def _parse_minion(item: Any, field_name: str) -> Minion:
    if not isinstance(item, dict):
        raise ValueError(f"{field_name} entries must be objects")

    name = str(item.get("name", "")).strip()
    if not name:
        raise ValueError(f"{field_name}.name is required")

    attack = _as_non_negative_int(item.get("attack", 0), f"{field_name} {name}.attack")
    health = _as_non_negative_int(item.get("health", 1), f"{field_name} {name}.health")
    return Minion(name=name, attack=attack, health=health)


def _parse_hero(item: Any, field_name: str) -> Hero:
    if item is None:
        return Hero()
    if not isinstance(item, dict):
        raise ValueError(f"{field_name} must be an object")

    health = _as_non_negative_int(item.get("health", 30), f"{field_name}.health")
    armor = _as_non_negative_int(item.get("armor", 0), f"{field_name}.armor")
    return Hero(health=health, armor=armor)
