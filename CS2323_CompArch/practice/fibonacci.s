.text

addi x5, x5, 1
addi x6, x6, 1

fibonacci:
    add x7, x5, x6
    addi x5, x6, 0
    addi x6, x7, 0
    jal x0, fibonacci
exit: