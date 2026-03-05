from __future__ import annotations

from engine.actions import Action, generate_actions
from engine.scoring import score_action
from engine.state import GameState


def _action_label(action: Action) -> str:
    if action.action_type == "PlayCard":
        return f"PlayCard({action.card_id})"
    return "HeroPower"


def recommend_top3(state: GameState, top_k: int = 3) -> list[dict[str, object]]:
    """Generate candidate actions, score them, and return top-k results."""
    ranked: list[dict[str, object]] = []

    for action in generate_actions(state):
        breakdown = score_action(state, action)
        ranked.append(
            {
                "action": _action_label(action),
                "action_type": action.action_type,
                "card_id": action.card_id,
                "target": action.target,
                "score": breakdown.total,
                "breakdown": breakdown,
                "reasons": breakdown.reasons,
            }
        )

    ranked.sort(key=lambda x: float(x["score"]), reverse=True)
    return ranked[:top_k]
