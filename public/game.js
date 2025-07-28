import { MainScene } from './scenes/MainScene.js';

const config = {
    type: Phaser.AUTO,
    width: 1200,      // Increased width
    height: 900,      // Increased height
    backgroundColor: '#333',
    scene: MainScene
};

const game = new Phaser.Game(config);
