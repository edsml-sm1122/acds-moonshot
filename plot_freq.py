import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

def plot_frequency_distribution(path):
    df = pd.read_csv(path)

    sns.displot(df, x="crater_size", kde=False)

    plt.xlabel("Crater Size (km)")
    plt.ylabel("Frequency")
    plt.title("Size-Frequency Distribution of Craters")

    plt.show()
