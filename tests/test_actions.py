from engine.actions import generate_actions
from engine.state import GameState


def test_generate_actions_filters_cards_above_mana() -> None:
    state = GameState.from_json("examples/state.json")
    actions = generate_actions(state)

    play_cards = [a for a in actions if a.action_type == "PlayCard"]
    card_ids = {a.card_id for a in play_cards}

    assert "Boulderfist Ogre" not in card_ids
    assert "Fireball" in card_ids


def test_generate_actions_has_at_least_one_for_example_state() -> None:
    state = GameState.from_json("examples/state.json")
    actions = generate_actions(state)

    assert len(actions) >= 1
