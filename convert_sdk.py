#!/usr/bin/env python3

# NITRO-SDK 3.0 GCC Converter
# By TheGameratorT
# 4th April 2021

import re
import glob
import sys
import distutils.dir_util

# Headers to ignore the global to local header change
libHeaders = ['stdio.h', 'stdarg.h']

print("Compiling RegEx...")

# Regular Expressions
regex_clz = re.compile(r'\s+asm\s+\{\s+clz\s+x,\s+x\}')
regex_include = re.compile(r'(#include)\s*(<)')
regex_pragma_1 = re.compile(r'(#pragma)\s*(warn_padding)')
regex_pragma_2 = re.compile(r'(#pragma)\s*(unused)')
regex_pragma_3 = re.compile(r'(#pragma)\s*(thumb)')
regex_multichar = re.compile(r"'(.{4})'")
regex_reg_bit = re.compile(r'(reg_([^\s]+))\s*((\&|\|)=)')
regex_GXWndPlane = re.compile(r'(typedef)(.|\n)*(GXWndPlane;)')
regex_DispCnt = re.compile(r'(\/\/ Display)(.|\n)*(GXSDispCnt;)')
regex_BGCnt = re.compile(r'(typedef)(.|\n)*(GXBg2ControlLargeBmp;)')

def isLibHeader(txt: str):
	for x in libHeaders:
		if x in txt:
			return True
	return False

