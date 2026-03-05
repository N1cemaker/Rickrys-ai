# Rickrys

Rickrys is a Hearthstone decision engine prototype inspired by **Zephrys**.

Given a board state JSON, the system generates candidate actions, evaluates them
using heuristic scoring, and returns the top recommendations with a detailed
score breakdown.

This project demonstrates a modular AI decision pipeline for turn-based games.

---

# Features

- Typed game state representation (GameState dataclasses)
- Candidate action generation
- Heuristic scoring system
- Recommendation ranking
- CLI demo interface
- Unit tests for core modules

---

# Architecture

Rickrys follows a modular decision pipeline:

GameState  
→ Candidate Generator  
→ Scoring System  
→ Ranking Engine  
→ Top-K Recommendations

Core modules:

engine/state.py  
Defines dataclasses for GameState, Card, Minion, Hero.

engine/actions.py  
Generates candidate actions (playable cards, hero power).

engine/scoring.py  
Evaluates each action using heuristic components:

- tempo  
- board control  
- damage  
- mana efficiency

recommend/recommender.py  
Runs the decision pipeline and returns ranked recommendations.

---

# Quick Start

Run tests:

```bash
pytest -q
```

Run CLI (human-readable output):

```bash
python main.py examples/state.json
```

Run with custom top-k:

```bash
python main.py examples/state.json --topk 5
```

Run with JSON output:

```bash
python main.py examples/state.json --topk 3 --json
```

---

# Example CLI Output

```text
Top 3 recommendations
------------------------------------------------------------
1. action: PlayCard(card=Wolfrider)
   score: 2.1
   breakdown: tempo=0.5, board_control=1.0, damage=0.0, mana_efficiency=0.6
   reasons:
   - spend mana efficiently (3/5)
   - develop board presence
   - playable this turn
```

---

# Project Structure

```
Rickrys/
│
├─ engine/
│  ├─ state.py
│  ├─ actions.py
│  └─ scoring.py
│
├─ recommend/
│  └─ recommender.py
│
├─ examples/
│  └─ state.json
│
├─ tests/
│
├─ main.py
└─ README.md
```

---

# Roadmap

### Phase 1 — Engine Prototype ✅

- Typed GameState schema
- Candidate action generation
- Heuristic scoring
- Recommendation ranking
- CLI demo

### Phase 2 — Strategic Reasoning

- Threat evaluation
- Lethal detection
- Multi-step action reasoning

### Phase 3 — Evaluation System

- Benchmark dataset
- Offline evaluation metrics
- Performance analysis

### Phase 4 — ML Integration

- Data-driven scoring model
- Learning-based decision engine

---

# License

MIT