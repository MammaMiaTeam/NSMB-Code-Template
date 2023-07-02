#include "nsmb.hpp"


/*
	Utility for faster testing which instantly boots the game into the given stage group, stage and area.

	Originally written by TheGameratorT
*/

ncp_call(0x020CC720, 1) // BootScene::onUpdate
static void replaceBootEnd() {

	static constexpr u8 Group = StageGroups::World1;
	static constexpr u8 Stage = Game::getStage(Group, 1);
	static constexpr u8 Area = 0;

	Game::loadLevel(
		SceneID::StageIntro,	// scene
		0,						// vs mode
		Group, Stage, Area,		// group (world), stage, (sub) area
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

ncp_call(0x020CC5A8, 1) // BootScene::onUpdate
static void nullifyBootTimer(u16& timer) {
	timer = 0;
}

// BootScene::onCreate
ncp_repl(0x020CCBF0, 1, "b 0x020CCD90"); // Skip BootScene creation

// StageIntroScene::onRender
ncp_repl(0x02152884, 54, "mov r0, #1\nbx lr"); // Disable stage intro rendering
// StageIntroScene::onUpdate
ncp_repl(0x0215285C, 54, "mov r0, #0"); // Nullify stage intro duration
