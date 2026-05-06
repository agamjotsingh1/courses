.data
#.word 0b00111111000000000000000000000000, 5
#.word 0b01000000011110001000001000101111, 7
#.word 0b01000000011110001000001000101111, 13
.word 0xffffffff, 32
#.word 0b00111111001100110011001100110011, -1

.text

lui x3, 0x10000 
ld t0, 0(x3)
fmv.w.x fa0, t0
ld a0, 4(x3)
jal x1, fact
add x0, x0, x0

# fact(a0)
# INPUTS
# a0 := input (INT64)
# OUTPUTS
# a0 := a0! (INT64)
fact:
    blt a0, x0, nan_error
    li t0, 1

    fact_loop:
        bge x0, a0, fact_ret
        mul t0, t0, a0 # repeatedly multiply decremented a0
        addi a0, a0, -1 # decrement a0
        jal x0, fact_loop

    fact_ret:
        mv a0, t0
        ret

# pow(fa0, a0)
# INPUTS
# fa0 := base (FP32)
# a0 := exponent (INT64)
# OUTPUTS
# fa0 := pow(fa0, a0) (FP32)
pow:
    li t0, 1
    fcvt.s.l ft0, t0 # init to 1 (in float)

    pow_loop:
        bge x0, a0, pow_ret
        fmul.s ft0, ft0, fa0 # repeatedly multiply with fa0
        addi a0, a0, -1
        jal x0, pow_loop

    pow_ret:
        fmv.w.x ft1, x0
        fadd.s fa0, ft1, ft0 # move ft0 to fa0 by adding zero
        ret

# exp(fa0, a0)
# INPUTS
# fa0 := input (FP32)
# a0 := number of terms (INT64)
# OUTPUTS
# fa0 := exp(fa0) till a0 terms (FP32)
exp:
    bge x0, a0, nan_error # no of terms <= 0 then error
    # save saved registers (s0, fs0, fs1, fs2)

    # PLEASE NOTE THIS IS NOT CONFIRMED
    # NOTE := Although we only need 16 bytes of stack
    # and the stack should be 16 bit aligned
    # the stack pointer should leave space for a red zone?
    # So, we subtract it with 32
    addi sp, sp, -32
    sd s0, 8(sp)
    fsw fs1, 4(sp)
    fsw fs0, 0(sp)

    li s0, 1 # upward counter for 'n' in taylor series
    fcvt.s.l fs0, s0 # fs0 := result

    # decrease a0 by 1 as we already considered first term
    addi a0, a0, -1 

    exp_loop:
        bge x0, a0, exp_ret

        # saving registers (fa0, a0, x1)
        addi sp, sp, -32
        fsw fa0, 16(sp)
        sd a0, 8(sp)
        sd x1, 0(sp)

        # Calculating fact(s0)
        # a0 = s0
        # Stored in a0
        mv a0, s0
        jal x1, fact
        fcvt.s.l fs1, a0 # fs1 contains factorial

        # Calculating pow(fa0, s0)
        # Stored in fa0
        mv a0, s0
        # Input is already in fa0
        jal x1, pow
        fdiv.s fa0, fa0, fs1
        fadd.s fs0, fs0, fa0

        # loading back registers (fa0, a0, x1)
        ld x1, 0(sp)
        ld a0, 8(sp)
        flw fa0, 16(sp)
        addi sp, sp, 32

        addi a0, a0, -1
        addi s0, s0, 1 # increment 'n' by one
        jal x0, exp_loop 

    exp_ret:
        fmv.w.x ft1, x0
        fadd.s fa0, ft1, fs0 # move fs0 to fa0 by adding zero

        # load back the saved registers
        flw fs0, 0(sp)
        flw fs1, 4(sp)
        ld s0, 8(sp)
        addi sp, sp, 32

        ret

    
