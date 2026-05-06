.data

.word 5
.word 4, 0x3f800000, 0
.word 4, 0x3f000000, -1
.word 4, 0x00000000, 10
.word 4, 0xbf800000, 10
.word 4, 0x40400000, 30

.text

lui x3, 0x10000 
lw s0, 0(x3) # Number of inputs
addi s1, x3, 4 # Mem Location for reading values
addi s2, x3, 512 # Mem Location for storing values

main:
    bge x0, s0, exit # if s0 <= 0, exit

    lw s3, 0(s1) # function code
    flw fa0, 4(s1) # function input (x)
    lw a0, 8(s1) # number of terms

    # Switch case, s3 := code
    case1:
        bne s3, x0, case2
        jal x1, exp # code 0 for exp

    case2:
        addi s3, s3, -1
        bne s3, x0, case3 
        jal x1, sin # code 1 for sin
    
    case3:
        addi s3, s3, -1
        bne s3, x0, case4
        jal x1, cos # code 2 for cos

    case4:
        addi s3, s3, -1
        bne s3, x0, case5
        jal x1, ln # code 3 for ln

    case5:
        addi s3, s3, -1
        bne s3, x0, default
        jal x1, reciprocal # code 4 for 1/x
    
    default:
        # 'if any of the previous cases
        # are satsfied then store
        bge x0, s3, store
        jal x1, nan_error # error, code not valid

    store:
        fsw fa0, 0(s2)
    
    addi s2, s2, 4
    addi s1, s1, 12
    addi s0, s0, -1
    beq x0, x0, main

exit:
    jal x0, exit

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
# fa0 := fa0 ^ a0 (FP32)
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
# a0 := number of terms (INT32)
# OUTPUTS
# fa0 := exp(fa0) till a0 terms (FP32)
exp:
    # --- ERROR HANDLING ---
    bge x0, a0, nan_error # no of terms <= 0 then error

    # --- SAVING SAVED REGISTERS ---
    # saved registers used := s0, fs0, fs1
    # sp is pulled down by 32 bits as 
    # stack is aligned by 16 bits by default
    addi sp, sp, -32
    sd s0, 8(sp)
    fsw fs1, 4(sp)
    fsw fs0, 0(sp)

    li s0, 1 # upward counter for 'n' in taylor series
    fcvt.s.l fs0, s0 # fs0 := result (first term = 1)

    # decrease a0 by 1 as we already considered first term
    addi a0, a0, -1 

    exp_loop:
        bge x0, a0, exp_ret

        # --- SAVING ARGUMENT REGISTERS ---
        # argument registers := fa0, a0
        # return address := x1
        addi sp, sp, -32
        fsw fa0, 16(sp)
        sd a0, 8(sp)
        sd x1, 0(sp)

        # --- CALCULATING FACTORIAL ---
        # a0 = s0
        # Stored in a0
        mv a0, s0
        jal x1, fact
        fcvt.s.l fs1, a0 # fs1 contains factorial


        # --- CALCULATING POWER ---
        # Stored in fa0
        mv a0, s0
        # Input is already in fa0
        jal x1, pow
        fdiv.s fa0, fa0, fs1

        fadd.s fs0, fs0, fa0 # Adding term to result

        # --- LOADING BACK ARGUMENT REGISTERS ---
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

        # --- LOADING BACK SAVED REGISTERS ---
        flw fs0, 0(sp)
        flw fs1, 4(sp)
        ld s0, 8(sp)
        addi sp, sp, 32
        ret

    
# cos(fa0, a0)
# INPUTS
# fa0 := input (FP32)
# a0 := number of terms (INT32)
# OUTPUTS
# fa0 := cos(fa0) till a0 terms (FP32)
cos:
    # --- ERROR HANDLING ---
    bge x0, a0, nan_error # no of terms <= 0 then error


    # --- SAVING SAVED REGISTERS ---
    # saved registers used := s0, s1, fs0, fs1
    # sp is pulled down by 32 bits as 
    # stack is aligned by 16 bits by default
    addi sp, sp, -32
    sd s1, 16(sp)
    sd s0, 8(sp)
    fsw fs1, 4(sp)
    fsw fs0, 0(sp)

    # starts with 2 as first term is already considered
    li s0, 2 # upward counter for '2*n' in taylor series

    # cosine has alternating -1 and 1
    # it is just convenient to have a register for it
    li s1, 1 
    fcvt.s.l fs0, s1 # fs0 := result (first term = 1)

    # decrease a0 by 1 as we already considered first term
    addi a0, a0, -1 

    cos_loop:
        bge x0, a0, cos_ret

        # --- SAVING ARGUMENT REGISTERS ---
        # argument registers := fa0, a0
        # return address := x1
        addi sp, sp, -32
        fsw fa0, 16(sp)
        sd a0, 8(sp)
        sd x1, 0(sp)

        # --- CALCULATING FACTORIAL ---
        # a0 = s0
        # fact(s0) stored in a0
        mv a0, s0
        jal x1, fact
        fcvt.s.l fs1, a0 # fs1 contains factorial


        # --- CALCULATING POWER ---
        # pow(fa0, s0) stored in fa0
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

        # --- LOADING BACK ARGUMENT REGISTERS ---
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

        # --- LOADING BACK SAVED REGISTERS ---
        flw fs0, 0(sp)
        flw fs1, 4(sp)
        ld s0, 8(sp)
        ld s1, 16(sp)
        addi sp, sp, 32

        ret

