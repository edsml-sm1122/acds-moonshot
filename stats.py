import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

def plot_frequency_distribution(path):
    df = pd.read_csv(path)

    sns.displot(df, x="crater_size", kde=False)

    plt.xlabel("Crater Size (km)")
    plt.ylabel("Frequency")
    plt.title("Size-Frequency Distribution of Craters")

    plt.show()

def confusion_matrix():
    statistics_files = [f for f in os.listdir("output/statistics")]
    df_list = [pd.read_csv(os.path.join("output/statistics", f)) for f in statistics_files]

    df = pd.concat(df_list)
    pivot_table = df.pivot_table(index="Stats", values="Count", aggfunc=np.sum)
    # True negative needs to be calculated: TN = Total observations - (TP + FP + FN) 
    # But, what is the total observations?? (number of instances that were evaluated by the classifier)

    pivot_table = pivot_table.fillna(0)
    print(pivot_table)

    sns.heatmap(pivot_table, annot=True, fmt="d")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.title("Confusion Matrix")
    plt.show()

confusion_matrix()