# beta_binomial.py


import numpy as np
from scipy.stats import bernoulli, beta
import matplotlib.pyplot as plt

def plot_coin_toss_bayesian_update(number_of_trials, data):
    """
    Plot the Bayesian update of coin tosses using the Beta-Binomial model.

    Parameters:
    number_of_trials (list of int): List of the number of coin tosses to simulate.
    data (numpy array): Array of coin toss results, where 0 represents tails and 1 represents heads.
    """
    x = np.linspace(0, 1, 100)

    fig, axes = plt.subplots(nrows=(len(number_of_trials) + 1) // 2, ncols=2, figsize=(10, 8))
    axes = axes.flatten()

    for i, N in enumerate(number_of_trials):
        heads = data[:N].sum()
        ax = axes[i]
        ax.set_title(f"{N} trials, {heads} heads")

        ax.set_xlabel("$P(H)$, Probability of Heads")
        ax.set_ylabel("Density")
        if i == 0:
            ax.set_ylim([0.0, 2.0])
        ax.set_yticklabels([])

        y = beta.pdf(x, 1 + heads, 1 + N - heads)
        ax.plot(x, y, label=f"observe {N} tosses,\n {heads} heads")
        ax.fill_between(x, 0, y, color="#aaaadd", alpha=0.5)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    number_of_trials = [0, 2, 10, 20, 50, 500]
    data = bernoulli.rvs(0.5, size=number_of_trials[-1])
    plot_coin_toss_bayesian_update(number_of_trials, data)
