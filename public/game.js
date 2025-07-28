const CARD_WIDTH = 120;
const CARD_HEIGHT = 180;
const HAND_Y = 450; // Moved up so cards are visible

const CARD_TYPES = [
    { name: "Extract Water", color: 0x4fc3f7 },
    { name: "Boil Water", color: 0xffb74d },
    { name: "Generate Energy", color: 0x81c784 },
    { name: "Mine Ore", color: 0xa1887f },
    { name: "Refine Crystals", color: 0xba68c8 },
    { name: "Sell Crystals", color: 0xff8a65 }
];

class MainScene extends Phaser.Scene {
    constructor() {
        super('MainScene');
        this.hand = [];
        this.cardSprites = [];
        this.messageText = null;
    }

    create() {
        this.dealHand();

        this.messageText = this.add.text(400, 100, '', {
            font: '28px Arial',
            fill: '#fff'
        }).setOrigin(0.5);

        this.renderHand();
    }

    dealHand() {
        // Draw 5 random cards
        this.hand = [];
        for (let i = 0; i < 5; i++) {
            const card = Phaser.Utils.Array.GetRandom(CARD_TYPES);
            this.hand.push(card);
        }
    }

    renderHand() {
        // Remove old sprites
        this.cardSprites.forEach(sprite => sprite.destroy());
        this.cardSprites = [];

        const startX = 400 - ((this.hand.length - 1) * (CARD_WIDTH + 20)) / 2;

        this.hand.forEach((card, i) => {
            const x = startX + i * (CARD_WIDTH + 20);
            const cardSprite = this.add.rectangle(x, HAND_Y, CARD_WIDTH, CARD_HEIGHT, card.color)
                .setStrokeStyle(4, 0xffffff)
                .setInteractive({ useHandCursor: true });

            const label = this.add.text(x, HAND_Y, card.name, {
                font: '18px Arial',
                fill: '#000', // Black text for better contrast
                align: 'center',
                wordWrap: { width: CARD_WIDTH - 10 }
            }).setOrigin(0.5);

            cardSprite.on('pointerdown', () => this.playCard(i));

            this.cardSprites.push(cardSprite, label);
        });
    }

    playCard(cardIndex) {
        const card = this.hand[cardIndex];
        this.messageText.setText(`Played: ${card.name}`);
        this.hand.splice(cardIndex, 1);
        this.renderHand();
    }
}

const config = {
    type: Phaser.AUTO,
    width: 800,
    height: 600,
    backgroundColor: '#333',
    scene: MainScene
};

const game = new Phaser.Game(config);
