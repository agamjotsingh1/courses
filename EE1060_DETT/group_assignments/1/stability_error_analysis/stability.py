import numpy as np
import matplotlib.pyplot as plt

# Circuit and signal params
inductance = 0.001
period = 0.001
dutyRatio = 0.5
amplitude = 10

# Square wave function
def squareWave(period, dutyRatio, amplitude, currentTime):
    if currentTime % period <= period * dutyRatio:
        return amplitude
    else:
        return 0

# Step size
stepSize = period / 1000

# Time vector
timeEnd = 10 * period  # Simulate for 5 periods
timeVector = np.arange(0, timeEnd, stepSize)

# Initialize arrays to store results for different numerical methods
eulerCurrent = np.zeros_like(timeVector)
rk2Current = np.zeros_like(timeVector)
rk4Current = np.zeros_like(timeVector)
trapezoidalCurrent = np.zeros_like(timeVector)
reverseEulerCurrent = np.zeros_like(timeVector)

# Initial condition for current
initialCurrentValue = 0.0
eulerCurrent[0] = initialCurrentValue
rk2Current[0] = initialCurrentValue
rk4Current[0] = initialCurrentValue
trapezoidalCurrent[0] = initialCurrentValue
reverseEulerCurrent[0] = initialCurrentValue

#Numerical methods
def eulerMethod(resistance, inductance, period, dutyRatio, amplitude, timeVector, stepSize, initialCurrentValue):
    """Implements Euler's method."""
    current = np.zeros_like(timeVector)
    current[0] = initialCurrentValue
    for n in range(len(timeVector) - 1):
        Time = timeVector[n]
        currentValue = current[n]
        voltageValue = squareWave(period, dutyRatio, amplitude, Time)
        dIdt = (voltageValue - resistance * currentValue) / inductance
        current[n + 1] = currentValue + stepSize * dIdt
    return current

def rk2Method(resistance, inductance, period, dutyRatio, amplitude, timeVector, stepSize, initialCurrentValue):
    """Implements RK2 (Midpoint) method."""
    current = np.zeros_like(timeVector)
    current[0] = initialCurrentValue
    for n in range(len(timeVector) - 1):
        Time = timeVector[n]
        currentValue = current[n]
        voltageValue = squareWave(period, dutyRatio, amplitude, Time)
        k1 = (voltageValue - resistance * currentValue) / inductance
        voltageValue_mid = squareWave(period, dutyRatio, amplitude, Time + stepSize/2)
        k2 = (voltageValue_mid - resistance * (currentValue + (stepSize/2) * k1)) / inductance
        current[n + 1] = currentValue + stepSize * k2
    return current

def rk4Method(resistance, inductance, period, dutyRatio, amplitude, timeVector, stepSize, initialCurrentValue):
    """Implements RK4 (Classic) method."""
    current = np.zeros_like(timeVector)
    current[0] = initialCurrentValue
    for n in range(len(timeVector) - 1):
        Time = timeVector[n]
        currentValue = current[n]
        voltageValue = squareWave(period, dutyRatio, amplitude, Time)

        k1 = (voltageValue - resistance * currentValue) / inductance

        voltageValue_k2 = squareWave(period, dutyRatio, amplitude, Time + stepSize/2)
        k2 = (voltageValue_k2 - resistance * (currentValue + (stepSize/2) * k1)) / inductance

        voltageValue_k3 = squareWave(period, dutyRatio, amplitude, Time + stepSize/2)
        k3 = (voltageValue_k3 - resistance * (currentValue + (stepSize/2) * k2)) / inductance

        voltageValue_k4 = squareWave(period, dutyRatio, amplitude, Time + stepSize)
        k4 = (voltageValue_k4 - resistance * (currentValue + stepSize * k3)) / inductance

        current[n + 1] = currentValue + (stepSize / 6) * (k1 + 2*k2 + 2*k3 + k4)
    return current

def trapezoidalMethod(resistance, inductance, period, dutyRatio, amplitude, timeVector, stepSize, initialCurrentValue):
    """Implements Trapezoidal method."""
    current = np.zeros_like(timeVector)
    current[0] = initialCurrentValue
    for n in range(len(timeVector) - 1):
        Time = timeVector[n]
        currentValue = current[n]
        nextTime = timeVector[n+1]
        voltageValue_n = squareWave(period, dutyRatio, amplitude, Time)
        voltageValue_next = squareWave(period, dutyRatio, amplitude, nextTime)

        current[n+1] = (currentValue + (stepSize / (2 * inductance)) * (voltageValue_n + voltageValue_next) - (stepSize * resistance / (2 * inductance)) * currentValue) / (1 + (stepSize * resistance) / (2 * inductance))
    return current


