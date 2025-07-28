# Video Game Prototype

A Python3-based video game prototype using pygame and Jupyter notebooks for rapid development and experimentation.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the basic game:
```bash
source venv/bin/activate && python3 src/web_server.py
```

3. Start Jupyter for prototyping:
```bash
jupyter notebook notebooks/
```

## Project Structure

```
grand-engine/
├── src/game/           # Core game modules
│   ├── engine.py       # Main game engine
│   └── __init__.py
├── notebooks/          # Jupyter notebooks for prototyping
│   └── game_prototype.ipynb
├── assets/            # Game assets
│   ├── images/
│   └── sounds/
├── tests/             # Unit tests
├── main.py            # Entry point
└── requirements.txt   # Dependencies
```

## Development

Use the Jupyter notebook in `notebooks/game_prototype.ipynb` to experiment with game mechanics, physics, and features before implementing them in the main codebase.