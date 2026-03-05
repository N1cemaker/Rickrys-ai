from __future__ import annotations

from dataclasses import dataclass, field

from engine.actions import Action
from engine.state import GameState


@dataclass(frozen=True)
class ScoreBreakdown:
    tempo: float
    board_control: float
    damage: float
    mana_efficiency: float
    total: float
    reasons: list[str] = field(default_factory=list)


def score_action(state: GameState, action: Action) -> ScoreBreakdown:
    tempo = 0.0
    board_control = 0.0
    damage = 0.0
    mana_efficiency = 0.0
    reasons: list[str] = []

    if action.action_type == "PlayCard" and action.card_id is not None:
        card = next((c for c in state.hand if c.name == action.card_id), None)
        if card is not None:
            mana_efficiency = card.cost / max(state.mana, 1)
            reasons.append(f"spend mana efficiently ({card.cost}/{state.mana})")

            if card.name in {"River Crocolisk", "Wolfrider", "Boulderfist Ogre"}:
                board_control = 1.0
                reasons.append("develop board presence")

            if card.name == "Fireball" and action.target == "enemy_hero":
                damage = 2.0
                reasons.append("direct damage to enemy hero")

            tempo = 0.5
            reasons.append("playable this turn")

    elif action.action_type == "HeroPower":
        mana_efficiency = 1.0
        tempo = 0.2
        reasons.append("use remaining mana with hero power")

    total = round(tempo + board_control + damage + mana_efficiency, 2)
    return ScoreBreakdown(
        tempo=round(tempo, 2),
        board_control=round(board_control, 2),
        damage=round(damage, 2),
        mana_efficiency=round(mana_efficiency, 2),
        total=total,
        reasons=reasons,
    )
