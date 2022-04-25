
.global __aeabi_uldiv
.global __aeabi_uldivmod
.global __aeabi_ldiv
.global __aeabi_ldivmod

__aeabi_uldiv:
__aeabi_uldivmod:
	stmfd	sp!, { r4-r7, lr }

	@ Store numerator
	mov		r4, r0
	mov		r5, r1

	@ Store denominator
	mov		r6, r2
	mov		r7, r3

	@ Calculate division remainder
	bl		_ull_mod

	@ Load denominator
	mov		r2, r6
	mov		r3, r7

	@ Store division remainder
	mov		r6, r0
	mov		r7, r1

	@ Load numerator
	mov		r0, r4
	mov		r1, r5
	
	@ Calculate division result
	bl		_ull_div

	@ Load division remainder
	mov		r2, r6
	mov		r3, r7

	ldmia	sp!, { r4-r7, pc }

	
__aeabi_ldiv:
__aeabi_ldivmod:
	stmfd	sp!, { r4-r7, lr }

	@ Store numerator
	mov		r4, r0
	mov		r5, r1

	@ Store denominator
	mov		r6, r2
	mov		r7, r3

	@ Calculate division remainder
	bl		_ll_mod

	@ Load denominator
	mov		r2, r6
	mov		r3, r7

	@ Store division remainder
	mov		r6, r0
	mov		r7, r1

	@ Load numerator
	mov		r0, r4
	mov		r1, r5
	
	@ Calculate division result
	bl		_ll_div

	@ Load division remainder
	mov		r2, r6
	mov		r3, r7

	ldmia	sp!, { r4-r7, pc }
