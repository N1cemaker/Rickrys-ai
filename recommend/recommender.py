from __future__ import annotations

from typing import Any


def _enemy_total_health(state: dict[str, Any]) -> int:
    return int(state.get("enemy_hero_health", 30)) + int(state.get("enemy_hero_armor", 0))


def _my_board_attack(state: dict[str, Any]) -> int:
    board = state.get("my_board", [])
    return sum(int(minion.get("attack", 0)) for minion in board)


def _enemy_board_attack(state: dict[str, Any]) -> int:
    board = state.get("enemy_board", [])
    return sum(int(minion.get("attack", 0)) for minion in board)


def recommend_top3(state: dict[str, Any]) -> list[dict[str, Any]]:
    """Return top-3 card recommendations with scores and short explanations."""
    mana = int(state.get("mana", 0))
    hand = list(state.get("my_hand", []))
    enemy_hp = _enemy_total_health(state)
    my_attack = _my_board_attack(state)
    enemy_attack = _enemy_board_attack(state)

    recommendations: list[dict[str, Any]] = []

    for card in hand:
        score = 0.0
        reasons: list[str] = []

        if card == "Fireball":
            score += 7.0
            reasons.append("direct damage finisher")
            if mana >= 4:
                score += 1.0
                reasons.append("playable this turn")
            if my_attack + 6 >= enemy_hp:
                score += 4.0
                reasons.append("sets up or enables lethal")

        elif card == "Wolfrider":
            score += 5.0
            reasons.append("charge allows immediate pressure")
            if mana >= 3:
                score += 1.0
                reasons.append("fits current mana")

        elif card == "River Crocolisk":
            score += 3.0
            reasons.append("solid low-cost tempo")
            if mana >= 2:
                score += 1.0
                reasons.append("easy to curve out")

        elif card == "Boulderfist Ogre":
            score += 4.0
            reasons.append("high raw stats")
            if mana < 6:
                score -= 1.0
                reasons.append("not playable this turn")

        else:
            score += 1.0
            reasons.append("default heuristic score")

        if enemy_attack >= 6 and card in {"Fireball", "Wolfrider"}:
            score += 0.5
            reasons.append("helps stabilize initiative")

        recommendations.append(
            {
                "card": card,
                "score": round(score, 2),
                "explanation": "; ".join(reasons),
            }
        )

    recommendations.sort(key=lambda x: x["score"], reverse=True)
    return recommendations[:3]
