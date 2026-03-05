import marimo

__generated_with = "0.19.11"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import scipy.io as sio
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns

    return np, plt, sio


@app.cell
def _(np, sio):
    data = sio.loadmat('hw6_5.mat')
    h1 = data['h1'].flatten()
    h2 = data['h2'].flatten()
    h3 = data['h3'].flatten()

    def makeA(h, N=42, M_conv=65):
        """
        Build convolution matrix (M_conv x N), then downsample rows by 2.
        h:      filter (length 30)
        N:      input length (42 pixels per column)
        M_conv: convolution output length (indices 0..64 = 65 samples)
        """
        L = len(h)
        H = np.zeros((M_conv, N))
        for col in range(N):
            for row in range(M_conv):
                fi = row - col
                if 0 <= fi < L:
                    H[row, col] = h[fi]
        # downsample by 2: keep rows 0,2,4,...,64 → 33 rows
        return H[::2, :]   # shape: (33, 42)

    A1 = makeA(h1)   # 33 x 42
    A2 = makeA(h2)   # 33 x 42
    A3 = makeA(h3)   # 33 x 42

    A = np.vstack([A1, A2, A3])  # 99 x 42
    print(A.shape)  # should be (99, 42)
    return A, data


@app.cell
def _(A, np):
    U, s, Vh = np.linalg.svd(A, full_matrices=False)
    print(f"Condition number κ(A) = {s[0]/s[-1]:.2f}")
    return U, Vh, s


@app.cell
def _(U, Vh, data, np, plt, s):
    d1 = data['d1']  # 33x80
    d2 = data['d2']
    d3 = data['d3']

    def reconstruct(filter_fn, lam):
        X_hat = np.zeros((42, 80))
        for q in range(80):
            b_q = np.concatenate([d1[:,q], d2[:,q], d3[:,q]])
            X_hat[:,q] = filter_fn(s, U, Vh, b_q, lam)
        return X_hat

    def tikhonov(s, U, Vh, b, lam):
        return Vh.T @ (s/(s**2 + lam**2) * (U.T @ b))

    def threshold(s, U, Vh, b, lam):
        f = np.where(s >= lam, 1/s, 0.0)
        return Vh.T @ (f * (U.T @ b))

    def thresh_to_zero(s, U, Vh, b, lam):
        f = np.where(s >= lam, (s - lam)/s**2, 0.0)
        return Vh.T @ (f * (U.T @ b))

    lambdas = [0.01, 0.05, 0.1, 0.3]

    fig, axes = plt.subplots(3, 4, figsize=(16, 8))
    for i, lam in enumerate(lambdas):
        axes[0,i].imshow(reconstruct(tikhonov, lam),     cmap='gray', aspect='auto')
        axes[0,i].set_title(f'Tikhonov λ={lam}')
        axes[0,i].axis('off')

        axes[1,i].imshow(reconstruct(threshold, lam),    cmap='gray', aspect='auto')
        axes[1,i].set_title(f'Threshold λ={lam}')
        axes[1,i].axis('off')

        axes[2,i].imshow(reconstruct(thresh_to_zero, lam), cmap='gray', aspect='auto')
        axes[2,i].set_title(f'Thresh-to-zero λ={lam}')
        axes[2,i].axis('off')

    axes[0,0].set_ylabel('Tikhonov')
    axes[1,0].set_ylabel('Threshold')
    axes[2,0].set_ylabel('Thresh-to-zero')

    plt.tight_layout()
    plt.savefig('hw6_p5b.png', dpi=150)
    plt.show()
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
