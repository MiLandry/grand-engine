#!/usr/bin/env python3
"""
Grand Engine Web Server
A simple Flask server to serve the economic management game.
"""

from flask import Flask, render_template_string, send_from_directory
import os
import tempfile
import webbrowser
from pathlib import Path

app = Flask(__name__)

# Game HTML template
GAME_HTML = """<!DOCTYPE html>
<html>
<head>
    <title>Grand Engine - Economic Management Game</title>
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
            <h1>⚙️ Grand Engine</h1>
        </div>
        
        <div class="resources">
            <div class="resource">
                <div>💰 Money</div>
                <div class="resource-value" id="money">100</div>
            </div>
            <div class="resource">
                <div>💧 Water</div>
                <div class="resource-value" id="water">0</div>
            </div>
            <div class="resource">
                <div>🌫️ Steam</div>
                <div class="resource-value" id="steam">0</div>
            </div>
            <div class="resource">
                <div>⚡ Energy</div>
                <div class="resource-value" id="energy">0</div>
            </div>
            <div class="resource">
                <div>⛏️ Ore</div>
                <div class="resource-value" id="ore">0</div>
            </div>
            <div class="resource">
                <div>💎 Crystals</div>
                <div class="resource-value" id="crystals">0</div>
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
            <div class="log-entry">Welcome to Grand Engine! Build your economic empire.</div>
        </div>
    </div>
    
    <script>
        class EconomicGame {
            constructor() {
                this.resources = {
                    money: 100,
                    water: 0,
                    steam: 0,
                    energy: 0,
                    ore: 0,
                    crystals: 0
                };
                
                this.turn = 1;
                this.hand = [];
                this.deck = [];
                this.discard = [];
                
                this.cardDefinitions = {
                    extractWater: {
                        title: "Extract Water",
                        cost: 10,
                        effect: "Gain 3 water",
                        action: () => {
                            if (this.resources.money >= 10) {
                                this.resources.money -= 10;
                                this.resources.water += 3;
                                this.log("Extracted 3 water for $10");
                                return true;
                            }
                            return false;
                        }
                    },
                    boilWater: {
                        title: "Boil Water",
                        cost: 0,
                        effect: "Convert 2 water to 1 steam",
                        action: () => {
                            if (this.resources.water >= 2) {
                                this.resources.water -= 2;
                                this.resources.steam += 1;
                                this.log("Boiled 2 water into 1 steam");
                                return true;
                            }
                            return false;
                        }
                    },
                    generateEnergy: {
                        title: "Generate Energy",
                        cost: 0,
                        effect: "Convert 1 steam to 2 energy",
                        action: () => {
                            if (this.resources.steam >= 1) {
                                this.resources.steam -= 1;
                                this.resources.energy += 2;
                                this.log("Generated 2 energy from 1 steam");
                                return true;
                            }
                            return false;
                        }
                    },
                    mineOre: {
                        title: "Mine Ore",
                        cost: 15,
                        effect: "Gain 2 ore",
                        action: () => {
                            if (this.resources.money >= 15) {
                                this.resources.money -= 15;
                                this.resources.ore += 2;
                                this.log("Mined 2 ore for $15");
                                return true;
                            }
                            return false;
                        }
                    },
                    refineCrystals: {
                        title: "Refine Crystals",
                        cost: 0,
                        effect: "Convert 1 ore + 1 energy to 1 crystal",
                        action: () => {
                            if (this.resources.ore >= 1 && this.resources.energy >= 1) {
                                this.resources.ore -= 1;
                                this.resources.energy -= 1;
                                this.resources.crystals += 1;
                                this.log("Refined 1 crystal from 1 ore + 1 energy");
                                return true;
                            }
                            return false;
                        }
                    },
                    sellCrystals: {
                        title: "Sell Crystals",
                        cost: 0,
                        effect: "Sell 1 crystal for $40",
                        action: () => {
                            if (this.resources.crystals >= 1) {
                                this.resources.crystals -= 1;
                                this.resources.money += 40;
                                this.log("Sold 1 crystal for $40");
                                return true;
                            }
                            return false;
                        }
                    },
                    activateEngine: {
                        title: "Activate Core Engine",
                        cost: 0,
                        effect: "Redraw hand + gain 1 energy",
                        action: () => {
                            this.refreshHand();
                            this.resources.energy += 1;
                            this.log("Core engine activated! Redrew hand and gained 1 energy");
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
                for (let i = 0; i < 3; i++) this.deck.push('extractWater');
                for (let i = 0; i < 3; i++) this.deck.push('boilWater');
                for (let i = 0; i < 3; i++) this.deck.push('generateEnergy');
                for (let i = 0; i < 2; i++) this.deck.push('mineOre');
                for (let i = 0; i < 2; i++) this.deck.push('refineCrystals');
                for (let i = 0; i < 2; i++) this.deck.push('sellCrystals');
                for (let i = 0; i < 2; i++) this.deck.push('activateEngine');
                
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
                        <p>You've built a successful economic engine!</p>
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
                        <p>Your economic engine has failed.</p>
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
                document.getElementById('water').textContent = this.resources.water;
                document.getElementById('steam').textContent = this.resources.steam;
                document.getElementById('energy').textContent = this.resources.energy;
                document.getElementById('ore').textContent = this.resources.ore;
                document.getElementById('crystals').textContent = this.resources.crystals;
                
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
                    case 'extractWater':
                        return this.resources.money >= 10;
                    case 'boilWater':
                        return this.resources.water >= 2;
                    case 'generateEnergy':
                        return this.resources.steam >= 1;
                    case 'mineOre':
                        return this.resources.money >= 15;
                    case 'refineCrystals':
                        return this.resources.ore >= 1 && this.resources.energy >= 1;
                    case 'sellCrystals':
                        return this.resources.crystals >= 1;
                    case 'activateEngine':
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

@app.route('/')
def game():
    """Serve the Grand Engine game."""
    return GAME_HTML

@app.route('/health')
def health():
    """Health check endpoint."""
    return {'status': 'healthy', 'game': 'Grand Engine'}

def run_server(host='127.0.0.1', port=5000, debug=True):
    """Run the Flask server."""
    print(f"🎮 Starting Grand Engine server at http://{host}:{port}")
    print("📖 How to play:")
    print("   • Extract Water ($10) → Gain 3 water")
    print("   • Boil Water (Free) → Convert 2 water to 1 steam")
    print("   • Generate Energy (Free) → Convert 1 steam to 2 energy")
    print("   • Mine Ore ($15) → Gain 2 ore")
    print("   • Refine Crystals (Free) → Convert 1 ore + 1 energy to 1 crystal")
    print("   • Sell Crystals (Free) → Sell 1 crystal for $40")
    print("   • Activate Core Engine (Free) → Redraw hand + gain 1 energy")
    print("\n🎯 Goal: Reach $300 to win!")
    print("💡 Strategy: Extract → Boil → Generate → Mine → Refine → Sell!")
    
    # Open browser automatically
    webbrowser.open(f'http://{host}:{port}')
    
    app.run(host=host, port=port, debug=debug)

if __name__ == '__main__':
    run_server() 