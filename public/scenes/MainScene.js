import { CARD_TYPES, playCardEffect } from '../cards.js';

const CARD_WIDTH = 120;
const CARD_HEIGHT = 180;
const HAND_Y = 450;

export class MainScene extends Phaser.Scene {
    constructor() {
        super('MainScene');
        this.hand = [];
        this.cardSprites = [];
        this.messageText = null;
        this.resources = {
            money: 100,
            water: 0,
            steam: 0,
            energy: 0,
            ore: 0,
            crystal: 0
        };
        this.resourceText = null;
    }

    create() {
        this.dealHand();

        this.resourceText = this.add.text(20, 20, '', {
            font: '22px Arial',
            fill: '#fff'
        }).setOrigin(0, 0);

        this.updateResourceText();

        this.messageText = this.add.text(400, 100, '', {
            font: '28px Arial',
            fill: '#fff'
        }).setOrigin(0.5);

        this.renderHand();
    }

    updateResourceText() {
        const { money, water, steam, energy, ore, crystal } = this.resources;
        this.resourceText.setText(
            `💰 $${money}   💧 ${water}   ♨️ ${steam}   ⚡ ${energy}   ⛏️ ${ore}   💎 ${crystal}`
        );
    }

    dealHand() {
        // Always draw all unique cards in original order (no shuffle)
        this.hand = [...CARD_TYPES];
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
        }
    }
}