print("Applying...")
for filename in glob.iglob('./include/**/*.h', recursive=True):

	unix_filename = filename.replace('\\', '/')
	if(
		unix_filename != './include/nitro.h' and
		unix_filename != './include/nnsys.h' and
		(not unix_filename.startswith('./include/nitro/')) and
		(not unix_filename.startswith('./include/nitro_wl/')) and
		(not unix_filename.startswith('./include/nnsys/'))
		):
		continue

	print(f'Processing {unix_filename}')

	new_lines = []

	with open(filename, 'r') as f:

		text = ''.join(f.readlines())

		if(unix_filename == './include/nitro.h'):
			# Prevent warning in comment
			text = text.replace('mi/*.h', 'mi/_.h')

		elif(unix_filename == './include/nitro/math/math.h'):
			# CodeWarrior ASM block to GCC ASM block
			text = regex_clz.sub('\n    asm("clz x, x");', text)

		elif(
			unix_filename == './include/nitro/mi/memory.h' or
			unix_filename == './include/nitro/fx/fx_mtx22.h' or
			unix_filename == './include/nitro/fx/fx_mtx33.h' or
			unix_filename == './include/nitro/fx/fx_mtx43.h' or
			unix_filename == './include/nitro/fx/fx_mtx44.h' or
			unix_filename == './include/nitro/os/ARM9/protectionRegion.h'
			):
			# Register deprecation
			text = text.replace("register ", "/*register*/ ")

		elif(unix_filename == './include/nitro/os/common/interrupt.h'):
			# Volatile registers compound assignment
			text = text.replace("|= ", "= *(vu32 *)HW_INTR_CHECK_BUF | ")
			text = text.replace("&= ", "= *(vu32 *)HW_INTR_CHECK_BUF & ")
			# Volatile return
			text = text.replace("vu32 O", "u32 O")

		elif(unix_filename == './include/nitro/os/common/spinLock.h'):
			# Volatile struct
			text = text.replace(
"""typedef volatile struct OSLockWord
{
    u32     lockFlag;
    u16     ownerID;
    u16     extension;
}
OSLockWord;""",
"""typedef struct OSLockWord
{
    volatile u32     lockFlag;
    volatile u16     ownerID;
    volatile u16     extension;
}
OSLockWord;""")

		elif(unix_filename == './include/nitro/gx/g2.h'):
			# Volatile register copy
			text = regex_GXWndPlane.sub(
"""#ifndef __cplusplus
typedef
#endif
struct
#ifdef __cplusplus
GXWndPlane
#endif
{
    u8      planeMask:5;
    u8      effect:1;
    u8      _reserve:2;
#ifdef __cplusplus
    inline GXWndPlane(volatile GXWndPlane& rhs) {
        this->planeMask = rhs.planeMask;
        this->effect = rhs.effect;
        this->_reserve = rhs._reserve;
    }
#endif
}
#ifndef __cplusplus
GXWndPlane
#endif
;""", text)

		elif(unix_filename == './include/nitro/gx/gx.h'):
			# Volatile register copy
			text = regex_DispCnt.sub(
"""#ifdef __cplusplus
#define __dispcnt_decl(x, y) union x { u32 raw; struct { y }; inline x(volatile x& rhs) { this->raw = rhs.raw; } };
#else
#define __dispcnt_decl(x, y) typedef union { u32 raw; struct { y }; } x;
#endif

// Display control register(MAIN engine).
__dispcnt_decl(GXDispCnt,
    u32     bgMode:3;
    u32     bg0_2d3d:1;
    u32     objMapChar:1;
    u32     objMapBmp:2;
    u32     blankScr:1;
    u32     visiblePlane:5;
    u32     visibleWnd:3;
    u32     dispMode:4;
    u32     extObjMapChar:2;
    u32     extObjMapBmp:1;
    u32     hBlankObjProc:1;
    u32     bgCharOffset:3;
    u32     bgScrOffset:3;
    u32     bgExtPltt:1;
    u32     objExtPltt:1;
)

// Display control register(SUB engine).
__dispcnt_decl(GXSDispCnt,
    u32     bgMode:3;
    u32     _reserve1:1;
    u32     objMapChar:1;
    u32     objMapBmp:2;
    u32     blankScr:1;
    u32     visiblePlane:5;
    u32     visibleWnd:3;
    u32     dispMode:1;
    u32     _reserve2:3;
    u32     extObjMapChar:2;
    u32     _reserve3:1;
    u32     hBlankObjProc:1;
    u32     _reserve4:6;
    u32     bgExtPltt:1;
    u32     objExtPltt:1;
)

#undef __dispcnt_decl""", text)

			# ==== Missing Parentheses ====

			# GX_SetOBJVRamModeChar
			text = text.replace(
				"""reg_GX_DISPCNT = (u32)(reg_GX_DISPCNT &
                           ~(REG_GX_DISPCNT_EXOBJ_CH_MASK | REG_GX_DISPCNT_OBJMAP_CH_MASK) | mode);""",
				"""reg_GX_DISPCNT = (u32)((reg_GX_DISPCNT &
                           ~(REG_GX_DISPCNT_EXOBJ_CH_MASK | REG_GX_DISPCNT_OBJMAP_CH_MASK)) | mode);""")

			# GXS_SetOBJVRamModeChar
			text = text.replace(
				"""reg_GXS_DB_DISPCNT = (u32)(reg_GXS_DB_DISPCNT &
                               ~(REG_GXS_DB_DISPCNT_EXOBJ_CH_MASK |
                                 REG_GXS_DB_DISPCNT_OBJMAP_CH_MASK) | mode);""",
				"""reg_GXS_DB_DISPCNT = (u32)((reg_GXS_DB_DISPCNT &
                               ~(REG_GXS_DB_DISPCNT_EXOBJ_CH_MASK |
                                 REG_GXS_DB_DISPCNT_OBJMAP_CH_MASK)) | mode);""")

			# GX_SetOBJVRamModeBmp
			text = text.replace(
				"""reg_GX_DISPCNT = (u32)(reg_GX_DISPCNT &
                           ~(REG_GX_DISPCNT_EXOBJ_BM_MASK | REG_GX_DISPCNT_OBJMAP_BM_MASK) | mode);""",
				"""reg_GX_DISPCNT = (u32)((reg_GX_DISPCNT &
                           ~(REG_GX_DISPCNT_EXOBJ_BM_MASK | REG_GX_DISPCNT_OBJMAP_BM_MASK)) | mode);""")

			# GXS_SetOBJVRamModeBmp
			text = text.replace(
				"reg_GXS_DB_DISPCNT = (u32)(reg_GXS_DB_DISPCNT & ~(REG_GXS_DB_DISPCNT_OBJMAP_BM_MASK) | mode);",
				"reg_GXS_DB_DISPCNT = (u32)((reg_GXS_DB_DISPCNT & ~(REG_GXS_DB_DISPCNT_OBJMAP_BM_MASK)) | mode);")

		elif(unix_filename == './include/nitro/gx/gx_bgcnt.h'):
			# Volatile register copy
			text = regex_BGCnt.sub(
"""#ifdef __cplusplus
#define __bgcnt_decl(x, y) union x { u16 raw; struct { y }; inline x(volatile x& rhs) { this->raw = rhs.raw; } };
#else
#define __bgcnt_decl(x, y) typedef union { u16 raw; struct { y }; } x;
#endif

__bgcnt_decl(GXBg01Control,
    u16     priority:2;
    u16     charBase:4;
    u16     mosaic:1;
    u16     colorMode:1;
    u16     screenBase:5;
    u16     bgExtPltt:1;
    u16     screenSize:2;
)

__bgcnt_decl(GXBg23ControlText,
    u16     priority:2;
    u16     charBase:4;
    u16     mosaic:1;
    u16     colorMode:1;
    u16     screenBase:5;
    u16     _reserve:1;
    u16     screenSize:2;
)

__bgcnt_decl(GXBg23ControlAffine,
    u16     priority:2;
    u16     charBase:4;
    u16     mosaic:1;
    u16     _reserve:1;
    u16     screenBase:5;
    u16     areaOver:1;
    u16     screenSize:2;
)

__bgcnt_decl(GXBg23Control256x16Pltt,
    u16     priority:2;
    u16     _reserve1:1;
    u16     charBase:3;
    u16     mosaic:1;
    u16     _reserve2:1;
    u16     screenBase:5;
    u16     areaOver:1;
    u16     screenSize:2;
)

__bgcnt_decl(GXBg23Control256Bmp,
    u16     priority:2;
    u16     _reserve1:4;
    u16     mosaic:1;
    u16     _reserve2:1;
    u16     screenBase:5;
    u16     areaOver:1;
    u16     screenSize:2;
)

__bgcnt_decl(GXBg23ControlDCBmp,
    u16     priority:2;
    u16     _reserve1:4;
    u16     mosaic:1;
    u16     _reserve2:1;
    u16     screenBase:5;
    u16     areaOver:1;
    u16     screenSize:2;
)

__bgcnt_decl(GXBg2ControlLargeBmp,
    u16     priority:2;
    u16     _reserve1:4;
    u16     mosaic:1;
    u16     _reserve2:6;
    u16     areaOver:1;
    u16     screenSize:2;
)

#undef __bgcnt_decl""", text)

		elif(unix_filename == './include/nitro/gx/g3x.h'):

			# ==== Missing Parentheses ====
			
			# G3X_AlphaTest
			text = text.replace(
				"""reg_G3X_DISP3DCNT = (u16)(reg_G3X_DISP3DCNT &
                                  ~(REG_G3X_DISP3DCNT_RO_MASK | REG_G3X_DISP3DCNT_GO_MASK) |
                                  REG_G3X_DISP3DCNT_ATE_MASK);""",
				"""reg_G3X_DISP3DCNT = (u16)((reg_G3X_DISP3DCNT &
                                  ~(REG_G3X_DISP3DCNT_RO_MASK | REG_G3X_DISP3DCNT_GO_MASK)) |
                                  REG_G3X_DISP3DCNT_ATE_MASK);""")

			# G3X_AlphaBlend
			text = text.replace(
				"""reg_G3X_DISP3DCNT = (u16)(reg_G3X_DISP3DCNT &
                                  ~(REG_G3X_DISP3DCNT_RO_MASK | REG_G3X_DISP3DCNT_GO_MASK) |
                                  REG_G3X_DISP3DCNT_ABE_MASK);""",
				"""reg_G3X_DISP3DCNT = (u16)((reg_G3X_DISP3DCNT &
                                  ~(REG_G3X_DISP3DCNT_RO_MASK | REG_G3X_DISP3DCNT_GO_MASK)) |
                                  REG_G3X_DISP3DCNT_ABE_MASK);""")

			# G3X_AntiAlias
			text = text.replace(
				"""reg_G3X_DISP3DCNT = (u16)(reg_G3X_DISP3DCNT &
                                  ~(REG_G3X_DISP3DCNT_RO_MASK | REG_G3X_DISP3DCNT_GO_MASK) |
                                  REG_G3X_DISP3DCNT_AAE_MASK);""",
				"""reg_G3X_DISP3DCNT = (u16)((reg_G3X_DISP3DCNT &
                                  ~(REG_G3X_DISP3DCNT_RO_MASK | REG_G3X_DISP3DCNT_GO_MASK)) |
                                  REG_G3X_DISP3DCNT_AAE_MASK);""")

			# G3X_AntiAlias
			text = text.replace(
				"""reg_G3X_DISP3DCNT = (u16)(reg_G3X_DISP3DCNT &
                                  ~(REG_G3X_DISP3DCNT_RO_MASK | REG_G3X_DISP3DCNT_GO_MASK) |
                                  REG_G3X_DISP3DCNT_EME_MASK);""",
				"""reg_G3X_DISP3DCNT = (u16)((reg_G3X_DISP3DCNT &
                                  ~(REG_G3X_DISP3DCNT_RO_MASK | REG_G3X_DISP3DCNT_GO_MASK)) |
                                  REG_G3X_DISP3DCNT_EME_MASK);""")

		elif(unix_filename == './include/nnsys/g2d/load/g2d_NFT_load.h'):
			# Parameter name ommited
			text = text.replace("/*pFont*/", "pFont")

		elif(unix_filename == './include/nnsys/g2d/g2d_Animation_inline.h'):
			# Defined but not used
			text = text.replace("static", "NNS_G2D_INLINE")

		# Swap SDK_CW and SDK_GCC
		text = text.replace("SDK_CW", "SDK_TMP")
		text = text.replace("SDK_GCC", "SDK_CW")
		text = text.replace("SDK_TMP", "SDK_GCC")

		# Parameter name ommited
		text = text.replace("#ifdef __SNC__", "#if defined __SNC__ || defined __GNUC__")

		for line in text.split('\n'):

			# Convert lib header path to local header path
			if isLibHeader(line):
				newLine = line
			else:
				newLine = regex_include.sub('#include "', line)
				newLine = newLine.replace('.h>', '.h"')

			# Remove unknown pragmas
			newLine = regex_pragma_1.sub('//#pragma warn_padding', newLine)
			newLine = regex_pragma_2.sub('//#pragma unused', newLine)
			newLine = regex_pragma_3.sub('//#pragma thumb', newLine)

			# Volatile registers compound assignment
			reg_match = regex_reg_bit.search(newLine)
			if reg_match:
				reg_name = reg_match.group(1)
				reg_op = reg_match.group(4)
				newLine = regex_reg_bit.sub(f"{reg_name} = {reg_name} {reg_op}", newLine)

			# Multi-character constants
			mchr_match = regex_multichar.search(newLine)
			if mchr_match:
				mchr_full = mchr_match.group(0)
				mchr_name = mchr_match.group(1)

				mchr_name_ascii = mchr_name.encode('ascii')
				mchr_value = int.from_bytes(mchr_name_ascii, sys.byteorder)
				mchr_value_hex = hex(mchr_value)

				newLine = newLine.replace(mchr_full, mchr_value_hex + ' //' + mchr_full)

			new_lines.append(newLine + '\n')

	with open(filename, 'w') as f:
		f.writelines(new_lines)
