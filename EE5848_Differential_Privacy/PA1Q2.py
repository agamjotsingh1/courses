import argparse
import math

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

def project_l1_ball(p, radius=1.0):
    if np.sum(np.abs(p)) <= radius:
        return p
    a = np.abs(p)
    u = np.sort(a)[::-1]
    css = np.cumsum(u)
    ks = np.arange(1, len(p) + 1)
    rho = np.nonzero(u * ks > (css - radius))[0][-1]
    theta = (css[rho] - radius) / (rho + 1.0)
    return np.sign(p) * np.maximum(a - theta, 0.0)

# Args:
# data -> (*xN) matrix contains vectors
# K -> number of clusters
# T -> number of iterations
# dp -> DP or not
# sens, eps -> only valid if DP is valid
# sens -> max one norm of data possible
# rng -> numpy rng generator (preferably seeded)
# Returns:
# (T, K, N) dimensional array for centers for all T iters
def lloyd(data, K, T, dp=False, eps=1.0, rng=np.random.default_rng()):
    N = 2 # dimension of feature space
    centers = np.empty((T+1, K, N))

    if dp:
        eps_sum = eps_count = eps/(2*T)

    u = rng.uniform(low=-1.0, high=1.0, size=K)
    v = rng.uniform(low=-1.0, high=1.0, size=K)
    centers[0] = np.column_stack(((u + v) / 2, (u - v) / 2))

    for t in range(T):
        # add a new axis and then broadcast
        distances = np.linalg.norm(data[:, np.newaxis] - centers[t], axis=2)
        labels = np.argmin(distances, axis=1)

        for k in range(K):
            cluster = data[labels == k]

            if cluster.shape[0] == 0:
                center = np.zeros((N,))
            elif dp:
                noise_sum = rng.laplace(loc=0.0, scale=2.0/eps_sum, size=(N,))
                noise_count = rng.laplace(loc=0.0, scale=2.0/eps_count)

                noisy_count = max(cluster.shape[0] + noise_count, 1.0)
                center = (np.sum(cluster, axis=0) + noise_sum)/noisy_count
            else:
                center = np.sum(cluster, axis=0)/cluster.shape[0]

            centers[t+1][k] = project_l1_ball(center, 1.0)


    # ignore the inital random centers
    return centers[1:]

parser = argparse.ArgumentParser()
parser.add_argument("--data", default="lloyd_data/blobs2d_k4_tight.csv")
parser.add_argument("--eps", default=1.0, type=float)
parser.add_argument("--T", default=20, type=int)
parser.add_argument("--K", default=4, type=int)
parser.add_argument("--seed", default=0, type=int)

args = parser.parse_args()

data = np.empty((0, 2))

# data extraction
with open(args.data, mode='r') as file:
    for line in file:
        if line.startswith("#"):
            continue

        split_line = line.strip().split(',')

        if len(split_line) != 2:
            raise ValueError("Got invalid dimensions in data (2D is required).")

        new_row = np.array([[float(n) for n in split_line]])
        data = np.append(data, new_row, axis=0)

n = data.shape[0]
rng = np.random.default_rng(seed=args.seed)

eps = args.eps
T = args.T
K = args.K

assert(eps > 0)
assert(T >= 4)
assert(K >= 2)
assert(K <= n)

eps_dash = eps/T

# sub-composition #1: computing number of elements in each class
# basically a histogram query with sens = 2
sens1 = 2
b1 = sens1/(eps_dash/2)

# sub-composition #2: computing mean of each class
# as one norm of each data is less than 1, sens is 2
sens2 = 2
b2 = sens2/(eps_dash/2)

print(f"({eps_dash}, {b1}, {b2})")

rng_lloyd = np.random.default_rng(seed=args.seed)
centers_lloyd = lloyd(data, K, T, dp=False, rng=rng_lloyd)

rng_dp = np.random.default_rng(seed=args.seed)
centers_dp = lloyd(data, K, T, dp=True, eps=eps, rng=rng_dp)

print("\nFinal Lloyd Centers:")
for c in centers_lloyd[-1]:
    print(f"[{c[0]:.4f}, {c[1]:.4f}]")

