from __future__ import annotations

from dataclasses import dataclass

from engine.actions import Action, generate_actions
from engine.scoring import ScoreBreakdown, score_action
from engine.state import GameState


@dataclass(frozen=True)
class Recommendation:
    action: Action
    breakdown: ScoreBreakdown

    @property
    def score(self) -> float:
        return self.breakdown.total


def recommend_top3(state: GameState, top_k: int = 3) -> list[Recommendation]:
    """Generate candidate actions, score them, and return top-k recommendations."""
    ranked: list[Recommendation] = []

    for action in generate_actions(state):
        ranked.append(Recommendation(action=action, breakdown=score_action(state, action)))

    ranked.sort(key=lambda rec: rec.score, reverse=True)
    return ranked[:top_k]
