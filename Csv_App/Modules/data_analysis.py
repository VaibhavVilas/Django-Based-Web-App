# module which performs analysis on the csv file

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from io import StringIO

# function that will perform analysis on given csv file


def perform(filename):

    # to read csv file and convert it into a DataFrame
    df = pd.read_csv(filename)

    # to get first 5 rows of the DataFrame
    head = df.head()

    # these 3 lines allow df.info() to be shown as an html
    buffer = StringIO()
    # summary of DataFrame'structure and content
    df.info(buf=buffer)
    structure = buffer.getvalue()

    # to get all statistical metrics of a values in DataFrame's columns
    overall_statistics = df.describe()

    # to get median of each numeric column
    median = df.median(numeric_only=True)

    # to check for missing values
    missing_values = df.isnull().sum()

    # list to save all plots file path
    plots = []
    # to generate histograms for each numeric column present in the DataFrame
    for column in df.select_dtypes(include=[np.number]).columns:
        plt.figure()
        sns.histplot(df[column].dropna(), kde=False)
        # saving plots in media directory and path in plots list
        plot_path = os.path.join('media', f'{column}_histogram.png')
        plt.savefig(plot_path)
        plt.close()
        plots.append(plot_path)

    # saving all necessary values in a dictionary after converting them to html
    result = {
        'head': head.to_html(),
        'structure': structure,
        'description': overall_statistics.to_html(),
        # to_frame() converts series to DataFrame
        'median': median.to_frame().to_html(),
        'check_missing_values': missing_values.to_frame().to_html(),
        'plots': plots
    }

    # returning the dicionary
    return result
