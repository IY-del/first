from collections.abc import Generator

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.axes import Axes
from matplotlib.figure import Figure


def ScatterRegression(
    fig: Figure, x: pd.Series, xlabel: str, nsubfig: int
) -> Generator[tuple[int, int], tuple[pd.Series, str]]:
    n = 0
    x_line = np.linspace(x.min(), x.max(), 100)
    y: pd.Series
    ylabel: str
    ax: Axes

    def plot_line(ax: Axes, y: pd.Series, color: str = "red") -> None:
        def get_plot_args() -> tuple[np.ndarray, str]:
            def make_args(a, b) -> tuple[np.ndarray, str]:
                return a * x_line + b, f"fit: y={a:.2f}x+{b:.2f}"

            return make_args(*np.polyfit(x, y, 1))

        line, label = get_plot_args()
        ax.plot(x_line, line, "-", color=color, label=label)

    while n < nsubfig:
        n += 1
        y, ylabel = yield n, nsubfig
        ax = fig.add_subplot(1, nsubfig, n)
        ax.plot(x, y, ".", label="data")
        plot_line(ax, y)
        ax.set_xlabel(xlabel, fontsize=8)
        ax.set_ylabel(ylabel, fontsize=8)
        ax.legend(fontsize=6)


# Load data
data = pd.read_csv("/content/drive/MyDrive/TechRep_work/score.csv")

# Draw graphs
fig = plt.figure(figsize=(12, 4))

scatter_regression = ScatterRegression(fig, data["売上高(億円)"], "Amount of Sale", 3)
next(scatter_regression)

scatter_regression.send((data["1.接客スコア"], "Score of Hospitality"))
scatter_regression.send((data["2.品揃えスコア"], "Score of Assortment"))
scatter_regression.send((data["3.立地スコア"], "Score of Location"))

plt.subplots_adjust(wspace=0.4, hspace=0.4)
plt.show()
