import numpy as np
import matplotlib.pyplot as plt

# Circuit and signal params
resistance = 500
inductance = 5
period = 0.01
dutyRatio = 0.2
amplitude = 10

# Square wave function
def squareWave(period, dutyRatio, amplitude, currentTime):
    return amplitude if currentTime % period <= period * dutyRatio else 0

# Step sizes for comparison
stepSizesFractions = [1/10, 1/100, 1/1000]
stepSizes = [period * fraction for fraction in stepSizesFractions]
smallStepSize = period / 10000  # Reference step size

# Time vector
simulationTime = 10 * period

# Numerical Methods
def eulerMethod(R, L, T, D, A, timeVector, stepSize, I0):
    current = np.zeros_like(timeVector)
    current[0] = I0
    for n in range(len(timeVector) - 1):
        v = squareWave(T, D, A, timeVector[n])
        dIdt = (v - R * current[n]) / L
        current[n + 1] = current[n] + stepSize * dIdt
    return current

def reverseEulerMethod(R, L, T, D, A, timeVector, stepSize, I0):
    current = np.zeros_like(timeVector)
    current[0] = I0
    for n in range(len(timeVector) - 1):
        v_next = squareWave(T, D, A, timeVector[n] + stepSize)
        current[n+1] = (current[n] + (stepSize / L) * v_next) / (1 + (stepSize * R) / L)
    return current

def trapezoidalMethod(R, L, T, D, A, timeVector, stepSize, I0):
    current = np.zeros_like(timeVector)
    current[0] = I0
    for n in range(len(timeVector) - 1):
        v_n = squareWave(T, D, A, timeVector[n])
        v_np1 = squareWave(T, D, A, timeVector[n] + stepSize)
        # More stable implementation (often preferred for stiff equations):
        current[n+1] = (current[n] * (2*L - stepSize*R) + stepSize * (v_n + v_np1)) / (2*L + stepSize*R)
    return current


def rk2Method(R, L, T, D, A, timeVector, stepSize, I0):
    current = np.zeros_like(timeVector)
    current[0] = I0
    for n in range(len(timeVector) - 1):
        v = squareWave(T, D, A, timeVector[n])
        k1 = (v - R * current[n]) / L
        v_mid = squareWave(T, D, A, timeVector[n] + stepSize/2)
        k2 = (v_mid - R * (current[n] + (stepSize/2) * k1)) / L
        current[n + 1] = current[n] + stepSize * k2
    return current

def rk4Method(R, L, T, D, A, timeVector, stepSize, I0):
    current = np.zeros_like(timeVector)
    current[0] = I0
    for n in range(len(timeVector) - 1):
        Time = timeVector[n]
        currentValue = current[n]
        voltageValue = squareWave(T, D, A, Time)

        k1 = (voltageValue - R * currentValue) / L
        k2 = (squareWave(T, D, A, Time + stepSize/2) - R * (currentValue + (stepSize/2) * k1)) / L
        k3 = (squareWave(T, D, A, Time + stepSize/2) - R * (currentValue + (stepSize/2) * k2)) / L
        k4 = (squareWave(T, D, A, Time + stepSize) - R * (currentValue + stepSize * k3)) / L

        current[n + 1] = currentValue + (stepSize / 6) * (k1 + 2*k2 + 2*k3 + k4)
    return current

# Run simulations and store results
methods = {"Euler": eulerMethod, "Reverse Euler": reverseEulerMethod, "Trapezoidal": trapezoidalMethod, "RK2": rk2Method, "RK4": rk4Method}
simulationResults = {}
timeVectors = {}
for stepSize in stepSizes:
    timeVectors[stepSize] = np.arange(0, simulationTime, stepSize)
    simulationResults[stepSize] = {}
    for method, function in methods.items():
        simulationResults[stepSize][method] = function(resistance, inductance, period, dutyRatio, amplitude, timeVectors[stepSize], stepSize, 0.0)

# Generate reference solution with RK4 at a very small step size
timeVectorRef = np.arange(0, simulationTime, smallStepSize)
referenceSolution = rk4Method(resistance, inductance, period, dutyRatio, amplitude, timeVectorRef, smallStepSize, 0.0)

# Plot method comparison for each step size
for stepSize in stepSizes:
    plt.figure(figsize=(10, 6))
    plt.title(f"Numerical Method Comparison (Step Size = {stepSize:.6g}s)")
    plt.xlabel("Time (s)")
    plt.ylabel("Current (A)")
    plt.grid(True)
    
    for method in methods.keys():
        plt.plot(timeVectors[stepSize], simulationResults[stepSize][method], label=method)
    
    # Plot reference RK4 solution
    plt.plot(timeVectorRef, referenceSolution, linestyle='--', color='black', alpha=0.7, label='RK4 Reference')
    
    plt.legend()
    plt.savefig(f"MethodComparison_{stepSize:.6g}.png")
    plt.show()
    plt.close()
