from engine.state import GameState
from recommend import recommend_top3


def test_game_state_from_json_loads() -> None:
    state = GameState.from_json("examples/state.json")

    assert state.mana == 5
    assert len(state.my_hand) == 4
    assert state.my_hero.health == 20
    assert state.enemy_hero.armor == 0


def test_recommend_top3_smoke() -> None:
    state = GameState.from_json("examples/state.json")
    results = recommend_top3(state)

    assert len(results) == 3
    assert results[0]["score"] >= results[1]["score"] >= results[2]["score"]
    assert all("card" in item and "score" in item and "explanation" in item for item in results)
