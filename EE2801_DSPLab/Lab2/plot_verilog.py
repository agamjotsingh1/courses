import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

f_s = 48e3 # sampling frequency of the sampled sine wave
f = 1e3

plot_cycles = 5
plot_ticks = int((plot_cycles/f)/(1/f_s))

# read the result.csv file
desired_columns = ['time', 'original', 'q2_14', 'q4_12', 'add', 'sub', 'mul']
df = pd.read_csv('data/result.csv', usecols=desired_columns)
t = df['time']
q2_14 = df['q2_14']
q4_12 = df['q4_12']
add_result = df['add']
sub_result = df['sub']
mul_result = df['mul']

add_ideal_result = q2_14 + q4_12
sub_ideal_result = q2_14 - q4_12
mul_ideal_result = q2_14 * q4_12

plt.step(t[:plot_ticks], q2_14[:plot_ticks], label=f"Original Signal $x(t)$ in Q(2, 14) format")
plt.step(t[:plot_ticks], q4_12[:plot_ticks], label=f"Original Signal $x(t)$ in Q(4, 12) format")

plt.title(f"<Verilog> Original plots")
plt.legend()
plt.savefig(f"plots/original.png")
plt.show()


# --- ADD ---

plt.step(t[:plot_ticks], add_ideal_result[:plot_ticks], label=f"Python Added Signals")
plt.step(t[:plot_ticks], add_result[:plot_ticks], label=f"Verilog Added Signals")

plt.title(f"<Verilog> Add plots")
plt.legend()
plt.savefig(f"plots/add.png")
plt.show()

plt.step(t[:plot_ticks], add_ideal_result[:plot_ticks] - add_result[:plot_ticks], label=f"Error in Python vs Verilog")
print(np.mean(add_ideal_result[:plot_ticks] - add_result[:plot_ticks]))

plt.title(f"<Verilog> Add error plots")
plt.legend()
plt.savefig(f"plots/add_error.png")
plt.show()

# --- SUB ---

plt.step(t[:plot_ticks], sub_ideal_result[:plot_ticks], label=f"Python Subtracted Signals")
plt.step(t[:plot_ticks], sub_result[:plot_ticks], label=f"Verilog Subtracted Signals")

plt.title(f"<Verilog> Sub plots")
plt.legend()
plt.savefig(f"plots/sub.png")
plt.show()

plt.step(t[:plot_ticks], sub_ideal_result[:plot_ticks] - sub_result[:plot_ticks], label=f"Error in Python vs Verilog")

plt.title(f"<Verilog> Sub error plots")
plt.legend()
plt.savefig(f"plots/sub_error.png")
plt.show()

# --- MUL ---

plt.step(t[:plot_ticks], mul_ideal_result[:plot_ticks], label=f"Python Multiplied Signals")
plt.step(t[:plot_ticks], mul_result[:plot_ticks], label=f"Verilog Multiplied Signals")

plt.title(f"<Verilog> Mul plots")
plt.legend()
plt.savefig(f"plots/mul.png")
plt.show()

plt.step(t[:plot_ticks], mul_ideal_result[:plot_ticks] - mul_result[:plot_ticks], label=f"Error in Python vs Verilog")
print(np.mean(mul_ideal_result[:plot_ticks] - mul_result[:plot_ticks]))

plt.title(f"<Verilog> Mul error plots")
plt.legend()
plt.savefig(f"plots/mul_error.png")
plt.show()