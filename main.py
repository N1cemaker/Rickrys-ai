import json
from pathlib import Path

from engine.state import GameState
from recommend import recommend_top3


def main() -> None:
    state_path = Path("examples/state.json")
    state = GameState.from_json(state_path)
    results = recommend_top3(state)

    for idx, item in enumerate(results, start=1):
        print(f"{idx}. {item['card']} (score={item['score']})")
        print(f"   {item['explanation']}")


if __name__ == "__main__":
    main()