print("\nFinal DP-Lloyd Centers:")
for c in centers_dp[-1]:
    print(f"[{c[0]:.4f}, {c[1]:.4f}]")

print()

t_vals = [math.ceil(T/4), math.ceil(T/2), math.ceil(3*T/4), T]

def wcss(data, centers):
    distances = np.linalg.norm(data[:, np.newaxis] - centers, axis=2)
    labels = np.argmin(distances, axis=1)
    wcss = 0.0

    for k in range(centers.shape[0]):
        cluster = data[labels == k]
        wcss += np.sum((cluster - centers[k])**2)

    return wcss

# WCSS
for t in t_vals:
    wcss_lloyd = wcss(data, centers_lloyd[t-1])
    wcss_dp = wcss(data, centers_dp[t-1])
    print(f"t={t:2d} | Lloyd WCSS: {wcss_lloyd:.4f} | DP-Lloyd WCSS: {wcss_dp:.4f}")

# WCSS varying T for DP-lloyd
t_dp_vals = [2, 5, 10, 20, 50, 100]
wcss_dp_vals = []

for T_dp in t_dp_vals:
    rng_dp = np.random.default_rng(seed=args.seed)
    centers_T_dp = lloyd(data, K, T_dp, dp=True, eps=eps, rng=rng_dp)
    wcss_dp_vals.append(wcss(data, centers_T_dp[-1]))

plt.figure(figsize=(8, 5))
plt.plot(t_dp_vals, wcss_dp_vals, marker='o', linewidth=2, color='crimson', label=f'DP-Lloyd ($\epsilon={eps}$)')

plt.title(f"DP-Lloyd Final WCSS vs. Number of Rounds ($T$)", fontsize=12)
plt.xlabel("Number of Iterations ($T$)", fontsize=11)
plt.ylabel("Final WCSS", fontsize=11)
plt.xticks(t_dp_vals)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()
plt.tight_layout()
plt.savefig("dp_rounds_convergence.png")
plt.show()

# WCSS and DP-Lloyd Panel Grid varying EPS (fixed T, fixed K)
eps_dp_vals = [0.1, 1.0, 10.0]
wcss_dp_vals = []

for eps_val in eps_dp_vals:
    rng_dp = np.random.default_rng(seed=args.seed)
    centers_eps_dp = lloyd(data, K, T, dp=True, eps=eps_val, rng=rng_dp)
    wcss_dp_vals.append(wcss(data, centers_eps_dp[-1]))

plt.figure(figsize=(8, 5))
plt.plot(eps_dp_vals, wcss_dp_vals, marker='o', linewidth=2, color='crimson', label='DP-Lloyd')
plt.xscale('log')
plt.xticks(eps_dp_vals, labels=['0.1', '1.0', '10.0'])
plt.title(f"DP-Lloyd Final WCSS vs. Privacy Budget ($\epsilon$) [T={T}, K={K}]", fontsize=12)
plt.xlabel("Privacy Budget ($\epsilon$)", fontsize=11)
plt.ylabel("Final WCSS", fontsize=11)
plt.grid(True, which="both", linestyle='--', alpha=0.6)
plt.legend()
plt.tight_layout()
plt.savefig("dp_eps_convergence.png")
plt.show()

fig_eps, axes_eps = plt.subplots(
    len(eps_dp_vals), len(t_vals),
    figsize=(8, 5.5),
    sharex=True,
    sharey=True
)

fig_eps.suptitle(f"DP-Lloyd across Privacy Budgets ($\epsilon$) [T={T}, K={K}, seed={args.seed}]", fontsize=11, y=0.98)

cmap = plt.get_cmap('tab10')
colors = [cmap(k % 10) for k in range(K)]

