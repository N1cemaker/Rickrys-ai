import argparse
import json
from pathlib import Path

from engine.state import GameState
from recommend import recommend_top3


def _recommendation_to_dict(item) -> dict[str, object]:
    return {
        "action_type": item.action.action_type,
        "card_id": item.action.card_id,
        "target": item.action.target,
        "score": item.score,
        "breakdown": {
            "tempo": item.breakdown.tempo,
            "board_control": item.breakdown.board_control,
            "damage": item.breakdown.damage,
            "mana_efficiency": item.breakdown.mana_efficiency,
            "total": item.breakdown.total,
            "reasons": item.breakdown.reasons,
        },
    }


def _format_action(action) -> str:
    if action.action_type == "PlayCard":
        target = f", target={action.target}" if action.target else ""
        return f"PlayCard(card={action.card_id}{target})"
    target = f"(target={action.target})" if action.target else ""
    return f"{action.action_type}{target}"


def main() -> None:
    parser = argparse.ArgumentParser(description="Rickrys CLI demo")
    parser.add_argument("state", help="Path to input state.json")
    parser.add_argument("--topk", type=int, default=3, help="Number of recommendations")
    parser.add_argument("--json", action="store_true", dest="as_json", help="Print JSON output")
    args = parser.parse_args()

    state_path = Path(args.state)
    state = GameState.from_json(state_path)
    results = recommend_top3(state, top_k=max(args.topk, 1))

    if args.as_json:
        payload = [_recommendation_to_dict(item) for item in results]
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return

    print(f"State: {state_path}")
    print(f"Top {len(results)} recommendations")
    print("-" * 60)
    for idx, item in enumerate(results, start=1):
        b = item.breakdown
        print(f"{idx}. action: {_format_action(item.action)}")
        print(f"   score: {item.score}")
        print(
            "   breakdown: "
            f"tempo={b.tempo}, board_control={b.board_control}, "
            f"damage={b.damage}, mana_efficiency={b.mana_efficiency}"
        )
        if b.reasons:
            print("   reasons:")
            for reason in b.reasons:
                print(f"   - {reason}")
        else:
            print("   reasons: none")


if __name__ == "__main__":
    main()
