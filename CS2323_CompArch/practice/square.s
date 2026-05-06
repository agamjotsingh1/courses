.text

addi x5, x5, 1
addi x6, x6, 1 # counter

square:
    addi x6, x6, 1
    slli x7, x6, 1
    addi x7, x7, -1 
    add x5, x5, x7
    jal x0, square