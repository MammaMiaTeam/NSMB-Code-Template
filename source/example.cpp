#include "nsmb.hpp"


// Replaces the Stage::collectCoin function to not do anything

ncp_jump(0x02020354)
NTR_NAKED void replaceCollectCoin() {asm(R"(
	bx		lr					@ Return
)");}

// Hooks into Goomba::updateBahp to set his velocity.y to 4.0fx instead of the function argument

ncp_jump(0x020E2408, 10)
NTR_NAKED void higherGoombaBahp() {asm(R"(
	ldr		r1, =0x4000
	cmp		r2, #0				@ Replaced instruction
	b		0x020E2408 + 4		@ Branch back
)");}

// Nullifies a str instruction in StageScene::mainUpdateState to not decrease the timer

ncp_repl(0x020A2768, 0, "nop")

// Replaces the Stage::brickSpawnItems table to change which items will come out of brick blocks

ncp_over(0x020C20F0, 0)
const SpawnItem brickSpawnItems[16] = {
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
