import numpy as np
import struct
import warnings
from typing import Optional

# Suppress the specific warning
warnings.filterwarnings('ignore', 'invalid value encountered in scalar add')
warnings.filterwarnings('ignore', 'invalid value encountered in scalar divide')
np.seterr(over='ignore')

def float_to_ieee(f):
    # integer containing whose value in binaru
    # is same as that of floating point in IEE754 (s)
    bits = struct.unpack('I', struct.pack('f', f))[0]
    return f"0x{bits:08x}"
    return hex(bits)

def fact(n: np.int64) -> Optional[np.int64]:
    if n < 0:
        return None
    
    result = np.int64(1)
    for i in range(int(n)):
        result = np.int64(result * np.int64(i+1))
    
    return result

def pow(base: np.float32, exponent: np.int64) -> np.float32:
    # Positive exponent case - just multiply
    result = np.float32(1.0)

    for _ in range(exponent):
        result = np.float32(result * base)

    return result

def sin(x: np.float32, n: np.int32) -> np.float32:
    if n <= 0:
        return np.float32(None) # NaN
    
    result = np.float32(0.0)
    
    # Compute each term: (-1)^n * x^(2n+1) / (2n+1)!
    for i in range(n):
        # Calculate power: x^(2n+1)
        power = pow(x, np.int64(2*i + 1))
        if(i%2 != 0): power = np.float32(power * (-1))

        # Calculate factorial: (2n+1)!
        factorial = fact(np.int64(2*i + 1))
        if(factorial == None): return np.float32(None)

        # Calculate term with alternating sign

        result = result + np.float32(power/np.float32(factorial))

    return result

def exp(x: np.float32, n: np.int32) -> np.float32:
    if n <= 0:
        return np.float32(None)  # NaN
    
    result = np.float32(0.0)
    
    # Compute each term: x^n / n!
    for i in range(n):
        # Calculate power: x^i
        power = pow(x, np.int64(i))

        # Calculate factorial: i!
        factorial = fact(np.int64(i))
        if(factorial == None): return np.float32(None)

        # Calculate term
        result = result + np.float32(power/np.float32(factorial))

    return result

def cos(x: np.float32, n: np.int32) -> np.float32:
    if n <= 0:
        return np.float32(None)  # NaN
    
    result = np.float32(0.0)
    
    # Compute each term: (-1)^n * x^(2n) / (2n)!
    for i in range(n):
        # Calculate power: x^(2n)
        power = pow(x, np.int64(2*i))
        if(i%2 != 0): power = np.float32(power * (-1))

        # Calculate factorial: (2n)!
        factorial = fact(np.int64(2*i))
        if(factorial == None): return np.float32(None)

        # Calculate term with alternating sign
        result = result + np.float32(power/np.float32(factorial))

    return result


def reciprocal(x: np.float32, n: np.int32) -> np.float32:
    if n <= 0:
        return np.float32(None)  # NaN
    
    if x == np.float32(0): # Domain check, x != 0
        return np.float32(None)
    
    result = np.float32(0.0)
    
    x = np.float32(1) - x # we will use taylor series of 1/(1-x)
    for i in range(n):
        # Calculate power: x^i
        power = pow(x, np.int64(i))
        result = result + power

    return result

def ln(x: np.float32, n: np.int32) -> np.float32:
    if n <= 0:
        return np.float32(None)  # NaN
    
    if x <= np.float32(0.0):
        return np.float32(None)  # ln undefined for x <= 0
    
    x = x - np.float32(1.0)
    result = np.float32(0.0)
    
    # Compute each term: (-1)^(n-1) * x^n / n
    for i in range(1, n + 1):  # Start from i=1 since first term is x^1/1
        # Calculate power: u^i
        power = pow(x, np.int64(i))
        if((i-1)%2 != 0): power = np.float32(power * (-1))

        # Calculate term: x^i / i
        result = result + np.float32(power/np.float32(i))

    return result

code = int(input("Enter code: "))

