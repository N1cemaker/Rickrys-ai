from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from engine.state import GameState


@dataclass(frozen=True)
class Action:
    action_type: str
    card_id: Optional[str] = None
    target: Optional[str] = None

    @classmethod
    def PlayCard(cls, card_id: str, target: Optional[str] = None) -> "Action":
        return cls(action_type="PlayCard", card_id=card_id, target=target)

    @classmethod
    def HeroPower(cls, target: Optional[str] = None) -> "Action":
        return cls(action_type="HeroPower", target=target)


def generate_actions(state: GameState) -> list[Action]:
    actions: list[Action] = []

    for card in state.hand:
        if card.cost <= state.mana:
            actions.append(Action.PlayCard(card_id=card.name, target=None))

    actions.append(Action.HeroPower(target=None))
    return actions
