from util import pyhw

def hw_fir_direct(sig, coeffs):
    num_taps = len(coeffs)
    x = [0] * num_taps
    out = []
    
    extended_sig = sig + [0] * (num_taps - 1)
    
    for data_in in extended_sig:
        for i in range(num_taps - 1, 0, -1):
            x[i] = x[i-1]
        x[0] = data_in
        
        accum = 0
        
        for count in range(num_taps):
            prod = pyhw.fp_mul(x[count], coeffs[count])
            accum = pyhw.fp_add(prod, accum)
            
        out.append(accum)
        
    return out