# exp
if(code == 0):
    test_cases = [
        [np.float32(0.0), np.int32(5)],
        [np.float32(1.0), np.int32(8)],
        [np.float32(0.5), np.int32(6)],
        [np.float32(-0.5), np.int32(7)],
        [np.float32(2.0), np.int32(15)],
    ]

    convergence_test_cases = [
        [np.float32(1.0), np.int32(1)],
        [np.float32(1.0), np.int32(3)],
        [np.float32(1.0), np.int32(5)],
        [np.float32(1.0), np.int32(10)],
        [np.float32(1.0), np.int32(15)],
    ]

    edge_test_cases = [
        [np.float32(0.0), np.int32(0)],     # Zero terms
        [np.float32(1.0), np.int32(-1)],    # Negative terms
        [np.float32(-10.0), np.int32(10)],  # Large negative input
        [np.float32(100.0), np.int32(30)],  # Very large input (overflow risk)
        [np.float32(0.0), np.int32(40)],    # Excessive terms for simple case
    ]

    print("--- EXP TEST INJECTION ---")
    print("Copy paste this into your data segment\n")
    print(f".word {len(test_cases)}")
    for testcase in test_cases:
        print(f'.word {0}, {float_to_ieee(testcase[0])}, {testcase[1]}')

    print()

    print("--- EXP TESTCASES ---")
    for testcase in test_cases:
        result = exp(*testcase)
        print(f"exp({float(testcase[0])}), {testcase[1]} terms := Taylor FP32 Value = {float_to_ieee(result)} = {result} | Function value = {np.exp(testcase[0])}")

    print()

    print("--- EXP CONVERGENCE TEST INJECTION ---")
    print("Copy paste this into your data segment\n")
    print(f".word {len(test_cases)}")
    for testcase in convergence_test_cases:
        print(f'.word {0}, {float_to_ieee(testcase[0])}, {testcase[1]}')

    print()

    print("--- EXP CONVERGENCE TESTCASES ---")
    for testcase in convergence_test_cases:
        result = exp(*testcase)
        print(f"exp({float(testcase[0])}), {testcase[1]} terms := Taylor FP32 Value = {float_to_ieee(result)} = {result} | Function value = {np.exp(testcase[0])}")

    print()

    print("--- EXP EDGE TEST INJECTION ---")
    print("Copy paste this into your data segment\n")
    print(f".word {len(test_cases)}")
    for testcase in edge_test_cases:
        print(f'.word {0}, {float_to_ieee(testcase[0])}, {testcase[1]}')

    print()

    print("--- EXP EDGE TESTCASES ---")
    for testcase in edge_test_cases:
        result = exp(*testcase)
        print(f"exp({float(testcase[0])}), {testcase[1]} terms := Taylor FP32 Value = {float_to_ieee(result)} = {result} | Function value = {np.exp(testcase[0])}")

    print()

# sin
elif code == 1:
    test_cases = [
        [np.float32(0.0), np.int32(5)],
        [np.float32(np.pi/6), np.int32(8)],  # sin(30°) = 0.5
        [np.float32(np.pi/4), np.int32(6)],  # sin(45°) = √2/2
        [np.float32(np.pi/3), np.int32(7)],  # sin(60°) = √3/2
        [np.float32(np.pi/2), np.int32(15)], # sin(90°) = 1
    ]

    convergence_test_cases = [
        [np.float32(1.0), np.int32(1)],
        [np.float32(1.0), np.int32(3)],
        [np.float32(1.0), np.int32(5)],
        [np.float32(1.0), np.int32(10)],
        [np.float32(1.0), np.int32(15)],
    ]

    edge_test_cases = [
        [np.float32(0.0), np.int32(0)],       # Zero terms
        [np.float32(1.0), np.int32(-1)],      # Negative terms
        [np.float32(-np.pi/2), np.int32(10)], # sin(-90°) = -1
        [np.float32(2*np.pi), np.int32(30)],  # sin(360°) = 0
        [np.float32(0.0), np.int32(40)],      # Excessive terms for simple case
    ]

    print("--- SIN TEST INJECTION ---")
    print("Copy paste this into your data segment\n")
    print(f".word {len(test_cases)}")
    for testcase in test_cases:
        print(f'.word {1}, {float_to_ieee(testcase[0])}, {testcase[1]}')

    print()

    print("--- SIN TESTCASES ---")
    for testcase in test_cases:
        result = sin(*testcase)
        print(f"sin({float(testcase[0])}), {testcase[1]} terms := Taylor FP32 Value = {float_to_ieee(result)} = {result} | Function value = {np.sin(testcase[0])}")

    print()

    print("--- SIN CONVERGENCE TEST INJECTION ---")
    print("Copy paste this into your data segment\n")
    print(f".word {len(test_cases)}")
    for testcase in convergence_test_cases:
        print(f'.word {1}, {float_to_ieee(testcase[0])}, {testcase[1]}')

    print()

    print("--- SIN CONVERGENCE TESTCASES ---")
    for testcase in convergence_test_cases:
        result = sin(*testcase)
        print(f"sin({float(testcase[0])}), {testcase[1]} terms := Taylor FP32 Value = {float_to_ieee(result)} = {result} | Function value = {np.sin(testcase[0])}")

    print()

    print("--- SIN EDGE TEST INJECTION ---")
    print("Copy paste this into your data segment\n")
    print(f".word {len(test_cases)}")
    for testcase in edge_test_cases:
        print(f'.word {1}, {float_to_ieee(testcase[0])}, {testcase[1]}')

    print()

    print("--- SIN EDGE TESTCASES ---")
    for testcase in edge_test_cases:
        result = sin(*testcase)
        print(f"sin({float(testcase[0])}), {testcase[1]} terms := Taylor FP32 Value = {float_to_ieee(result)} = {result} | Function value = {np.sin(testcase[0])}")

    print()

