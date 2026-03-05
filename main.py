from pathlib import Path

from engine.state import GameState
from recommend import recommend_top3


def main() -> None:
    state_path = Path("examples/state.json")
    state = GameState.from_json(state_path)
    results = recommend_top3(state)

    for idx, item in enumerate(results, start=1):
        breakdown = item["breakdown"]
        print(f"{idx}. {item['action']} (score={item['score']})")
        print(
            "   "
            f"tempo={breakdown.tempo}, "
            f"board_control={breakdown.board_control}, "
            f"damage={breakdown.damage}, "
            f"mana_efficiency={breakdown.mana_efficiency}"
        )
        print(f"   reasons: {'; '.join(item['reasons'])}")


if __name__ == "__main__":
    main()
