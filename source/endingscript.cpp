#include "nsmb.hpp"


/*
	Template file to allow easy ending credits script editing

	End::ScriptEntry { string, page, y position, palette, multipage flag }

	- Due to the game using the char graphic index in the string chars, you are not supposed to use any standard string literal for this purpose
	  To face this issue, the reference contains some utilities to convert strings/chars at compile time like the literal operator ""end (check nsmb/ending/mainscreen/script.h)
	  Make sure to use the wchar_t literal (L""end) instead of a normal one (""end) when using special characters
	  If a given character cannot be converted, compilation will fail (due to End::charConv being consteval)

	- The game reads the string only up to the 41th character, exceeding this limit won't cause anything bad

	- The Y Position is in pixels starting from the top
	
	- The palette is supposed to be a value of the End::ScriptEntry::Palette enum because the other values are used for the white fading

	- Strings starting with a space or with a null terminator aren't handled correctly (give it a try)

	- Multipages entries requires you to duplicate the entry for each page always with the same values
	  Make sure to set the multipage flag to false in the last entry of the sequence

	- Any entry with string == nullptr counts as script terminator (you can use the End::scriptTerminator variable)

	- A max of 128 characters can be loaded at the same time (even if not visible), terminators and spaces excluded
	  Since this code replaces the original script in the binary, a static_assert has been added to avoid overwriting other data

	- The slideshow is not synced with the bottom screen so once the game reaches the end of the script the music will fade out
	  Because of that, try to keep the pages count as close as possible to the original (36 pages) one to avoid a huge delay between the end of the script and the cutscene
*/

ncp_over(0x020EA678, 8)
static constexpr End::ScriptEntry script[] = {
	
	// Page 0
	{"abcdefg"end,				0,	75, End::ScriptEntry::Red,	false},

	// Page 1
	{"Sample text"end,			1,	75,	End::ScriptEntry::Blue,	true},	// Start multipage
	{"skull_crossbones"end,		1,	90,	End::ScriptEntry::Red,	false},

	// Page 2
	{"Sample text"end,			2,	75,	End::ScriptEntry::Blue,	false},	// End multipage
	{L"àbcdéfgß"end,			2,	90,	End::ScriptEntry::Red,	false}, // Requires wide string due to 'ß' not fitting in a standard char
	
	// Page 3
	{"skull"end,				3,	75, End::ScriptEntry::Blue,	false},

	End::ScriptTerminator, // Terminator
};

static_assert(NTR_ARRAY_SIZE(script) < 115, "Script size out of bounds");
