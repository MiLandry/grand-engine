const CARD_WIDTH = 120;
const CARD_HEIGHT = 180;
const HAND_Y = 450;

const CARD_TYPES = [
    { name: "Extract Water", color: 0x4fc3f7 },
    { name: "Boil Water", color: 0xffb74d },
    { name: "Generate Energy", color: 0x81c784 },
    { name: "Mine Ore", color: 0xa1887f },
    { name: "Refine Crystals", color: 0xba68c8 },
    { name: "Sell Crystals", color: 0xff8a65 }
];

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
        this.hand = [];
        for (let i = 0; i < 5; i++) {
            const card = Phaser.Utils.Array.GetRandom(CARD_TYPES);
            this.hand.push(card);
        }
    }

    renderHand() {
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
        this.messageText.setText(`Played: ${card.name}`);
        // Example: update resources based on card played
        if (card.name === "Extract Water") {
            this.resources.money -= 10;
            this.resources.water += 3;
        } else if (card.name === "Boil Water") {
            if (this.resources.water >= 2) {
                this.resources.water -= 2;
                this.resources.steam += 1;
            }
        } else if (card.name === "Generate Energy") {
            if (this.resources.steam >= 1) {
                this.resources.steam -= 1;
                this.resources.energy += 2;
            }
        } else if (card.name === "Mine Ore") {
            this.resources.money -= 15;
            this.resources.ore += 2;
        } else if (card.name === "Refine Crystals") {
            if (this.resources.ore >= 1 && this.resources.energy >= 1) {
                this.resources.ore -= 1;
                this.resources.energy -= 1;
                this.resources.crystal += 1;
            }
        } else if (card.name === "Sell Crystals") {
            if (this.resources.crystal >= 1) {
                this.resources.crystal -= 1;
                this.resources.money += 40;
            }
        }
        this.hand.splice(cardIndex, 1);
        this.updateResourceText();
        this.renderHand();
    }
}
