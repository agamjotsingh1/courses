"""Preview the nine generated datasets."""
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# categorical slots 1-3 validate all-pairs (scatter) in light mode;
# slot 4 (violet) is carried by MARKER SHAPE as secondary encoding.
HUES    = ["#2a78d6", "#eb6834", "#1baf7a", "#6250d6"]
MARKERS = ["o", "s", "^", "D"]
INK, MUTED = "#0b0b0b", "#52514e"
LEVELS = ["tight", "medium", "loose"]

def read_csv(p):
    return np.loadtxt(p, delimiter=",", comments="#")

def read_truth(p):
    return np.loadtxt(p, delimiter=",", comments="#", ndmin=2)

fig, axes = plt.subplots(3, 3, figsize=(11.5, 11.8), constrained_layout=True)

for r, K in enumerate((2, 3, 4)):
    for c, lvl in enumerate(LEVELS):
        ax = axes[r, c]
        stem = f"blobs2d_k{K}_{lvl}"
        X = read_csv(f"{stem}.csv")
        T = read_truth(f"{stem}_truth.csv")
        Y = T[:, 1:3]

        # assign each point to its nearest true centre, for colouring only
        lab = np.argmin(((X[:, None, :] - Y[None, :, :]) ** 2).sum(-1), axis=1)

        ax.plot([1, 0, -1, 0, 1], [0, 1, 0, -1, 0], color="0.6", lw=1.2,
                ls="-", zorder=1)                      # the L1 ball boundary
        for j in range(K):
            m = lab == j
            ax.scatter(X[m, 0], X[m, 1], s=7, marker=MARKERS[j],
                       color=HUES[j], alpha=0.55, linewidths=0, zorder=2,
                       label=f"cluster {j}" if (r == 2 and c == 0) else None)
            ax.scatter(*Y[j], s=230, marker="*", color=HUES[j],
                       edgecolor="black", linewidth=1.6, zorder=5)
            ax.annotate(str(j), Y[j], textcoords="offset points",
                        xytext=(9, 7), fontsize=9, color=INK, weight="bold",
                        zorder=6)                      # direct label = relief rule

        ax.set_xlim(-1.12, 1.12); ax.set_ylim(-1.12, 1.12)
        ax.set_aspect("equal")
        ax.grid(alpha=0.18, lw=0.5)
        for s in ax.spines.values():
            s.set_color("0.75")
        ax.tick_params(colors=MUTED, labelsize=8)
        sig = {"tight": 0.045, "medium": 0.090, "loose": 0.160}[lvl]
        ax.set_title(f"K={K}, {lvl}  ($\\sigma$={sig})", color=INK, fontsize=11)
        if c == 0: ax.set_ylabel("$x_2$", color=MUTED)
        if r == 2: ax.set_xlabel("$x_1$", color=MUTED)

axes[2, 0].legend(fontsize=8, loc="lower left", framealpha=0.95, markerscale=2)
fig.suptitle("Generated datasets: $n=1000$, all points inside $\\|x\\|_1 \\leq 1$",
             color=INK, fontsize=13)
fig.savefig("preview.png", dpi=150)
fig.savefig("preview.pdf")
print("wrote preview.png / preview.pdf")
