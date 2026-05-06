import numpy as np
import matplotlib.pyplot as plt

# Square wave function
def squareWave(period, dutyRatio, amplitude, currentTime):
    if currentTime % period <= period * dutyRatio:
        return amplitude
    else:
        return 0

def current_response(t, R, L, alpha, T, A=10, num_terms=1000):
    # First term (DC component)
    i = (A*alpha/R) * (1 - np.exp(-R*t/L))
    w0 = 2*np.pi/T
    
    # Sum of harmonic terms
    for n in range(1, num_terms+1):
        # Common denominator
        denom = R**2 + (L*n*w0)**2
        
        # First part with sin
        term1 = (A/(n*np.pi)) * np.sin(2*np.pi*alpha*n) * (
            (R*np.cos(n*w0*t) + n*w0*L*np.sin(n*w0*t))/denom - 
            (R/denom)*np.exp(-R*t/L)
        )
        
        # Second part with (1-cos)
        term2 = (A/(n*np.pi)) * (1 - np.cos(2*np.pi*alpha*n)) * (
            (R*np.sin(n*w0*t) - L*n*w0*np.cos(n*w0*t))/denom + 
            (n*w0*L/denom)*np.exp(-R*t/L)
        )
        
        i += term1 + term2
    
    return i

# Numerical methods
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

