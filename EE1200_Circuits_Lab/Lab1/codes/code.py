import numpy as np
import matplotlib.pyplot as plt

def plot_parametric_function(parametric_func, t_range, fig_name, labels):
    """
    Plots a parametric function and saves the figure.

    Parameters:
    - parametric_func: A tuple of two functions (f1, f2) that depend on t.
    - t_range: A tuple (start, end, num_points) defining the range of t.
    - fig_name: The name of the file to save the figure.
    - labels: A tuple of labels (label1, label2) for the functions.
    """
    t = np.linspace(t_range[0], t_range[1], t_range[2])
    f1, f2 = parametric_func
    
    y1 = f1(t)
    y2 = f2(t)

    plt.plot(y1, y2, label=f"${labels[0]}$ vs ${labels[1]}$")
    plt.axis('square')
    plt.xlim(-1.5, 1.5)
    plt.ylim(-1.5, 1.5)
    plt.legend(loc="upper left")  # Place the legend in the top-left corner
    plt.title("Parametric Plot")
    plt.savefig(fig_name)
    plt.show()

# Example usage
def f11(t):
    return np.sin(t)

def f12(t):
    return np.sin(t + np.pi / 2)

plot_parametric_function(
    (f11, f12), 
    (0, 20, 1000), 
    "../figs/fig1_verify.png", 
    ("\\sin(t)", "\\sin(t+\\frac{\\pi}{2})")
)

def f21(t):
    return np.sin(t)

def f22(t):
    return np.sin(t)

plot_parametric_function(
    (f21, f22), 
    (0, 20, 1000), 
    "../figs/fig2_verify.png", 
    ("\\sin(t)", "\\sin(t)")
)

def f31(t):
    return np.sin(t + np.pi / 4)

def f32(t):
    return np.sin(6*t + np.pi / 2)

plot_parametric_function(
    (f31, f32), 
    (0, 20, 1000), 
    "../figs/fig3_verify.png", 
    ("\\sin(t+\\frac{\\pi}{4})", "\\sin(6t+\\frac{\\pi}{2})")
)

def f41(t):
    return np.sin(4*t + np.pi / 4)

def f42(t):
    return np.sin(6*t + np.pi / 2)

plot_parametric_function(
    (f41, f42), 
    (0, 20, 1000), 
    "../figs/fig4_verify.png", 
    ("\\sin(4t+\\frac{\\pi}{4})", "\\sin(6t+\\frac{\\pi}{2})")
)

def f51(t):
    return np.sin(3*t + np.pi / 4)

def f52(t):
    return np.sin(8*t + np.pi / 2)

plot_parametric_function(
    (f51, f52), 
    (0, 20, 1000), 
    "../figs/fig5_verify.png", 
    ("\\sin(3t+\\frac{\\pi}{4})", "\\sin(8t+\\frac{\\pi}{2})")
)

def f61(t):
    return np.sin(t)

def f62(t):
    return np.sin(t + np.pi / 4)

plot_parametric_function(
    (f61, f62), 
    (0, 20, 1000), 
    "../figs/fig6_verify.png", 
    ("\\sin(t)", "\\sin(t+\\frac{\\pi}{4})")
)
