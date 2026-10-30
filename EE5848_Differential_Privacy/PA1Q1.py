import argparse

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon
from scipy.spatial import ConvexHull, HalfspaceIntersection
from scipy.stats import laplace, norm

parser = argparse.ArgumentParser()
parser.add_argument("--eps", type=float)
parser.add_argument("--delta", type=float)
parser.add_argument("--sens", type=float)

args = parser.parse_args()
eps = args.eps
delta = args.delta
sens = args.sens

assert(eps > 0)
assert(delta >= 0)
assert(delta < 1)

# -- q1 --
# 0 < alpha < 1, 0 < beta < 1
A1 = np.array([[-1, 0], [1, 0], [0, -1], [0, 1]])
v1 = np.array([[0], [1], [0], [1]])

# (eps, delta) constraints
A2 = np.array([[-1, -np.exp(eps)], [1, np.exp(eps)], [-np.exp(eps), -1], [np.exp(eps), 1]])
v2 = np.array([[delta - 1], [delta + np.exp(eps)], [delta - 1], [delta + np.exp(eps)]])

A = np.vstack((A1, A2))
v = np.vstack((v1, v2))

halfspaces = np.column_stack((A, -v))
interior_point = np.array([0.5, 0.5])
hs = HalfspaceIntersection(halfspaces, interior_point)
vertices = hs.intersections

hull = ConvexHull(vertices)
ordered_vertices = vertices[hull.vertices]

fig, ax = plt.subplots(figsize=(8, 8))

margin = 0.3
xmin = min(vertices[:, 0].min() - margin, -0.2)
xmax = max(vertices[:, 0].max() + margin, 1.2)
ymin = min(vertices[:, 1].min() - margin, -0.2)
ymax = max(vertices[:, 1].max() + margin, 1.2)

poly = Polygon(
    ordered_vertices,
    facecolor="lightblue",
    edgecolor="blue",
    alpha=0.4,
    label="Feasible Region ($Au \\leq v$)",
)
ax.add_patch(poly)

line_labels = [
    r"$\alpha = 0$",
    r"$\alpha = 1$",
    r"$\beta = 0$",
    r"$\beta = 1$",
    r"$-\alpha - e^\epsilon \beta = \delta - 1$",
    r"$\alpha + e^\epsilon \beta = \delta + e^\epsilon$",
    r"$-e^\epsilon \alpha - \beta = \delta - 1$",
    r"$e^\epsilon \alpha + \beta = \delta + e^\epsilon$",
]

x_vals = np.linspace(xmin, xmax, 400)
colors = plt.cm.tab10(np.linspace(0, 1, len(A)))

for i in range(len(A)):
    a_x, a_y = A[i, 0], A[i, 1]
    val = v[i, 0]

    if np.isclose(a_y, 0):
        # vertical boundary line
        ax.axvline(
            x=val / a_x,
            color=colors[i],
            linestyle="--",
            linewidth=1,
            alpha=0.5,
            label=line_labels[i],
        )
    else:
        # non-vertical boundary line
        y_vals = (val - a_x * x_vals) / a_y
        ax.plot(
            x_vals,
            y_vals,
            color=colors[i],
            linestyle="--",
            linewidth=1,
            alpha=0.5,
            label=line_labels[i],
        )

ax.set_xlim(xmin, xmax)
ax.set_ylim(ymin, ymax)
ax.set_xlabel(r"$\alpha$")
ax.set_ylabel(r"$\beta$")
ax.grid(True, linestyle="--", alpha=0.6)
ax.set_aspect("equal")
ax.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
plt.title(f"Region and Boundaries defined by $Au \\leq v$ ($\\epsilon={eps}, \\delta={delta}$)")
plt.tight_layout()
plt.savefig("feasible_region.png")
plt.show()

# TODO!

# -- q2 & 3 --
t = np.arange(-(2*eps), (2*eps), 1e-4)

# for t not in [-eps, eps]:
# a) t < -eps : At = full real set
# b) t > eps : At = null set

# mode = lap or gauss
def alpha(t, sens, mode='lap'):
    if mode == 'lap':
        lam = sens/eps
        # note that t is only defined from [-eps, eps] for lap
        # for this thresh to be valid
        thresh = (sens/2) * (1 - t/eps)
        if t < -eps:
            return 0.0
        elif t > eps:
            return 1.0
        else:
            return (1 - laplace.cdf(thresh, loc=0.0, scale=lam))
    elif mode == 'gauss':
        thresh = (sens/2) * (1 - 4*(t/eps)*np.log(2/delta))
        sigma = (sens/eps) * np.sqrt(2*np.log(2/delta))
        return (1 - norm.cdf(thresh, loc=0.0, scale=sigma))
    else:
        raise TypeError("Invalid mode: lap or gauss.")


