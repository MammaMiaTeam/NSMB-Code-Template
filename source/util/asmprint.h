#pragma once


/*
	Assembly macro that allows printing

	Usage example:

	func_mla:
		mul r0, r1
		print "mul: %r0%\n"
		add r0, r2
		print "add: %r0%\n"
		bx lr
*/

#ifdef NTR_DEBUG
asm(R"(
	.macro print txt
	mov	r12, r12
	b 1f
	.word 0x6464
	.ascii "\txt"
	.byte 0
	.align 4
	1:
	.endm
)");
#else
asm(R"(
	.macro print txt
	.endm
)");
#endif
