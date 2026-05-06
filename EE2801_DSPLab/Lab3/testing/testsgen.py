import tomllib
import csv
import numpy as np

# read the config
with open("config.toml", "rb") as file:
    config = tomllib.load(file)

indexing = int(config['indexing'])
int_nbits = int(config["int_nbits"])
frac_nbits = int(config["frac_nbits"])

def float_to_fixed(num):
    total_nbits = int_nbits + frac_nbits
    scaled_num = np.round(num * (2**frac_nbits)).astype(int)
    
    MASK = (1 << total_nbits) - 1
    twos_comp_num = scaled_num & MASK
    
    return f"{twos_comp_num:0{total_nbits}x}"

# tests = [
#     (1.0, 29.0),
#     (15.0, 23.0),
#     (10.0, 79.0),
#     (2.0, 63.0),
#     (1.0, 3.0),
#     (64.0, 7.0),
#     (0.5, 8.0),
#     (255.0, 255.0),
#     (-1.0, 38.0)
# ]

tests = [
    (1.0, 29.0),
    (42.0, 31.0),
    (7.25, 19.0),
    (128.0, 47.0),
    (0.75, 5.0),
    (91.0, 53.0),
    (-4.0, 59.0),
    (-22.5, 71.0),
    (-0.125, 43.0),
    (12.0, 97.0)
]
with open("testing/tests.csv", "w") as file:
    data = csv.writer(file)
    data.writerow(("num1", "num2"))

    print(float_to_fixed(tests[-1][0]))

    tests_fixed_point = [(float_to_fixed(n1), float_to_fixed(n2)) for n1, n2 in tests]
    data.writerows(tests_fixed_point)

print("Successfully generated tests from testgen.py")