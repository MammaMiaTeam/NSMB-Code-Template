#include "nsmb.h"


// Replaces the Stage::collectCoin function to change the player's runtimePowerup to PowerupState::Mini once a coin is collected

rlnk(0x02020354)
void replaceCollectCoin(u8 playerID) {
	
	Player& player = *Game::getPlayer(playerID);

	player.runtimePowerup = PowerupState::Mini;
}

// Hooks into Goomba::updateBahp to set his velocity.y to 8.0fx instead of the function argument

hook(0x020E2408, 10)
asm_func void higherGoombaBahp() {asm(R"(
	ldr		r1, =0x8000
	cmp		r2, #0				@ Replaced instruction
	b		0x020E2408 + 4		@ Branch back
)");}

// Nullifies a str instruction in StageScene::mainUpdateState to not decrease the timer

over_asm(0x020A2768, 0, "nop")

// Replaces the Stage::brickSpawnItems table to change which items will come out of brick blocks

over(0x020C20F0, 0) const SpawnItem brickSpawnItems[16] = {
	SpawnItem::None,
	SpawnItem::Star,
	SpawnItem::Star,
	SpawnItem::OneUp,
	SpawnItem::Star,
	SpawnItem::MultiCoin,
	SpawnItem::Vine,
	SpawnItem::TNone,
	SpawnItem::None,
	SpawnItem::None,
	SpawnItem::None,
	SpawnItem::None,
	SpawnItem::None,
	SpawnItem::None,
	SpawnItem::None,
	SpawnItem::None
};
