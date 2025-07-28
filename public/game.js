import { LevelScene } from './scenes/LevelScene.js';

const firstMission = {
    resources: { money: 100, water: 0, steam: 0, energy: 0, ore: 0, crystal: 0 },
    objective: 'Reach $200 and 3 crystals',
    winCondition: (resources) => resources.money >= 200 && resources.crystal >= 3
};

const config = {
    type: Phaser.AUTO,
    width: 1200,
    height: 900,
    backgroundColor: '#333',
    scene: [new LevelScene({ key: 'LevelScene', levelConfig: firstMission })]
};

const game = new Phaser.Game(config);
