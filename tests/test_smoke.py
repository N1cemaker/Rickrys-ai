import json
from pathlib import Path

from recommend import recommend_top3


def test_recommend_top3_smoke() -> None:
    state = json.loads(Path("examples/state.json").read_text(encoding="utf-8-sig"))
    results = recommend_top3(state)

    assert len(results) == 3
    assert results[0]["score"] >= results[1]["score"] >= results[2]["score"]
    assert all("card" in item and "score" in item and "explanation" in item for item in results)

