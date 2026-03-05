from __future__ import annotations

from engine.actions import generate_actions
from engine.state import GameState


def _enemy_total_health(state: GameState) -> int:
    return state.enemy_hero.health + state.enemy_hero.armor


def _my_board_attack(state: GameState) -> int:
    return sum(minion.attack for minion in state.my_board)


def _enemy_board_attack(state: GameState) -> int:
    return sum(minion.attack for minion in state.enemy_board)


def recommend_top3(state: GameState) -> list[dict[str, object]]:
    """Return top-3 card recommendations with scores and short explanations."""
    mana = state.mana
    enemy_hp = _enemy_total_health(state)
    my_attack = _my_board_attack(state)
    enemy_attack = _enemy_board_attack(state)

    actions = generate_actions(state)
    playable_cards = {
        action.card_id
        for action in actions
        if action.action_type == "PlayCard" and action.card_id is not None
    }

    recommendations: list[dict[str, object]] = []

    for card in state.hand:
        if card.name not in playable_cards:
            continue

        score = 0.0
        reasons: list[str] = []

        if card.name == "Fireball":
            score += 7.0
            reasons.append("direct damage finisher")
            if mana >= 4:
                score += 1.0
                reasons.append("playable this turn")
            if my_attack + 6 >= enemy_hp:
                score += 4.0
                reasons.append("sets up or enables lethal")

        elif card.name == "Wolfrider":
            score += 5.0
            reasons.append("charge allows immediate pressure")
            if mana >= 3:
                score += 1.0
                reasons.append("fits current mana")

        elif card.name == "River Crocolisk":
            score += 3.0
            reasons.append("solid low-cost tempo")
            if mana >= 2:
                score += 1.0
                reasons.append("easy to curve out")

        elif card.name == "Boulderfist Ogre":
            score += 4.0
            reasons.append("high raw stats")
            if mana < 6:
                score -= 1.0
                reasons.append("not playable this turn")

        else:
            score += 1.0
            reasons.append("default heuristic score")

        if enemy_attack >= 6 and card.name in {"Fireball", "Wolfrider"}:
            score += 0.5
            reasons.append("helps stabilize initiative")

        recommendations.append(
            {
                "card": card.name,
                "score": round(score, 2),
                "explanation": "; ".join(reasons),
            }
        )

    recommendations.sort(key=lambda x: float(x["score"]), reverse=True)
    return recommendations[:3]
