#!/usr/bin/env python3
"""
Economic Management Game Prototype
A roguelite economic management game with card-based actions.
"""

import webbrowser
import tempfile
import os
from pathlib import Path

def create_game_html():
    """Create the HTML file for the economic game."""
    html_content = """<!DOCTYPE html>
<html>
<head>
    <title>Factory Empire - Economic Management Game</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0;
            padding: 20px;
            min-height: 100vh;
        }
        
        .game-container {
            max-width: 1200px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }
        
        .header {
            text-align: center;
            margin-bottom: 30px;
        }
        
        .header h1 {
            color: #2c3e50;
            margin: 0;
            font-size: 2.5em;
        }
        
        .resources {
            display: flex;
            justify-content: space-around;
            margin-bottom: 30px;
            flex-wrap: wrap;
        }
        
        .resource {
            background: linear-gradient(45deg, #3498db, #2980b9);
            color: white;
            padding: 15px 25px;
            border-radius: 10px;
            text-align: center;
            min-width: 120px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }
        
        .resource-value {
            font-size: 1.5em;
            font-weight: bold;
        }
        
        .hand {
            display: flex;
            justify-content: center;
            gap: 15px;
            margin-bottom: 30px;
            flex-wrap: wrap;
        }
        
        .card {
            background: linear-gradient(45deg, #e74c3c, #c0392b);
            color: white;
            padding: 20px;
            border-radius: 12px;
            min-width: 150px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 6px 20px rgba(0,0,0,0.3);
            position: relative;
            overflow: hidden;
        }
        
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.4);
        }
        
        .card:active {
            transform: translateY(0);
        }
        
        .card.disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }
        
        .card-title {
            font-size: 1.2em;
            font-weight: bold;
            margin-bottom: 10px;
        }
        
        .card-cost {
            font-size: 0.9em;
            opacity: 0.8;
        }
        
        .card-effect {
            font-size: 0.8em;
            margin-top: 8px;
        }
        
        .game-info {
            text-align: center;
            margin-bottom: 20px;
        }
        
        .turn-info {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        
        .log {
            background: #2c3e50;
            color: #ecf0f1;
            padding: 15px;
            border-radius: 10px;
            max-height: 200px;
            overflow-y: auto;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
        }
        
        .log-entry {
            margin: 5px 0;
            padding: 5px;
            border-left: 3px solid #3498db;
        }
        
        .win-screen, .lose-screen {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.8);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 1000;
        }
        
        .win-screen .content, .lose-screen .content {
            background: white;
            padding: 40px;
            border-radius: 15px;
            text-align: center;
        }
        
        .btn {
            background: linear-gradient(45deg, #27ae60, #2ecc71);
            color: white;
            border: none;
            padding: 12px 25px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 1em;
            transition: all 0.3s ease;
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        }
    </style>
</head>
<body>
    <div class="game-container">
        <div class="header">
            <h1>🏭 Factory Empire</h1>
        </div>
        
        <div class="resources">
            <div class="resource">
                <div>💰 Money</div>
                <div class="resource-value" id="money">100</div>
            </div>
            <div class="resource">
                <div>📦 Materials</div>
                <div class="resource-value" id="materials">0</div>
            </div>
            <div class="resource">
                <div>🏭 Goods</div>
                <div class="resource-value" id="goods">0</div>
            </div>
            <div class="resource">
                <div>👥 Workers</div>
                <div class="resource-value" id="workers">2</div>
            </div>
        </div>
        
        <div class="game-info">
            <div class="turn-info">
                <strong>Turn:</strong> <span id="turn">1</span> | 
                <strong>Cards in Hand:</strong> <span id="cards-in-hand">4</span>
            </div>
        </div>
        
        <div class="hand" id="hand">
            <!-- Cards will be generated here -->
        </div>
        
        <div class="log" id="log">
            <div class="log-entry">Welcome to Factory Empire! Manage your resources wisely.</div>
        </div>
    </div>
    
    <script>
        class EconomicGame {
            constructor() {
                this.resources = {
                    money: 100,
                    materials: 0,
                    goods: 0,
                    workers: 2
                };
                
                this.turn = 1;
                this.hand = [];
                this.deck = [];
                this.discard = [];
                
                this.cardDefinitions = {
                    buyMaterials: {
                        title: "Buy Materials",
                        cost: 20,
                        effect: "Gain 3 materials",
                        action: () => {
                            if (this.resources.money >= 20) {
                                this.resources.money -= 20;
                                this.resources.materials += 3;
                                this.log("Bought materials for $20");
                                return true;
                            }
                            return false;
                        }
                    },
                    produceGoods: {
                        title: "Produce Goods",
                        cost: 0,
                        effect: "Convert 2 materials to 1 good",
                        action: () => {
                            if (this.resources.materials >= 2) {
                                this.resources.materials -= 2;
                                this.resources.goods += 1;
                                this.log("Produced 1 good from 2 materials");
                                return true;
                            }
                            return false;
                        }
                    },
                    sellGoods: {
                        title: "Sell Goods",
                        cost: 0,
                        effect: "Sell 1 good for $30",
                        action: () => {
                            if (this.resources.goods >= 1) {
                                this.resources.goods -= 1;
                                this.resources.money += 30;
                                this.log("Sold 1 good for $30");
                                return true;
                            }
                            return false;
                        }
                    },
                    hireWorker: {
                        title: "Hire Worker",
                        cost: 50,
                        effect: "Gain 1 worker",
                        action: () => {
                            if (this.resources.money >= 50) {
                                this.resources.money -= 50;
                                this.resources.workers += 1;
                                this.log("Hired a new worker for $50");
                                return true;
                            }
                            return false;
                        }
                    },
                    refresh: {
                        title: "Refresh",
                        cost: 0,
                        effect: "Redraw your hand",
                        action: () => {
                            this.refreshHand();
                            this.log("Refreshed your hand");
                            return true;
                        }
                    }
                };
                
                this.initializeDeck();
                this.drawHand();
                this.updateDisplay();
            }
            
            initializeDeck() {
                this.deck = [];
                // Add cards to deck
                for (let i = 0; i < 3; i++) this.deck.push('buyMaterials');
                for (let i = 0; i < 3; i++) this.deck.push('produceGoods');
                for (let i = 0; i < 3; i++) this.deck.push('sellGoods');
                for (let i = 0; i < 2; i++) this.deck.push('hireWorker');
                for (let i = 0; i < 2; i++) this.deck.push('refresh');
                
                this.shuffleDeck();
            }
            
            shuffleDeck() {
                for (let i = this.deck.length - 1; i > 0; i--) {
                    const j = Math.floor(Math.random() * (i + 1));
                    [this.deck[i], this.deck[j]] = [this.deck[j], this.deck[i]];
                }
            }
            
            drawHand() {
                this.hand = [];
                for (let i = 0; i < 4; i++) {
                    if (this.deck.length > 0) {
                        this.hand.push(this.deck.pop());
                    } else if (this.discard.length > 0) {
                        this.shuffleDiscardIntoDeck();
                        if (this.deck.length > 0) {
                            this.hand.push(this.deck.pop());
                        }
                    }
                }
            }
            
            shuffleDiscardIntoDeck() {
                this.deck = [...this.discard];
                this.discard = [];
                this.shuffleDeck();
            }
            
            refreshHand() {
                // Move hand to discard
                this.discard.push(...this.hand);
                this.hand = [];
                this.drawHand();
            }
            
            playCard(cardIndex) {
                if (cardIndex >= 0 && cardIndex < this.hand.length) {
                    const cardId = this.hand[cardIndex];
                    const card = this.cardDefinitions[cardId];
                    
                    if (card.action()) {
                        // Remove card from hand and add to discard
                        this.discard.push(this.hand.splice(cardIndex, 1)[0]);
                        
                        // Check win/lose conditions
                        this.checkGameEnd();
                        
                        this.updateDisplay();
                    } else {
                        this.log("Cannot play this card - insufficient resources!");
                    }
                }
            }
            
            checkGameEnd() {
                if (this.resources.money >= 300) {
                    this.showWinScreen();
                } else if (this.resources.money <= 0 && this.hand.length === 0) {
                    this.showLoseScreen();
                }
            }
            
            showWinScreen() {
                const winScreen = document.createElement('div');
                winScreen.className = 'win-screen';
                winScreen.innerHTML = `
                    <div class="content">
                        <h2>🎉 Victory!</h2>
                        <p>You've built a successful factory empire!</p>
                        <p>Final Money: $${this.resources.money}</p>
                        <button class="btn" onclick="location.reload()">Play Again</button>
                    </div>
                `;
                document.body.appendChild(winScreen);
            }
            
            showLoseScreen() {
                const loseScreen = document.createElement('div');
                loseScreen.className = 'lose-screen';
                loseScreen.innerHTML = `
                    <div class="content">
                        <h2>💸 Bankruptcy!</h2>
                        <p>Your factory empire has failed.</p>
                        <button class="btn" onclick="location.reload()">Try Again</button>
                    </div>
                `;
                document.body.appendChild(loseScreen);
            }
            
            log(message) {
                const logElement = document.getElementById('log');
                const entry = document.createElement('div');
                entry.className = 'log-entry';
                entry.textContent = `Turn ${this.turn}: ${message}`;
                logElement.appendChild(entry);
                logElement.scrollTop = logElement.scrollHeight;
            }
            
            updateDisplay() {
                // Update resources
                document.getElementById('money').textContent = this.resources.money;
                document.getElementById('materials').textContent = this.resources.materials;
                document.getElementById('goods').textContent = this.resources.goods;
                document.getElementById('workers').textContent = this.resources.workers;
                
                // Update turn info
                document.getElementById('turn').textContent = this.turn;
                document.getElementById('cards-in-hand').textContent = this.hand.length;
                
                // Update hand
                const handElement = document.getElementById('hand');
                handElement.innerHTML = '';
                
                this.hand.forEach((cardId, index) => {
                    const card = this.cardDefinitions[cardId];
                    const cardElement = document.createElement('div');
                    cardElement.className = 'card';
                    cardElement.innerHTML = `
                        <div class="card-title">${card.title}</div>
                        <div class="card-cost">Cost: $${card.cost}</div>
                        <div class="card-effect">${card.effect}</div>
                    `;
                    
                    // Check if card can be played
                    const canPlay = this.canPlayCard(cardId);
                    if (!canPlay) {
                        cardElement.classList.add('disabled');
                    }
                    
                    cardElement.onclick = () => {
                        if (canPlay) {
                            this.playCard(index);
                        }
                    };
                    
                    handElement.appendChild(cardElement);
                });
            }
            
            canPlayCard(cardId) {
                const card = this.cardDefinitions[cardId];
                
                switch(cardId) {
                    case 'buyMaterials':
                        return this.resources.money >= 20;
                    case 'produceGoods':
                        return this.resources.materials >= 2;
                    case 'sellGoods':
                        return this.resources.goods >= 1;
                    case 'hireWorker':
                        return this.resources.money >= 50;
                    case 'refresh':
                        return true;
                    default:
                        return true;
                }
            }
        }
        
        // Initialize the game
        const game = new EconomicGame();
    </script>
</body>
</html>"""
    
    return html_content

def run_game():
    """Run the economic game in the default web browser."""
    html_content = create_game_html()
    
    # Create a temporary HTML file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
        f.write(html_content)
        temp_file = f.name
    
    # Open in browser
    webbrowser.open(f'file://{temp_file}')
    
    print("🎮 Factory Empire game opened in your browser!")
    print("📖 How to play:")
    print("   • Buy Materials ($20) → Gain 3 materials")
    print("   • Produce Goods (Free) → Convert 2 materials to 1 good")
    print("   • Sell Goods (Free) → Sell 1 good for $30")
    print("   • Hire Worker ($50) → Gain 1 worker")
    print("   • Refresh (Free) → Redraw your hand")
    print("\n🎯 Goal: Reach $300 to win!")
    print("💡 Strategy: Buy → Produce → Sell → Repeat!")

if __name__ == "__main__":
    run_game() 