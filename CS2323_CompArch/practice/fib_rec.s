li a0, 6
jal ra, fibonacci
add x0, x0, x0

fibonacci:
    addi sp, sp, -32
    sd a0, 8(sp)
    sd ra, 0(sp)

    li t0, 2
    bge a0, t0, fibonacci_recursive

    addi sp, sp, 32
    jalr x0, 0(ra)

fibonacci_recursive:
    addi a0, a0, -1
    jal ra, fibonacci

    mv t0, a0
    ld a0, 8(sp)
    addi sp, sp, -16
    sd t0, 0(sp)

    addi a0, a0, -2
    jal ra, fibonacci

    ld t0, 0(sp)
    addi sp, sp, 16

    add a0, a0, t0
    ld ra, 0(sp)
    addi sp, sp, 32

    jalr x0, 0(ra)

