from engine.actions import Action
from engine.scoring import score_action
from engine.state import GameState


def test_score_action_fireball_is_deterministic() -> None:
    state = GameState.from_json("examples/state.json")
    action = Action.PlayCard(card_id="Fireball", target="enemy_hero")

    score = score_action(state, action)

    assert score.tempo == 0.5
    assert score.board_control == 0.0
    assert score.damage == 2.0
    assert score.mana_efficiency == 0.8
    assert score.total == 3.3
    assert "direct damage to enemy hero" in score.reasons


def test_score_action_hero_power_is_deterministic() -> None:
    state = GameState.from_json("examples/state.json")
    action = Action.HeroPower(target=None)

    score = score_action(state, action)

    assert score.tempo == 0.2
    assert score.board_control == 0.0
    assert score.damage == 0.0
    assert score.mana_efficiency == 1.0
    assert score.total == 1.2
