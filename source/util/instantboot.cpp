#include "nsmb.h"


// Instantly boots the game into the StageScene at given stage group, stage and area
// Originally written by TheGameratorT

rlnk(0x020CC720, 1) // BootScene::onUpdate
static void replaceBootEnd() {

	static constexpr u8 group = StageGroups::World1;
	static constexpr u8 stage = Game::getStage(group, 1);
	static constexpr u8 area = 0;

	Game::loadLevel(
		SceneID::StageIntro,	// scene
		0,						// vs mode
		group, stage, area,		// group (world), stage, (sub) area
		0, 1,					// player ID, player mask
		0, 0,					// character 1, character 2
		1,						// powerup
		-1,						// entrance
		1, 						// flag
		1, 						// <unused>
		-1,						// control mode
		1, 						// <unused>
		0, 						// challenge mode
		-1						// rng seed
	);
}

rlnk(0x020CC5A8, 1) // BootScene::onUpdate
static void nullifyBootTimer(u16& timer) {
	timer = 0;
}

// BootScene::onCreate
over_asm(0x020CCBF0, 1, "b 0x020CCD90"); // Skip BootScene creation

// StageIntroScene::onRender
over_asm(0x02152884, 54, "mov r0, #1\nbx lr"); // Disable stage intro rendering
// StageIntroScene::onUpdate
over_asm(0x0215285C, 54, "mov r0, #0"); // Nullify stage intro duration
