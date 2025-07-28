export const CARD_TYPES = [
    { name: "Extract Water", color: 0x4fc3f7 },
    { name: "Boil Water", color: 0xffb74d },
    { name: "Generate Energy", color: 0x81c784 },
    { name: "Mine Ore", color: 0xa1887f },
    { name: "Refine Crystals", color: 0xba68c8 },
    { name: "Sell Crystals", color: 0xff8a65 },
    { name: "Run Core Engine", color: 0xFFD700 }
];

// Handles the effect of playing a card. Returns {played, message, removeFromHand}
export function playCardEffect(card, resources, dealHandCallback) {
    let played = false;
    let message = `Played: ${card.name}`;
    let removeFromHand = true; // New flag

    switch (card.name) {
        case "Extract Water":
            resources.money -= 10;
            resources.water += 3;
            played = true;
            break;
        case "Boil Water":
            if (resources.water >= 2) {
                resources.water -= 2;
                resources.steam += 1;
                played = true;
            }
            break;
        case "Generate Energy":
            if (resources.steam >= 1) {
                resources.steam -= 1;
                resources.energy += 2;
                played = true;
            }
            break;
        case "Mine Ore":
            resources.money -= 15;
            resources.ore += 2;
            played = true;
            break;
        case "Refine Crystals":
            if (resources.ore >= 1 && resources.energy >= 1) {
                resources.ore -= 1;
                resources.energy -= 1;
                resources.crystal += 1;
                played = true;
            }
            break;
        case "Sell Crystals":
            if (resources.crystal >= 1) {
                resources.crystal -= 1;
                resources.money += 40;
                played = true;
            }
            break;
        case "Run Core Engine":
            // Reset to full hand - all 7 cards restored
            dealHandCallback(); 
            resources.energy += 1;
            message = "Core Engine activated! Full hand restored +1 ⚡";
            played = true;
            removeFromHand = false; // Don't remove Core Engine
            break;
    }

    if (!played) {
        message = `Can't play: ${card.name}`;
    }
    return { played, message, removeFromHand };
}