def reverseEulerMethod(resistance, inductance, period, dutyRatio, amplitude, timeVector, stepSize, initialCurrentValue):
    """Implements Reverse Euler (Backward Euler) method."""
    current = np.zeros_like(timeVector)
    current[0] = initialCurrentValue
    for n in range(len(timeVector) - 1):
        Time = timeVector[n]
        currentValue = current[n]
        nextTime = timeVector[n+1]
        voltageValue_next = squareWave(period, dutyRatio, amplitude, nextTime)

        current[n+1] = (currentValue + (stepSize / inductance) * voltageValue_next) / (1 + (stepSize * resistance) / inductance)
    return current

# Run simulations with appropriate R values for each method

# Forward Euler
eulerResistanceValues = [1000, 1500, 1750, 2000, 2100]
for resistance in eulerResistanceValues:
    eulerCurrent = eulerMethod(resistance, inductance, period, dutyRatio, amplitude, timeVector, stepSize, initialCurrentValue)
    
    plt.figure(figsize=(8, 6))
    plt.title(f'RL Circuit Response - Step Size = {stepSize}, R = {resistance}, L = {inductance}')
    plt.plot(timeVector, eulerCurrent, label='Forward Euler Method')
    plt.xlabel('Time (s)')
    plt.ylabel('Current (A)')
    plt.legend()
    plt.grid(True)
    plt.savefig(f"./figs/euler_R{resistance}_L{inductance}.png")
    plt.close()

# RK2
rk2ResistanceValues = [1000, 1500, 1750, 2000, 2100]
for resistance in rk2ResistanceValues:
    rk2Current = rk2Method(resistance, inductance, period, dutyRatio, amplitude, timeVector, stepSize, initialCurrentValue)
    
    plt.figure(figsize=(8, 6))
    plt.title(f'RL Circuit Response - Step Size = {stepSize}, R = {resistance}, L = {inductance}')
    plt.plot(timeVector, rk2Current, label='RK2 Method')
    plt.xlabel('Time (s)')
    plt.ylabel('Current (A)')
    plt.legend()
    plt.grid(True)
    plt.savefig(f"./figs/rk2_R{resistance}_L{inductance}.png")
    plt.close()

# RK4
rk4ResistanceValues = [1000, 1500, 2000, 2250, 2500, 2750, 2850]
for resistance in rk4ResistanceValues:
    rk4Current = rk4Method(resistance, inductance, period, dutyRatio, amplitude, timeVector, stepSize, initialCurrentValue)
    
    plt.figure(figsize=(8, 6))
    plt.title(f'RL Circuit Response - Step Size = {stepSize}, R = {resistance}, L = {inductance}')
    plt.plot(timeVector, rk4Current, label='RK4 Method')
    plt.xlabel('Time (s)')
    plt.ylabel('Current (A)')
    plt.legend()
    plt.grid(True)
    plt.savefig(f"./figs/rk4_R{resistance}_L{inductance}.png")
    plt.close()

# Backward Euler
reverseEulerResistanceValues = [1000, 1500, 2000, 2500, 5000, 10000]
for resistance in reverseEulerResistanceValues:
    reverseEulerCurrent = reverseEulerMethod(resistance, inductance, period, dutyRatio, amplitude, timeVector, stepSize, initialCurrentValue)
    
    plt.figure(figsize=(8, 6))
    plt.title(f'RL Circuit Response - Step Size = {stepSize}, R = {resistance}, L = {inductance}')
    plt.plot(timeVector, reverseEulerCurrent , label='Reverse Euler Method')
    plt.xlabel('Time (s)')
    plt.ylabel('Current (A)')
    plt.legend()
    plt.grid(True)
    plt.savefig(f"./figs/reverseEuler_R{resistance}_L{inductance}.png")
    plt.close()

# Trapezoidal
trapezoidalResistanceValues = [1000, 1500, 2000, 2500, 5000, 10000]
for resistance in trapezoidalResistanceValues:
    trapezoidalCurrent = trapezoidalMethod(resistance, inductance, period, dutyRatio, amplitude, timeVector, stepSize, initialCurrentValue)
    
    plt.figure(figsize=(8, 6))
    plt.title(f'RL Circuit Response - Step Size = {stepSize}, R = {resistance}, L = {inductance}')
    plt.plot(timeVector, trapezoidalCurrent, label='Trapezoidal Method')
    plt.xlabel('Time (s)')
    plt.ylabel('Current (A)')
    plt.legend()
    plt.grid(True)
    plt.savefig(f"./figs/trapezoidal_R{resistance}_L{inductance}.png")
    plt.close()
