#!/usr/bin/env python3

from src.game.engine import GameEngine

def main():
    game = GameEngine(title="Video Game Prototype")
    game.run()

if __name__ == "__main__":
    main()