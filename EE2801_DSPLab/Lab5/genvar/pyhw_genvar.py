from util import pyhw

# sig and coeffs are in int format
def hw_fir_genvar(sig, coeffs):
    out = []
    num_taps = len(coeffs)
    x = [0] * (len(sig) + num_taps - 1) 
    sig = sig + [0] * (num_taps - 1)

    for i, s in enumerate(sig):
        x = [int(s)] + x
        mult_out = [0] * num_taps

        for i in range(num_taps):
            mult_out[i] = pyhw.fp_mul(x[i], int(coeffs[i]))
        
        add_out = mult_out[0]

        for i in range(1, num_taps):
            add_out = pyhw.fp_add(add_out, mult_out[i])

        out.append(add_out)

    return out