# cos
if(code == 2):
    test_cases = [
        [np.float32(0.0), np.int32(5)],
        [np.float32(np.pi/6), np.int32(8)],
        [np.float32(np.pi/4), np.int32(6)],
        [np.float32(np.pi/3), np.int32(7)],
        [np.float32(np.pi/2), np.int32(15)],
    ]

    convergence_test_cases = [
        [np.float32(1.0), np.int32(1)],
        [np.float32(1.0), np.int32(3)],
        [np.float32(1.0), np.int32(5)],
        [np.float32(1.0), np.int32(10)],
        [np.float32(1.0), np.int32(15)],
    ]

    edge_test_cases = [
        [np.float32(0.0), np.int32(0)],     # Zero terms
        [np.float32(1.0), np.int32(-1)],    # Negative terms
        [np.float32(-np.pi/2), np.int32(10)],  # Large negative input
        [np.float32(np.pi), np.int32(30)],  # Very large input (overflow risk)
        [np.float32(0.0), np.int32(40)],    # Excessive terms for simple case
    ]

    print("--- COS TEST INJECTION ---")
    print("Copy paste this into your data segment\n")
    print(f".word {len(test_cases)}")
    for testcase in test_cases:
        print(f'.word {2}, {float_to_ieee(testcase[0])}, {testcase[1]}')

    print()

    print("--- COS TESTCASES ---")
    for testcase in test_cases:
        result = cos(*testcase)
        print(f"cos({float(testcase[0])}), {testcase[1]} terms := Taylor FP32 Value = {float_to_ieee(result)} = {result} | Function value = {np.cos(testcase[0])}")

    print()

    print("--- COS CONVERGENCE TEST INJECTION ---")
    print("Copy paste this into your data segment\n")
    print(f".word {len(convergence_test_cases)}")
    for testcase in convergence_test_cases:
        print(f'.word {2}, {float_to_ieee(testcase[0])}, {testcase[1]}')

    print()

    print("--- COS CONVERGENCE TESTCASES ---")
    for testcase in convergence_test_cases:
        result = cos(*testcase)
        print(f"cos({float(testcase[0])}), {testcase[1]} terms := Taylor FP32 Value = {float_to_ieee(result)} = {result} | Function value = {np.cos(testcase[0])}")

    print()

    print("--- COS EDGE TEST INJECTION ---")
    print("Copy paste this into your data segment\n")
    print(f".word {len(edge_test_cases)}")
    for testcase in edge_test_cases:
        print(f'.word {2}, {float_to_ieee(testcase[0])}, {testcase[1]}')

    print()

    print("--- COS EDGE TESTCASES ---")
    for testcase in edge_test_cases:
        result = cos(*testcase)
        print(f"cos({float(testcase[0])}), {testcase[1]} terms := Taylor FP32 Value = {float_to_ieee(result)} = {result} | Function value = {np.cos(testcase[0])}")

    print()

# ln
if(code == 3):
    test_cases = [
        [np.float32(1.0), np.int32(5)],     # ln(1) = 0
        [np.float32(1.5), np.int32(8)],     # ln(1.5)
        [np.float32(0.5), np.int32(6)],     # ln(0.5)
        [np.float32(1.2), np.int32(7)],     # ln(1.2)
        [np.float32(0.8), np.int32(15)],    # ln(0.8)
    ]

    convergence_test_cases = [
        [np.float32(1.5), np.int32(1)],
        [np.float32(1.5), np.int32(3)],
        [np.float32(1.5), np.int32(5)],
        [np.float32(1.5), np.int32(10)],
        [np.float32(1.5), np.int32(15)],
    ]

    edge_test_cases = [
        [np.float32(1.0), np.int32(0)],     # Zero terms
        [np.float32(1.5), np.int32(-1)],    # Negative terms
        [np.float32(0.0), np.int32(10)],    # Out of domain: x = 0
        [np.float32(-1.0), np.int32(10)],   # Out of domain: x < 0
        [np.float32(3.0), np.int32(30)],    # Out of convergence range |x-1| >= 1
    ]

    print("--- LN TEST INJECTION ---")
    print("Copy paste this into your data segment\n")
    print(f".word {len(test_cases)}")
    for testcase in test_cases:
        print(f'.word {3}, {float_to_ieee(testcase[0])}, {testcase[1]}')

    print()

    print("--- LN TESTCASES ---")
    for testcase in test_cases:
        result = ln(*testcase)
        print(f"ln({float(testcase[0])}), {testcase[1]} terms := Taylor FP32 Value = {float_to_ieee(result)} = {result} | Function value = {np.log(testcase[0])}")

    print()

    print("--- LN CONVERGENCE TEST INJECTION ---")
    print("Copy paste this into your data segment\n")
    print(f".word {len(convergence_test_cases)}")
    for testcase in convergence_test_cases:
        print(f'.word {3}, {float_to_ieee(testcase[0])}, {testcase[1]}')

    print()

    print("--- LN CONVERGENCE TESTCASES ---")
    for testcase in convergence_test_cases:
        result = ln(*testcase)
        print(f"ln({float(testcase[0])}), {testcase[1]} terms := Taylor FP32 Value = {float_to_ieee(result)} = {result} | Function value = {np.log(testcase[0])}")

    print()

    print("--- LN EDGE TEST INJECTION ---")
    print("Copy paste this into your data segment\n")
    print(f".word {len(edge_test_cases)}")
    for testcase in edge_test_cases:
        print(f'.word {3}, {float_to_ieee(testcase[0])}, {testcase[1]}')

    print()

    print("--- LN EDGE TESTCASES ---")
    for testcase in edge_test_cases:
        result = ln(*testcase)
        if testcase[0] > 0:
            print(f"ln({float(testcase[0])}), {testcase[1]} terms := Taylor FP32 Value = {float_to_ieee(result)} = {result} | Function value = {np.log(testcase[0])}")
        else:
            print(f"ln({float(testcase[0])}), {testcase[1]} terms := Taylor FP32 Value = {float_to_ieee(result)} = {result} | Function value = undefined (out of domain)")

    print()

