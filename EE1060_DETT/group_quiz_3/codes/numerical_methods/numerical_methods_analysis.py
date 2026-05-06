import numpy as np
import matplotlib.pyplot as plt

# Circuit and signal parameters
resistance_cases = [1000, 100, 10]  
inductance_cases = [1, 1, 1]  
period_cases = [0.01, 0.05, 0.1] 
dutyRatios = [0.2, 0.5, 0.8] 
amplitude = 10

# Square wave function
def squareWave(period, dutyRatio, amplitude, currentTime):
    return amplitude if currentTime % period <= period * dutyRatio else 0

# Numerical methods
def eulerMethod(resistance, inductance, timeVector, stepSize, initialCurrentValue, period, dutyRatio):
    current = np.zeros_like(timeVector)
    current[0] = initialCurrentValue
    for n in range(len(timeVector) - 1):
        Time = timeVector[n]
        currentValue = current[n]
        voltageValue = squareWave(period, dutyRatio, amplitude, Time)
        dIdt = (voltageValue - resistance * currentValue) / inductance
        current[n + 1] = currentValue + stepSize * dIdt
    return current

def reverseEulerMethod(resistance, inductance, timeVector, stepSize, initialCurrentValue, period, dutyRatio):
    current = np.zeros_like(timeVector)
    current[0] = initialCurrentValue
    for n in range(len(timeVector) - 1):
        Time = timeVector[n]
        voltageValue_next = squareWave(period, dutyRatio, amplitude, Time + stepSize)
        current[n+1] = (current[n] + (stepSize / inductance) * voltageValue_next) / (1 + (stepSize * resistance) / inductance)
    return current

def rk4Method(resistance, inductance, timeVector, stepSize, initialCurrentValue, period, dutyRatio):
    current = np.zeros_like(timeVector)
    current[0] = initialCurrentValue
    for n in range(len(timeVector) - 1):
        Time = timeVector[n]
        currentValue = current[n]
        voltageValue = squareWave(period, dutyRatio, amplitude, Time)

        k1 = (voltageValue - resistance * currentValue) / inductance
        k2 = (squareWave(period, dutyRatio, amplitude, Time + stepSize/2) - resistance * (currentValue + (stepSize/2) * k1)) / inductance
        k3 = (squareWave(period, dutyRatio, amplitude, Time + stepSize/2) - resistance * (currentValue + (stepSize/2) * k2)) / inductance
        k4 = (squareWave(period, dutyRatio, amplitude, Time + stepSize) - resistance * (currentValue + stepSize * k3)) / inductance

        current[n + 1] = currentValue + (stepSize / 6) * (k1 + 2*k2 + 2*k3 + k4)
    return current

# Steady-State and Transient Response Analysis
plt.figure(figsize=(12, 8))
stepSize = period_cases[0] / 1000
timeEnd = 30 * period_cases[0]
timeVector = np.arange(0, timeEnd, stepSize)

for i in range(3):
    resistance = resistance_cases[i]
    inductance = inductance_cases[i]
    
    eulerCurrent = eulerMethod(resistance, inductance, timeVector, stepSize, 0.0, period_cases[0], dutyRatios[1])
    reverseEulerCurrent = reverseEulerMethod(resistance, inductance, timeVector, stepSize, 0.0, period_cases[0], dutyRatios[1])
    rk4Current = rk4Method(resistance, inductance, timeVector, stepSize, 0.0, period_cases[0], dutyRatios[1])
    
    steadyStateCurrent = (amplitude * dutyRatios[1]) / resistance
    
    plt.subplot(3, 1, i + 1)
    plt.plot(timeVector, eulerCurrent, label='Euler Method')
    plt.plot(timeVector, reverseEulerCurrent, label='Reverse Euler Method')
    plt.plot(timeVector, rk4Current, label='RK4 Method')
    plt.axhline(y=steadyStateCurrent, color='k', linestyle='--', label='Steady-State Current')
    plt.xlabel("Time (s)")
    plt.ylabel("Current (A)")
    plt.title(f"R={resistance}, L={inductance}")
    plt.legend()
    plt.grid(True)
plt.tight_layout()
plt.savefig("steady_state_comparison.png")
plt.show()

# Effect of Duty Cycle on Average Current
plt.figure(figsize=(12, 6))
for dutyRatio in dutyRatios:
    rk4Current = rk4Method(resistance_cases[1], inductance_cases[1], timeVector, stepSize, 0.0, period_cases[0], dutyRatio)
    steadyStateCurrent = (amplitude * dutyRatio) / resistance_cases[1]
    plt.plot(timeVector, rk4Current, label=f'α={dutyRatio}')
    plt.axhline(y=steadyStateCurrent, color='k', linestyle='--')
plt.xlabel("Time (s)")
plt.ylabel("Current (A)")
plt.title("Effect of Duty Cycle on Current")
plt.legend()
plt.grid(True)
plt.savefig("duty_cycle_effect.png")
plt.show()

# Numerical Frequency Response Analysis
frequencies = np.logspace(-1, 3, 50)  # Logarithmic frequency range (0.1Hz to 1kHz)
magnitude_response = []

resistance = resistance_cases[1]
inductance = inductance_cases[1]

for freq in frequencies:
    period = 1 / freq
    stepSize = period / 1000
    timeEnd = 30 * period
    timeVector = np.arange(0, timeEnd, stepSize)

    current = rk4Method(resistance, inductance, timeVector, stepSize, 0.0, period, dutyRatios[1])
    vout = inductance * np.gradient(current, stepSize)  # Compute VL = L dI/dt
    vin = np.array([squareWave(period, dutyRatios[1], amplitude, t) for t in timeVector])

    gain = np.max(np.abs(vout)) / np.max(np.abs(vin))  # Compute |Vout/Vin|
    magnitude_response.append(gain)

# Bode Plot - Numerical Frequency Response
plt.figure(figsize=(10, 6))
plt.semilogx(frequencies, 20 * np.log10(magnitude_response), label="Magnitude Response")
plt.xlabel("Frequency (Hz")
plt.ylabel("Magnitude (dB)")
plt.title("Numerical Frequency Response of RL Circuit")
plt.grid(True, which="both", linestyle="--")
plt.legend()
plt.savefig("bode_plot.png")
plt.show()
