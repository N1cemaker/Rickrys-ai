# Rickrys (Hearthstone Decision AI)

Goal: Build a card recommendation engine similar to Zephrys.

Input (JSON):
- mana
- my_hand
- my_board
- enemy_board
- hero_health / armor (optional)

Output:
- top 3 recommended cards (with scores + explanations)

Roadmap:
1) MVP: heuristic scoring + rule-based features
2) ML: dataset builder + supervised model
3) Open-source + paper