#pragma once


// Assembly macro that allows printing
// Usage example:
// print "test %r0% %r1%\n"

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
