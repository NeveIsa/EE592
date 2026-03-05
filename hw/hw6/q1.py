import marimo

__generated_with = "0.19.11"
app = marimo.App()


@app.cell(hide_code=True)
def _():
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns
    import scipy.io as sio

    import marimo as mo
    from scipy.sparse.linalg import svds

    return mo, np, plt, sio, sns


@app.cell(hide_code=True)
def _(mo):
    noise_flag  = mo.ui.switch(value=False, )
    noise_flag
    return (noise_flag,)


@app.cell(hide_code=True)
def _(noise_flag, np, sio):
    img = sio.loadmat("hw6_1.mat")['im']
    if noise_flag.value == True:
        np.random.seed(42)
        noise = np.random.randn(512,512)*0.2
        img += noise
        print("added noise")

    U,S,Vt = np.linalg.svd(img)
    K = np.min(img.shape)
    return S, U, Vt, img


@app.cell(hide_code=True)
def _(S, img, noise_flag, np, plt, sns):

    plt.figure(figsize=(20,5))
    plt.subplot(1,4,1)
    sns.lineplot(S, color='green')
    # plt.axvline(x=k.value, color='r', linestyle='--')
    plt.title("$\sigma_i(X) \;for\; 1 \leq i \leq 512$")
    plt.tight_layout()


    plt.subplot(1,4,2)
    sns.barplot(S[:20], color='green')
    # plt.axvline(x=k.value, color='r', linestyle='--')
    plt.title("$\sigma_i(X) \;for\; 1 \leq i \leq 20 $")
    plt.tight_layout()

    plt.subplot(1,4,3)
    sns.barplot(S[:20]/np.linalg.norm(img), color='green')
    # plt.axvline(x=k.value, color='r', linestyle='--')
    plt.title("$\sigma_i(X) \; / \; |X|_F \;for\; 1 \leq i \leq 20$")
    plt.tight_layout()

    plt.subplot(1,4,4)
    sns.barplot((np.cumsum(S**2)/np.linalg.norm(img)**2)[:20], color='lightgreen')
    plt.title("Cumulative normalized energy upto $\sigma_{20}$")

    if noise_flag.value: plt.suptitle("With added noise")
    plt.show()
    return


@app.cell(hide_code=True)
def _(S, U, Vt, img, noise_flag, np, plt):
    _MAX = 10

    plt.figure(figsize=(_MAX*3,3.5))

    plt.subplot(1,_MAX,_MAX)
    plt.imshow(img)
    plt.title('Original')


    for r in range(1,_MAX-1):
        plt.subplot(1,_MAX,r+1)

        imghat = U[:,:r] @ np.diag(S[:r]) @ Vt[:r,:]
        plt.imshow(imghat)


        plt.title(f'Rank={r} SVD')


    plt.tight_layout()



    if noise_flag.value: plt.suptitle("With added noise")

    plt.show()
    return


@app.cell(hide_code=True)
def _(S, U, Vt, img, noise_flag, np, plt):
    _MAX = 7

    plt.figure(figsize=(_MAX*3,3.5))

    plt.subplot(1,_MAX,_MAX)
    plt.imshow(img)
    plt.title('Original')


    for _r,R in enumerate([3, 10, 20, 30, 40, 50, 60]):
        plt.subplot(1,_MAX,_r+1)

        _imghat = U[:,:R] @ np.diag(S[:R]) @ Vt[:R,:]
        plt.imshow(_imghat)


        plt.title(f'Rank={R} | params = {(1025*R)}')

    if noise_flag.value: plt.suptitle("With added noise")

    plt.tight_layout()




    plt.show()
    return


@app.cell(hide_code=True)
def _(U, Vt, noise_flag, plt, sns):
    plt.figure(figsize=(15,3.5))

    plt.subplot(1,3,1)
    sns.lineplot(U[:,0], color="orange", label=f"$u_1$")
    sns.lineplot(Vt.T[:,0], color="lightgreen", label=f"$v_1$")
    plt.title("1st singular vectors")

    plt.subplot(1,3,2)
    sns.lineplot(U[:,1], color="orange", label=f"$u_2$")
    sns.lineplot(Vt.T[:,1], color="lightgreen", label=f"$v_2$")
    plt.title("2nd singular vectors")


    plt.subplot(1,3,3)
    sns.lineplot(U[:,0], color="orange", label=f"$u_3$")
    sns.lineplot(Vt.T[:,0], color="lightgreen", label=f"$v_3$")
    plt.title("3rd singular vectors")

    if noise_flag.value: plt.suptitle("With added noise")
    plt.tight_layout()
    plt.show()
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