# mode = lap or gauss
def beta(t, sens, mode='lap'):
    if mode == 'lap':
        lam = sens/eps
        # note that t is only defined from [-eps, eps] for lap
        # for this thresh to be valid
        thresh = (sens/2) * (1 - t/eps)
        if t < -eps:
            return 1.0
        elif t > eps:
            return 0.0
        else:
            return laplace.cdf(thresh, loc=sens, scale=lam)
    elif mode == 'gauss':
        thresh = (sens/2) * (1 - 4*(t/eps)*np.log(2/delta))
        sigma = (sens/eps) * np.sqrt(2*np.log(2/delta))
        return norm.cdf(thresh, loc=sens, scale=sigma)
    else:
        raise TypeError("Invalid mode: lap or gauss.")

alpha_vec = np.vectorize(alpha)
beta_vec = np.vectorize(beta)

# plt.figure(figsize=(8, 5))
# plt.plot(t, alpha_vec(t, sens, 'lap'), label=r'$\alpha(t)$ for Lap', linewidth=2)
# plt.plot(t, beta_vec(t, sens, 'lap'), label=r'$\beta(t)$ for Lap', linewidth=2)
# plt.plot(t, alpha_vec(t, sens, 'gauss'), label=r'$\alpha(t)$ for Gauss', linewidth=2)
# plt.plot(t, beta_vec(t, sens, 'gauss'), label=r'$\beta(t)$ for Gauss', linewidth=2)
#
# plt.title(f'Plot of $\\alpha(t)$ and $\\beta(t)$ (with $\\epsilon = {eps}, \\Delta = {sens}$)')
# plt.xlabel('t')
# plt.grid(True, linestyle='--', alpha=0.7)
# plt.legend()
# plt.tight_layout()
# plt.show()

alpha_lap = alpha_vec(t, sens, 'lap')
beta_lap = beta_vec(t, sens, 'lap')

alpha_gauss = alpha_vec(t, sens, 'gauss')
beta_gauss = beta_vec(t, sens, 'gauss')

fig, ax = plt.subplots(figsize=(8, 8))

poly = Polygon(
    ordered_vertices,
    facecolor="lightblue",
    edgecolor="none",
    alpha=0.5,
    label=r"Feasible Region ($Au \leq v$)",
)
ax.add_patch(poly)

# for lap, the curve is only continuous for t in [-eps, eps].
mask_lap = (t >= -eps) & (t <= eps)

ax.plot(alpha_lap[mask_lap], beta_lap[mask_lap], label='Laplace Mechanism', linewidth=2, color='tab:orange')
lap_alpha_start, lap_beta_start = alpha_lap[mask_lap][0], beta_lap[mask_lap][0]
lap_alpha_end, lap_beta_end = alpha_lap[mask_lap][-1], beta_lap[mask_lap][-1]
ax.plot([0.0, lap_alpha_start], [1.0, lap_beta_start], color='tab:orange', linestyle=':', linewidth=2)
ax.plot([lap_alpha_end, 1.0], [lap_beta_end, 0.0], color='tab:orange', linestyle=':', linewidth=2)
ax.plot(alpha_gauss, beta_gauss, label='Gaussian Mechanism', linewidth=2, color='tab:green')
ax.plot([0, 1], [1, 0], color='black', linestyle=':', label=f'\\alpha + \\beta = 1')

ax.set_title(f'Parametric curve overlaid on Feasible Region\n($\\epsilon = {eps}, \\delta = {delta}, \\Delta = {sens}$)')
ax.set_xlabel(r'$\alpha(t)$')
ax.set_ylabel(r'$\beta(t)$')
ax.set_xlim(-0.02, 1.02)
ax.set_ylim(-0.02, 1.02)
ax.set_aspect("equal")
ax.grid(True, linestyle='--', alpha=0.7)
ax.legend(loc="upper right")
plt.tight_layout()
plt.savefig("alpha_beta_parametric.png")
plt.show()

# checking for inconsistency at some sens
tol = 1e-6
sens_set = np.linspace(start=1.0, stop=10.0, num=10)
prev_sens = sens_set[0]

for s in sens_set:
    if np.any(np.abs(alpha_vec(t, s, 'lap') - alpha_vec(t, prev_sens, 'lap')) > tol):
        print(f"Found some sens={s} for which alpha differs in Lap mechanism!")
        break

    if np.any(np.abs(beta_vec(t, s, 'lap') - beta_vec(t, prev_sens, 'lap')) > tol):
        print(f"Found some sens={s} for which beta differs in Lap mechanism!")
        break
    prev_sens = s

print("""1.2.2 Remarks:
    thresh = (sens/2 * ( 1 - t/epsilon ))
    and laplace noise (Z) variance itself depends on sens (lam = sens/epsilon),
    so they cancel out and alpha and beta do not depend on sens at all.
""")

print("""1.2.3 Remarks:
    thresh = (sens/2 - sigma^2*(t/sens))
    alpha = 1 - norm_cdf(rho/2 - t/rho)
    beta = norm_cdf(-rho/2 - t/rho)
    where alpha and beta depend ONLY on rho (sens/sigma).

    in reality, alpha and beta dont really depend on sens,
    as sigma is proportional to sens so it cancels out.
    rho is, in reality, independent of sens.
""")
