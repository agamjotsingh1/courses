from util import pyhw

def hw_fir_symmetric(sig, coeffs):
    num_taps = len(coeffs)
    half_taps = num_taps // 2
    
    padded_sig = list(sig) + [0] * (num_taps - 1)
    
    out_sig = []
    x = [0] * num_taps
    
    for data_in in padded_sig:
        for i in range(num_taps - 1, 0, -1):
            x[i] = x[i-1]
        x[0] = data_in
        
        accum = 0
        
        for count in range(half_taps):
            symmetric_sum = pyhw.fp_add(x[count], x[num_taps - count - 1])
            prod = pyhw.fp_mul(symmetric_sum, coeffs[count])
            accum = pyhw.fp_add(prod, accum)
            
        out_sig.append(accum)
        
    return out_sig