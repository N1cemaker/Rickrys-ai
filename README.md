# Rickrys

Rickrys is a Hearthstone decision AI prototype focused on Zephrys-like recommendations.
Given a board state JSON, it generates candidate actions, scores them with simple heuristics,
and returns top recommendations with score breakdowns.

## Quickstart

Run tests:

```bash
pytest -q
```

Run CLI (human-readable):

```bash
python main.py examples/state.json
```

Run CLI with top-k:

```bash
python main.py examples/state.json --topk 5
```

Run CLI with JSON output:

```bash
python main.py examples/state.json --topk 3 --json
```

## Example CLI Output

```text
State: examples/state.json
Top 3 recommendations
------------------------------------------------------------
1. action: PlayCard(card=Wolfrider)
   score: 2.1
   breakdown: tempo=0.5, board_control=1.0, damage=0.0, mana_efficiency=0.6
   reasons:
   - spend mana efficiently (3/5)
   - develop board presence
   - playable this turn
2. action: PlayCard(card=River Crocolisk)
   score: 1.9
   breakdown: tempo=0.5, board_control=1.0, damage=0.0, mana_efficiency=0.4
   reasons:
   - spend mana efficiently (2/5)
   - develop board presence
   - playable this turn
3. action: PlayCard(card=Fireball)
   score: 1.3
   breakdown: tempo=0.5, board_control=0.0, damage=0.0, mana_efficiency=0.8
   reasons:
   - spend mana efficiently (4/5)
   - playable this turn
```