# reciprocal
if(code == 4):
    test_cases = [
        [np.float32(1.0), np.int32(5)],     # 1/1 = 1
        [np.float32(0.5), np.int32(8)],     # 1/0.5 = 2
        [np.float32(1.5), np.int32(6)],     # 1/1.5
        [np.float32(0.8), np.int32(7)],     # 1/0.8
        [np.float32(1.2), np.int32(15)],    # 1/1.2
    ]

    convergence_test_cases = [
        [np.float32(0.5), np.int32(1)],
        [np.float32(0.5), np.int32(3)],
        [np.float32(0.5), np.int32(5)],
        [np.float32(0.5), np.int32(10)],
        [np.float32(0.5), np.int32(15)],
    ]

    edge_test_cases = [
        [np.float32(1.0), np.int32(0)],     # Zero terms
        [np.float32(0.5), np.int32(-1)],    # Negative terms
        [np.float32(0.0), np.int32(10)],    # Out of domain: division by zero
        [np.float32(-1.0), np.int32(10)],   # Negative input
        [np.float32(3.0), np.int32(30)],    # Out of convergence range |x-1| >= 1
    ]

    print("--- RECIPROCAL TEST INJECTION ---")
    print("Copy paste this into your data segment\n")
    print(f".word {len(test_cases)}")
    for testcase in test_cases:
        print(f'.word {4}, {float_to_ieee(testcase[0])}, {testcase[1]}')

    print()

    print("--- RECIPROCAL TESTCASES ---")
    for testcase in test_cases:
        result = reciprocal(*testcase)
        print(f"1/({float(testcase[0])}), {testcase[1]} terms := Taylor FP32 Value = {float_to_ieee(result)} = {result} | Function value = {1.0/testcase[0]}")

    print()

    print("--- RECIPROCAL CONVERGENCE TEST INJECTION ---")
    print("Copy paste this into your data segment\n")
    print(f".word {len(convergence_test_cases)}")
    for testcase in convergence_test_cases:
        print(f'.word {4}, {float_to_ieee(testcase[0])}, {testcase[1]}')

    print()

    print("--- RECIPROCAL CONVERGENCE TESTCASES ---")
    for testcase in convergence_test_cases:
        result = reciprocal(*testcase)
        print(f"1/({float(testcase[0])}), {testcase[1]} terms := Taylor FP32 Value = {float_to_ieee(result)} = {result} | Function value = {1.0/testcase[0]}")

    print()

    print("--- RECIPROCAL EDGE TEST INJECTION ---")
    print("Copy paste this into your data segment\n")
    print(f".word {len(edge_test_cases)}")
    for testcase in edge_test_cases:
        print(f'.word {4}, {float_to_ieee(testcase[0])}, {testcase[1]}')

    print()

    print("--- RECIPROCAL EDGE TESTCASES ---")
    for testcase in edge_test_cases:
        result = reciprocal(*testcase)
        if testcase[0] != 0:
            print(f"1/({float(testcase[0])}), {testcase[1]} terms := Taylor FP32 Value = {float_to_ieee(result)} = {result} | Function value = {1.0/testcase[0]}")
        else:
            print(f"1/({float(testcase[0])}), {testcase[1]} terms := Taylor FP32 Value = {float_to_ieee(result)} = {result} | Function value = undefined (division by zero)")

    print()
