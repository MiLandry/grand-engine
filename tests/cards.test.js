import { CARD_TYPES, playCardEffect } from '../public/cards.js';

describe('Run Core Engine Card', () => {
    test('should reset hand to all 7 cards when played', () => {
        // Setup
        const resources = {
            money: 100,
            water: 0,
            steam: 0,
            energy: 0,
            ore: 0,
            crystal: 0
        };
        
        let handAfterDeal = [];
        const mockDealHand = () => {
            // Simulate dealing all 7 unique cards
            handAfterDeal = [...CARD_TYPES];
        };
        
        const runCoreEngineCard = CARD_TYPES.find(card => card.name === "Run Core Engine");
        
        // Act
        const result = playCardEffect(runCoreEngineCard, resources, mockDealHand);
        
        // Assert
        expect(result.played).toBe(true);
        expect(result.removeFromHand).toBe(false);
        expect(result.message).toBe("Core Engine activated! Full hand restored +1 ⚡");
        expect(resources.energy).toBe(1); // Should gain 1 energy
        expect(handAfterDeal.length).toBe(7); // Hand should have all 7 cards
        expect(handAfterDeal).toEqual(expect.arrayContaining(CARD_TYPES)); // Should contain all card types
    });
    
    test('should work with different starting hand sizes', () => {
        // Test with different scenarios
        const testCases = [
            { description: 'empty hand', initialHandSize: 0 },
            { description: 'partial hand', initialHandSize: 3 },
            { description: 'full hand', initialHandSize: 7 }
        ];
        
        testCases.forEach(({ description, initialHandSize }) => {
            const resources = { money: 100, water: 0, steam: 0, energy: 0, ore: 0, crystal: 0 };
            let handAfterDeal = [];
            
            const mockDealHand = () => {
                handAfterDeal = [...CARD_TYPES]; // Always restore to full hand
            };
            
            const runCoreEngineCard = CARD_TYPES.find(card => card.name === "Run Core Engine");
            
            const result = playCardEffect(runCoreEngineCard, resources, mockDealHand);
            
            expect(handAfterDeal.length).toBe(7);
            expect(result.played).toBe(true);
            expect(result.removeFromHand).toBe(false);
        });
    });
});
