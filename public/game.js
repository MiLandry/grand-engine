import { MainScene } from './scenes/MainScene.js';

const config = {
    type: Phaser.AUTO,
    width: 800,
    height: 600,
    backgroundColor: '#333',
    scene: MainScene
};

const game = new Phaser.Game(config);
