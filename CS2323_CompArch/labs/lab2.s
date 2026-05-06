.section .text
    start:
        li t0, 22222221
        li t1, 33334

        loop:
            mv a0, t0
            mv a1, t1
            jal x1, mod

            bge x0, a0, exit
            mv t0, a1
            mv t1, a0

            jal x0, loop

        exit:
            # t0 contains the final result
            addi t0, a1, 0
            jal x0, end
    
    mod:
        blt a0, a1, exit_mod
        sub a0, a0, a1
        jal x0, mod

    exit_mod:
        ret
    
    end:
        jal x0, end