# sin(fa0, a0)
# INPUTS
# fa0 := input (FP32)
# a0 := number of terms (INT32)
# OUTPUTS
# fa0 := sin(fa0) till a0 terms (FP32)
sin:
    # --- ERROR HANDLING ---
    bge x0, a0, nan_error # no of terms <= 0 then error

    # --- SAVING SAVED REGISTERS ---
    # saved registers used := s0, s1, fs0, fs1
    # sp is pulled down by 32 bits as 
    # stack is aligned by 16 bits by default
    addi sp, sp, -32
    sd s1, 16(sp)
    sd s0, 8(sp)
    fsw fs1, 4(sp)
    fsw fs0, 0(sp)

    # starts from 3 as first term is considered already
    li s0, 3 # upward counter for '2*n + 1' in taylor series

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

        # --- SAVING ARGUMENT REGISTERS ---
        # argument registers := fa0, a0
        # return address := x1
        addi sp, sp, -32
        fsw fa0, 16(sp)
        sd a0, 8(sp)
        sd x1, 0(sp)

        # --- CALCULATING FACTORIAL ---
        # a0 = s0
        # fact(s0) stored in a0
        mv a0, s0
        jal x1, fact
        fcvt.s.l fs1, a0 # fs1 contains factorial (in float)

        # --- CALCULATING POWER ---
        # pow(fa0, s0) stored in fa0
        mv a0, s0
        # Input is already in fa0
        jal x1, pow
        fdiv.s fa0, fa0, fs1

        # switching the sign of s1
        # -2 = 0b11111.....1110
        # xor with -2 makes it switch from 1 to -1 and -1 to 1
        xori s1, s1, -2
        fcvt.s.w ft0, s1
        fmul.s fa0, fa0, ft0 # multiplying by sign term
        fadd.s fs0, fs0, fa0 # adding the term to result

        # --- LOADING BACK ARGUMENT REGISTERS ---
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

        # --- LOADING BACK SAVED REGISTERS ---
        flw fs0, 0(sp)
        flw fs1, 4(sp)
        ld s0, 8(sp)
        ld s1, 16(sp)
        addi sp, sp, 32

        ret

# ln(fa0, a0)
# INPUTS
# fa0 := input (FP32)
# a0 := number of terms (INT32)
# OUTPUTS
# fa0 := ln(fa0) till a0 terms (FP32)
ln:
    # --- ERROR HANDLING ---
    bge x0, a0, nan_error # no of terms <= 0 then error
    fcvt.s.w ft0, x0
    fle.s t0, fa0, ft0 # domain of input is > 0
    bne t0, x0, nan_error

    # --- SAVING SAVED REGISTERS ---
    # saved registers used := s0, s1, fs0, fs1
    # sp is pulled down by 32 bits as 
    # stack is aligned by 16 bits by default
    addi sp, sp, -32
    sd s1, 12(sp)
    sd s0, 4(sp)
    fsw fs0, 0(sp)

    # NOTE := we have taylor series for only ln(1 + x)
    # so we substitute x = <input> - 1 to get ln(<input>)
    li t0, -1
    fcvt.s.w ft1, t0 # ft1 contains -1
    fadd.s fa0, fa0, ft1

    # starts with 2 as first term is already considered
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

        
        addi sp, sp, -32
        fsw fa0, 16(sp)
        sd a0, 8(sp)
        sd x1, 0(sp)

        # --- SAVING ARGUMENT REGISTERS ---
        # argument registers := fa0, a0
        # return address := x1
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

        # --- LOADING BACK ARGUMENT REGISTERS ---
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

        # --- LOADING BACK SAVED REGISTERS ---
        flw fs0, 0(sp)
        ld s0, 4(sp)
        ld s1, 12(sp)
        addi sp, sp, 32

        ret

# reciprocal(fa0, a0)
# INPUTS
# fa0 := input (FP32)
# a0 := number of terms (INT32)
# OUTPUTS
# fa0 := 1/(fa0) till a0 terms (FP32)
reciprocal:
    # --- ERROR HANDLING ---
    bge x0, a0, nan_error # no of terms <= 0 then error
    fcvt.s.w ft0, x0
    feq.s t0, fa0, ft0 # domain of input is R - {0}
    bne t0, x0, nan_error

    # --- SAVING SAVED REGISTERS ---
    # saved registers used := s0, s1, fs0, fs1
    # sp is pulled down by 32 bits as 
    # stack is aligned by 16 bits by default
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

        # --- SAVING ARGUMENT REGISTERS ---
        # argument registers := fa0, a0
        # return address := x1
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

        # --- LOADING BACK ARGUMENT REGISTERS ---
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

        # --- LOADING BACK SAVED REGISTERS ---
        flw fs0, 0(sp)
        ld s0, 4(sp)
        addi sp, sp, 16

        ret

# returns NaN
nan_error:
    li t0, -1 # 0xffffffff = Nan in floating point
    fmv.w.x fa0, t0
    ret