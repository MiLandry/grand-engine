import { CARD_TYPES, playCardEffect } from '../cards.js';

const CARD_WIDTH = 120;
const CARD_HEIGHT = 180;
const HAND_Y = 450;

export class LevelScene extends Phaser.Scene {
    constructor(config) {
        super(config.key || 'LevelScene');
        this.levelConfig = config.levelConfig || {};
        this.hand = [];
        this.cardSprites = [];
        this.resources = {};
        this.resourceText = null;
        this.messageText = null;
        this.objectiveText = null;
    }

    init(data) {
        // Accept levelConfig via scene start
        this.levelConfig = data.levelConfig || this.levelConfig || {};
    }

    create() {
        // Set up resources from level config or defaults
        this.resources = { 
            money: 100, water: 0, steam: 0, energy: 0, ore: 0, crystal: 0,
            ...(this.levelConfig.resources || {})
        };

        this.dealHand();

        this.resourceText = this.add.text(20, 20, '', {
            font: '22px Arial',
            fill: '#fff'
        }).setOrigin(0, 0);

        this.updateResourceText();

        this.messageText = this.add.text(this.sys.game.config.width / 2, 100, '', {
            font: '28px Arial',
            fill: '#fff'
        }).setOrigin(0.5);

        // Show objective if present
        if (this.levelConfig.objective) {
            this.objectiveText = this.add.text(this.sys.game.config.width / 2, 60, this.levelConfig.objective, {
                font: '20px Arial',
                fill: '#ffd700'
            }).setOrigin(0.5);
        }

        this.renderHand();
    }

    updateResourceText() {
        const { money, water, steam, energy, ore, crystal } = this.resources;
        this.resourceText.setText(
            `💰 $${money}   💧 ${water}   ♨️ ${steam}   ⚡ ${energy}   ⛏️ ${ore}   💎 ${crystal}`
        );
    }

    dealHand() {
        // Use hand from config or default to all cards
        this.hand = this.levelConfig.hand ? [...this.levelConfig.hand] : [...CARD_TYPES];
    }

    renderHand() {
        this.cardSprites.forEach(sprite => sprite.destroy());
        this.cardSprites = [];

        const startX = this.sys.game.config.width / 2 - ((this.hand.length - 1) * (CARD_WIDTH + 20)) / 2;

        this.hand.forEach((card, i) => {
            const x = startX + i * (CARD_WIDTH + 20);
            const cardSprite = this.add.rectangle(x, HAND_Y, CARD_WIDTH, CARD_HEIGHT, card.color)
                .setStrokeStyle(4, 0xffffff)
                .setInteractive({ useHandCursor: true });

            const label = this.add.text(x, HAND_Y, card.name, {
                font: '18px Arial',
                fill: '#000',
                align: 'center',
                wordWrap: { width: CARD_WIDTH - 10 }
            }).setOrigin(0.5);

            cardSprite.on('pointerdown', () => this.playCard(i));

            this.cardSprites.push(cardSprite, label);
        });
    }

    playCard(cardIndex) {
        const card = this.hand[cardIndex];
        const { played, message, removeFromHand = true } = playCardEffect(
            card,
            this.resources,
            () => this.dealHand()
        );
        this.messageText.setText(message);
        if (played) {
            if (removeFromHand) {
                this.hand.splice(cardIndex, 1);
            }
            this.updateResourceText();
            this.renderHand();
            this.checkObjective();
        }
    }

    checkObjective() {
        // Example: check for win condition from levelConfig
        if (typeof this.levelConfig.winCondition === 'function') {
            if (this.levelConfig.winCondition(this.resources)) {
                this.messageText.setText('🎉 Objective Complete!');
            }
        }
    }
}
