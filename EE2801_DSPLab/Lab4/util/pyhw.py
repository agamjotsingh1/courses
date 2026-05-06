TOTAL_NBITS = 16
FRAC_NBITS = 14
MASK = (1 << TOTAL_NBITS) - 1

def fp_mul(num1, num2):
    num1, num2 = int(num1), int(num2)
    is_neg1 = (num1 >> (TOTAL_NBITS - 1)) & 1
    is_neg2 = (num2 >> (TOTAL_NBITS - 1)) & 1
    
    abs_num1 = ((~num1) + 1) & MASK if is_neg1 else num1
    abs_num2 = ((~num2) + 1) & MASK if is_neg2 else num2
    
    res = 0
    for i in range(TOTAL_NBITS):
        if (abs_num2 >> i) & 1:
            res += (abs_num1 << i)
            
    if is_neg1 ^ is_neg2:
        if res != 0:
            res = (1 << (TOTAL_NBITS << 1)) - res
            
    return (res >> FRAC_NBITS) & MASK

def fp_add(num1, num2):
    return (int(num1) + int(num2)) & MASK

def fp_sub(num1, num2):
    return (int(num1) - int(num2)) & MASK