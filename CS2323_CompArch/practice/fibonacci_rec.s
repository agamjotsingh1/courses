li a0, 2
jal ra, fibonacci
add x0, x0, x0

fibonacci:
    addi sp, sp, -32
    sd a0, 8(sp)
    sd ra, 0(sp)

    li t0, 2
    bge a0, t0, fibonacci_inner

    ld ra, 0(sp)
    ld a0, 8(sp)
    addi sp, sp, 32
    jalr x0, 0(ra)

fibonacci_inner:

    addi a0, a0, -1
    jal ra, fibonacci

    sd a0, 0(sp)
    ld a0, 8(sp)

    addi a0, a0, -2
    jal ra, fibonacci

    ld t0, 0(sp)

    add a0, t0, a0

    addi sp, sp, -16
    jalr x0, 0(ra)

