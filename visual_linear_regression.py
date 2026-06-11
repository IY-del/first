import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def ScatterRegression(x, xlabel, nfig):
    n = 0
    x_line = np.linspace(x.min(), x.max(), 100)
    while n < nfig:
        n += 1
        y1, label = yield n
        ax = fig.add_subplot(1, nfig, n)
        ax.plot(x, y1, ".", label="data")
        a1, b1 = np.polyfit(x, y1, 1)
        y1_line = a1 * x_line + b1
        ax.plot(x_line, y1_line, "-", color="red", label=f"fit: y={a1:.2f}x+{b1:.2f}")
        ax.set_xlabel(xlabel, fontsize=8)
        ax.set_ylabel(label, fontsize=8)
        ax.legend(fontsize=6)

# Load data
data = pd.read_csv("/content/drive/MyDrive/TechRep_work/score.csv")

scatter_regression = ScatterRegression(data["売上高(億円)"], "Amount of Sale", 3)
next(scatter_regression)

# Draw graphs
fig = plt.figure(figsize=(12, 4))

scatter_regression.send((data["1.接客スコア"], "Score of Hospitality"))
scatter_regression.send((data["2.品揃えスコア"], "Score of Assortment"))
scatter_regression.send((data["3.立地スコア"], "Score of Location"))

plt.subplots_adjust(wspace=0.4, hspace=0.4)
plt.show()