# cos(fa0, a0)
# INPUTS
# fa0 := input (FP32)
# a0 := number of terms (INT64)
# OUTPUTS
# fa0 := cos(fa0) till a0 terms (FP32)
cos:
    bge x0, a0, nan_error # no of terms <= 0 then error

    # save saved registers (s0, s1, fs0, fs1)
    # NOTE := Although we only need 24 bytes of stack
    # memory, the stack pointer should be 16 bit aligned
    # So, we subtract it with 32
    addi sp, sp, -32
    sd s1, 16(sp)
    sd s0, 8(sp)
    fsw fs1, 4(sp)
    fsw fs0, 0(sp)

    # cosine starts with index 2
    # after the first term = 1
    li s0, 2 # upward counter for 'n' in taylor series
    # cosine has alternating -1 and 1
    # it is just convenient to have a register for it
    li s1, 1 
    fcvt.s.l fs0, s1 # fs0 := result (first term = 1)

    # decrease a0 by 1 as we already considered first term
    addi a0, a0, -1 

    cos_loop:
        bge x0, a0, cos_ret

        # saving registers (fa0, a0, x1)
        addi sp, sp, -32
        fsw fa0, 16(sp)
        sd a0, 8(sp)
        sd x1, 0(sp)

        # Calculating fact(s0)
        # a0 = s0
        # Stored in a0
        mv a0, s0
        jal x1, fact
        fcvt.s.l fs1, a0 # fs1 contains factorial

        # Calculating pow(fa0, s0)
        # Stored in fa0
        mv a0, s0
        # Input is already in fa0
        jal x1, pow
        fdiv.s fa0, fa0, fs1

        # switching the sign of s1
        # -2 = 0b11111.....1110
        # xor with -2 makes it switch from 1 to -1 and -1 to 1
        xori s1, s1, -2
        fcvt.s.w ft0, s1
        fmul.s fa0, fa0, ft0
        fadd.s fs0, fs0, fa0

        # loading back registers (fa0, a0, x1)
        ld x1, 0(sp)
        ld a0, 8(sp)
        flw fa0, 16(sp)
        addi sp, sp, 32

        addi a0, a0, -1
        # increment 'n' by 2
        # as the cos taylor series contains even powers only
        addi s0, s0, 2 
        jal x0, cos_loop 

    cos_ret:
        fmv.w.x ft1, x0
        fadd.s fa0, ft1, fs0 # move fs0 to fa0 by adding zero

        # load back the saved registers
        flw fs0, 0(sp)
        flw fs1, 4(sp)
        ld s0, 8(sp)
        ld s1, 16(sp)
        addi sp, sp, 32

        ret

# sin(fa0, a0)
# INPUTS
# fa0 := input (FP32)
# a0 := number of terms (INT64)
# OUTPUTS
# fa0 := sin(fa0) till a0 terms (FP32)
sin:
    bge x0, a0, nan_error # no of terms <= 0 then error

    # save saved registers (s0, s1, fs0, fs1)
    # NOTE := Although we only need 24 bytes of stack
    # memory, the stack pointer should be 16 bit aligned
    # So, we subtract it with 32
    addi sp, sp, -32
    sd s1, 16(sp)
    sd s0, 8(sp)
    fsw fs1, 4(sp)
    fsw fs0, 0(sp)

    # sine starts with power 1
    # but second term starts with power 3
    # as we are already considering first term
    # for initiliazation, s0 starts with 3
    li s0, 3 # upward counter for 'n' in taylor series
    # sine has alternating -1 and 1
    # it is just convenient to have a register for it
    li s1, 1 
    # fs0 := result (first term = <input> or x)
    fmv.w.x ft1, x0
    fadd.s fs0, ft1, fa0 # move fa0 to fs0 by adding zero

    # decrease a0 by 1 as we already considered first term
    addi a0, a0, -1 

    sin_loop:
        bge x0, a0, sin_ret

        # saving registers (fa0, a0, x1)
        addi sp, sp, -32
        fsw fa0, 16(sp)
        sd a0, 8(sp)
        sd x1, 0(sp)

        # Calculating fact(s0)
        # a0 = s0
        # Stored in a0
        mv a0, s0
        jal x1, fact
        fcvt.s.l fs1, a0 # fs1 contains factorial

        # Calculating pow(fa0, s0)
        # Stored in fa0
        mv a0, s0
        # Input is already in fa0
        jal x1, pow
        fdiv.s fa0, fa0, fs1

        # switching the sign of s1
        # -2 = 0b11111.....1110
        # xor with -2 makes it switch from 1 to -1 and -1 to 1
        xori s1, s1, -2
        fcvt.s.w ft0, s1
        fmul.s fa0, fa0, ft0
        fadd.s fs0, fs0, fa0

        # loading back registers (fa0, a0, x1)
        ld x1, 0(sp)
        ld a0, 8(sp)
        flw fa0, 16(sp)
        addi sp, sp, 32

        addi a0, a0, -1
        # increment 'n' by 2
        # as the sin taylor series contains odd powers only
        # (s0 started with 1)
        addi s0, s0, 2 
        jal x0, sin_loop 

    sin_ret:
        fmv.w.x ft1, x0
        fadd.s fa0, ft1, fs0 # move fs0 to fa0 by adding zero

        # load back the saved registers
        flw fs0, 0(sp)
        flw fs1, 4(sp)
        ld s0, 8(sp)
        ld s1, 16(sp)
        addi sp, sp, 32

        ret

