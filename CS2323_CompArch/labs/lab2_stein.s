# Reference: https://en.algorithmica.org/hpc/algorithms/gcd/
# Stein's algorithm (a.k.a. Binary GCD)
.data
#.dword 3, 12, 3, 125, 50, 32, 16
.dword 1, 2273351831, 798618983

.text
# Memory location 0x10000000 for storage
lui x3, 0x10000
ld s1, 0(x3) # s1 contains number of dwords
addi s2, x3, 8 # s2 contains the current location
addi s3, x3, 512 # s3 contains the storing location

start:
    # get two numbers from s2 memory loc
    ld a0, 0(s2)
    ld a1, 8(s2)

    # compute gcd
    jal x1, gcd

    sd a0, 0(s3)

    # increment s2 by 16 to get next memory loc
    addi s2, s2, 16

    # increment s3 by 8 to get next storing memory loc
    addi s3, s3, 8
    addi s1, s1, -1 # s1 acts as a counter

    beq s1, x0, end
    jal x0, start

# Gcd procedure
gcd:
    beq a0, x0, exit_null_loop_gcd
    beq a1, x0, exit_null_loop_gcd

    # Divide both the algorithms till you get odd
    # gcd(2a, 2b) = 2*gcd(a, b)
    # Number of shifts will be stored
    # Result will be shifted back that amount of times
    loop_odd:
        or t0, a0, a1
        andi t0, t0, 1
        bne t0, x0, loop_gcd
        srli a0, a0, 1
        srli a1, a1, 1
        addi t6, t6, 1 # t6 will store number of shifts
        beq x0, x0, loop_odd

    loop_gcd:
        beq a0, x0, exit_loop_gcd # Return if a0 == 0
        bgeu a0, a1, continue

        # Swapping a0 and a1 with XOR if a0 < a1
        xor a0, a0, a1
        xor a1, a0, a1
        xor a0, a0, a1
        continue:

        sub a0, a0, a1

        # strip zeroes of a0
        # basically division by zero till
        # you get first argument odd
        # gcd(a, b) = gcd((a - b)/2, b)
        loop_strip_zeroes:
            andi t0, a0, 1
            bne t0, x0, loop_gcd
            srli a0, a0, 1

        jal x0, loop_gcd

    exit_null_loop_gcd:
        # just return zero if any input is zero
        xor a0, a0, a0
        ret

    exit_loop_gcd:
        # shift the output back
        sll a0, a1, t6 
        ret

end:
    jal x0, end