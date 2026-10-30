#!/usr/bin/env python3
"""
Generate 2-D clustered datasets for the private-Lloyd assignment.

Every point satisfies ||x||_1 <= 1 (the cross-polytope / L1 ball in R^2).

Recipe
------
1. Draw K centres y_1..y_K uniformly from the L1 ball, rejection-resampled
   until they are mutually separated and sit away from the boundary.
2. For each of n points: draw J ~ Uniform{1..K}, then
   x = y_J + sigma * N(0, I_2), rejection-resampled until ||x||_1 <= 1.

Uniform sampling on the L1 ball is exact and rejection-free:
    u, v ~ U[-1,1],  x = ((u+v)/2, (u-v)/2)
because  (|u+v| + |u-v|)/2 == max(|u|,|v|) <= 1,  and the map is a bijection
from the square onto the ball with constant Jacobian.
"""
import argparse
import numpy as np

L1_MARGIN   = 0.75      # centres obey ||y||_1 <= L1_MARGIN, leaving room for noise
MIN_SEP     = {2: 0.70, 3: 0.60, 4: 0.52}   # min pairwise L2 distance between centres
NOISE = {"tight": 0.045, "medium": 0.090, "loose": 0.160}


def sample_l1_ball(m, rng, radius=1.0):
    """m points uniform on {||x||_1 <= radius}. Exact, no rejection."""
    u = rng.uniform(-radius, radius, m)
    v = rng.uniform(-radius, radius, m)
    return np.column_stack([(u + v) / 2.0, (u - v) / 2.0])


def sample_centres(K, rng, min_sep, radius, max_tries=200_000):
    """K centres in the shrunken L1 ball, pairwise L2 distance >= min_sep."""
    for _ in range(max_tries):
        Y = sample_l1_ball(K, rng, radius)
        if K == 1:
            return Y
        d = np.linalg.norm(Y[:, None, :] - Y[None, :, :], axis=-1)
        d[np.diag_indices(K)] = np.inf
        if d.min() >= min_sep:
            return Y
    raise RuntimeError(f"could not place {K} centres with min_sep={min_sep}")


def sample_points(Y, n, sigma, rng, max_rounds=1000):
    """n points: pick a centre uniformly, add N(0, sigma^2 I), keep inside the ball."""
    K = Y.shape[0]
    labels = rng.integers(0, K, n)
    X = np.empty((n, 2))
    todo = np.arange(n)
    for _ in range(max_rounds):
        cand = Y[labels[todo]] + sigma * rng.standard_normal((todo.size, 2))
        ok = np.abs(cand).sum(axis=1) <= 1.0
        X[todo[ok]] = cand[ok]
        todo = todo[~ok]
        if todo.size == 0:
            return X, labels
    raise RuntimeError(f"{todo.size} points still outside after {max_rounds} rounds")


def write_csv(path, X, K, sigma, seed, level):
    with open(path, "w") as fh:
        fh.write(f"# 2-D dataset for PA1 Q2 (private Lloyd's algorithm)\n")
        fh.write(f"# n={len(X)}  K={K}  noise_level={level}  sigma={sigma}  seed={seed}\n")
        fh.write(f"# every point satisfies ||x||_1 <= 1\n")
        fh.write(f"# x,y\n")
        for p in X:
            fh.write(f"{p[0]:.6f},{p[1]:.6f}\n")


def write_truth(path, Y, labels, K, sigma, seed, level):
    with open(path, "w") as fh:
        fh.write(f"# ground truth -- INSTRUCTOR COPY, do not release with the dataset\n")
        fh.write(f"# K={K}  noise_level={level}  sigma={sigma}  seed={seed}\n")
        fh.write("# cluster,centre_x,centre_y,n_points\n")
        for j in range(K):
            fh.write(f"{j},{Y[j,0]:.6f},{Y[j,1]:.6f},{int((labels==j).sum())}\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=1000)
    ap.add_argument("--seed", type=int, default=20261018)
    ap.add_argument("--outdir", default=".")
    args = ap.parse_args()

    print(f"{'file':<34}{'K':>3}{'sigma':>8}{'min dc':>9}{'sigma/dc':>10}"
          f"{'max |x|_1':>11}{'sizes':>22}")
    for K in (2, 3, 4):
        for level, sigma in NOISE.items():
            rng = np.random.default_rng(args.seed + 1000 * K + hash(level) % 97)
            Y = sample_centres(K, rng, MIN_SEP[K], L1_MARGIN)
            X, labels = sample_points(Y, args.n, sigma, rng)

            assert np.all(np.abs(X).sum(axis=1) <= 1.0 + 1e-12)
            assert len(X) == args.n

            stem = f"blobs2d_k{K}_{level}"
            write_csv(f"{args.outdir}/{stem}.csv", X, K, sigma, args.seed, level)
            write_truth(f"{args.outdir}/{stem}_truth.csv", Y, labels, K, sigma,
                        args.seed, level)

            d = np.linalg.norm(Y[:, None, :] - Y[None, :, :], axis=-1)
            d[np.diag_indices(K)] = np.inf
            dc = d.min()
            sizes = ",".join(str(int((labels == j).sum())) for j in range(K))
            print(f"{stem+'.csv':<34}{K:>3}{sigma:>8.3f}{dc:>9.3f}{sigma/dc:>10.3f}"
                  f"{np.abs(X).sum(1).max():>11.4f}{sizes:>22}")


if __name__ == "__main__":
    main()