# ln(fa0, a0)
# INPUTS
# fa0 := input (FP32)
# a0 := number of terms (INT64)
# OUTPUTS
# fa0 := ln(fa0) till a0 terms (FP32)
ln:
    bge x0, a0, nan_error # no of terms <= 0 then error
    fcvt.s.w ft0, x0
    fle.s t0, fa0, ft0 # domain of input is > 0
    bne t0, x0, nan_error

    # save saved registers (s0, s1, fs0, fs1)
    # NOTE := Although we only need 20 bytes of stack
    # memory, the stack pointer should be 16 bit aligned
    # So, we subtract it with 32
    addi sp, sp, -32
    sd s1, 12(sp)
    sd s0, 4(sp)
    fsw fs0, 0(sp)

    # NOTE := we have taylor series for only ln(1 + x)
    # so we substitute x = <input> - 1 to get ln(<input>)
    li t0, -1
    fcvt.s.w ft1, t0 # ft1 contains -1
    fadd.s fa0, fa0, ft1

    # ln starts with power 1
    # but second term starts with power 2
    # as we are already considering first term
    # for initiliazation, s0 starts with 2
    li s0, 2 # upward counter for 'n' in taylor series
    # ln has alternating -1 and 1
    # it is just convenient to have a register for it
    li s1, 1 
    # fs0 := result (first term = <input> or x)
    fmv.w.x ft1, x0
    fadd.s fs0, ft1, fa0 # move fa0 to fs0 by adding zero

    # decrease a0 by 1 as we already considered first term
    addi a0, a0, -1 

    ln_loop:
        bge x0, a0, ln_ret

        # saving registers (fa0, a0, x1)
        addi sp, sp, -32
        fsw fa0, 16(sp)
        sd a0, 8(sp)
        sd x1, 0(sp)

        # Calculating pow(fa0, s0)
        # Stored in fa0
        mv a0, s0
        # Input is already in fa0
        jal x1, pow

        # Divide by index (s0)
        fcvt.s.w ft0, s0
        fdiv.s fa0, fa0, ft0

        # switching the sign of s1
        # -2 = 0b11111.....1110
        # xor with -2 makes it switch from 1 to -1 and -1 to 1
        xori s1, s1, -2
        fcvt.s.w ft0, s1
        fmul.s fa0, fa0, ft0
        fadd.s fs0, fs0, fa0

        # loading back registers (fa0, a0, x1)
        ld x1, 0(sp)
        ld a0, 8(sp)
        flw fa0, 16(sp)
        addi sp, sp, 32

        addi a0, a0, -1
        # increment 'n' by 2
        # as the sin taylor series contains odd powers only
        # (s0 started with 1)
        addi s0, s0, 1
        jal x0, ln_loop 

    ln_ret:
        fmv.w.x ft1, x0
        fadd.s fa0, ft1, fs0 # move fs0 to fa0 by adding zero

        # load back the saved registers
        flw fs0, 0(sp)
        ld s0, 4(sp)
        ld s1, 12(sp)
        addi sp, sp, 32

        ret

# reciprocal(fa0, a0)
# INPUTS
# fa0 := input (FP32)
# a0 := number of terms (INT64)
# OUTPUTS
# fa0 := 1/(fa0) till a0 terms (FP32)
reciprocal:
    bge x0, a0, nan_error # no of terms <= 0 then error
    fcvt.s.w ft0, x0
    feq.s t0, fa0, ft0 # domain of input is R - {0}
    bne t0, x0, nan_error

    # save saved registers (s0, fs0)
    # NOTE := Although we only need 12 bytes of stack
    # memory, the stack pointer should be 16 byte memory aligned
    # So, we subtract it with 16
    addi sp, sp, -16
    sd s0, 4(sp)
    fsw fs0, 0(sp)

    # NOTE := we have taylor series for only 1/(1 - x)
    # so we substitute x = 1 - <input> to get 1/(<input>)
    li t0, 1
    fcvt.s.w ft1, t0 # ft1 contains -1
    fsub.s fa0, ft1, fa0

    li s0, 1 # upward counter for 'n' in taylor series
    # fs0 initialized to 1 which is first term
    fcvt.s.l fs0, s0 # fs0 := result 

    # decrease a0 by 1 as we already considered first term
    addi a0, a0, -1 

    reciprocal_loop:
        bge x0, a0, reciprocal_ret

        # saving registers (fa0, a0, x1)
        addi sp, sp, -32
        fsw fa0, 16(sp)
        sd a0, 8(sp)
        sd x1, 0(sp)

        # Calculating pow(fa0, s0)
        # Stored in fa0
        mv a0, s0
        # Input is already in fa0
        jal x1, pow
        fadd.s fs0, fs0, fa0

        # loading back registers (fa0, a0, x1)
        ld x1, 0(sp)
        ld a0, 8(sp)
        flw fa0, 16(sp)
        addi sp, sp, 32

        addi a0, a0, -1
        addi s0, s0, 1 # increment 'n' by one
        jal x0, reciprocal_loop 

    reciprocal_ret:
        fmv.w.x ft1, x0
        fadd.s fa0, ft1, fs0 # move fs0 to fa0 by adding zero

        # load back the saved registers
        flw fs0, 0(sp)
        ld s0, 4(sp)
        addi sp, sp, 16

        ret

nan_error:
    li t0, -1 # 0xffffffff = Nan in floating point
    fmv.w.x fa0, t0
    ret