for row_idx, eps_val in enumerate(eps_dp_vals):
    rng_dp = np.random.default_rng(seed=args.seed)
    centers_eps_dp = lloyd(data, K, T, dp=True, eps=eps_val, rng=rng_dp)

    eps_dash_val = eps_val / T
    b1_val = 2.0 / (eps_dash_val / 2.0)
    b2_val = 2.0 / (eps_dash_val / 2.0)

    for col_idx, t in enumerate(t_vals):
        ax = axes_eps[row_idx, col_idx]
        current_centers = centers_eps_dp[t - 1]
        distances = np.linalg.norm(data[:, np.newaxis] - current_centers, axis=2)
        labels = np.argmin(distances, axis=1)

        for k in range(K):
            cluster_points = data[labels == k]
            ax.scatter(cluster_points[:, 0], cluster_points[:, 1],
                       color=colors[k], s=5, alpha=0.4, zorder=1)
            ax.scatter(current_centers[k, 0], current_centers[k, 1],
                       marker='*', s=120, color=colors[k],
                       edgecolors='black', linewidths=1.2, zorder=10)

        ax.set_xlim([-1.1, 1.1])
        ax.set_ylim([-1.1, 1.1])
        ax.set_aspect('equal')

        if row_idx == 0:
            ax.set_title(f"$t={t}$", fontsize=9, pad=3)
        if col_idx == 0:
            ax.set_ylabel(f"$\epsilon={eps_val}$", fontsize=9, fontweight='bold')

        annotation_text = f"$\epsilon'$={eps_dash_val:.3f}\nb1=b2={b1_val:.1f}"
        ax.text(0.04, 0.04, annotation_text, transform=ax.transAxes,
                fontsize=6.5, verticalalignment='bottom',
                bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.8, edgecolor='gray'))

legend_elements = [Line2D([0], [0], marker='o', color='w', label=f'C{k}',
                          markerfacecolor=colors[k], markersize=6) for k in range(K)]
legend_elements.append(Line2D([0], [0], marker='*', color='w', label='Center',
                              markerfacecolor='gray', markeredgecolor='black',
                              markersize=10, markeredgewidth=1.2))

fig_eps.legend(handles=legend_elements, loc='lower center', ncol=K+1, bbox_to_anchor=(0.5, -0.02), fontsize=8, frameon=False)

plt.subplots_adjust(wspace=0.0, hspace=0.08, left=0.07, right=0.98, top=0.91, bottom=0.10)
plt.savefig("dp_eps_bottom_rows.png", bbox_inches='tight', dpi=300)
plt.show()

# full plot
algos = [("Lloyd", centers_lloyd), ("DP-Lloyd", centers_dp)]

cmap = plt.get_cmap('tab10')
colors = [cmap(k % 10) for k in range(K)]

fig, axes = plt.subplots(2, 4, figsize=(16, 8))
fig.suptitle(f"n={n}, K={K}, T={T}, eps={eps}, seed={args.seed}")

for row, (algo_name, centers_all) in enumerate(algos):
    for col, t in enumerate(t_vals):
        ax = axes[row, col]
        current_centers = centers_all[t-1]
        distances = np.linalg.norm(data[:, np.newaxis] - current_centers, axis=2)
        labels = np.argmin(distances, axis=1)
        for k in range(K):
            cluster_points = data[labels == k]
            ax.scatter(cluster_points[:, 0], cluster_points[:, 1],
                       color=colors[k], s=10, alpha=0.5, zorder=1)
        for k in range(K):
            ax.scatter(current_centers[k, 0], current_centers[k, 1],
                       marker='*', s=250, color=colors[k],
                       edgecolors='black', linewidths=1.6, zorder=10)

        ax.set_xlim([-1.1, 1.1])
        ax.set_ylim([-1.1, 1.1])
        ax.set_aspect('equal')

        ax.set_title(f"{algo_name}, t={t}")

        if row == 1:
            annotation_text = f"eps'={eps_dash:.4f}\nb1={b1:.4f}\nb2={b2:.4f}"
            ax.text(0.05, 0.05, annotation_text, transform=ax.transAxes,
                    fontsize=9, verticalalignment='bottom',
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8, edgecolor='gray'))

legend_elements = [Line2D([0], [0], marker='o', color='w', label=f'Cluster {k}',
                          markerfacecolor=colors[k], markersize=8) for k in range(K)]
legend_elements.append(Line2D([0], [0], marker='*', color='w', label='Center',
                              markerfacecolor='gray', markeredgecolor='black',
                              markersize=15, markeredgewidth=1.6))

fig.legend(handles=legend_elements, loc='lower center', ncol=K+1, bbox_to_anchor=(0.5, 0.02))
plt.tight_layout(rect=[0, 0.08, 1, 1])
plt.savefig("lloyd_convergence.png")
plt.show()
