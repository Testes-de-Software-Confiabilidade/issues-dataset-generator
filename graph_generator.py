from reliability.Distributions import Weibull_Distribution
from reliability.Fitters import Fit_Weibull_2P
from reliability.Probability_plotting import plot_points
import matplotlib.pyplot as plt
from collections import Counter

import seaborn as sns


from reliability.Utils import generate_X_array
import scipy.stats as ss

class GraphGenerator:

    def get_dataset(file_name):
        with open(file_name) as file:
            dataset = [int(date.strip()) for date in file]
        return dataset


    @staticmethod
    def export_graphs(dataset_file, image_name, title):
        sns.set_theme()
        dataset = GraphGenerator.get_dataset(dataset_file)

        hist = Counter()
        axis_y = []
        for date in dataset:
            hist[date] += 1

        for date in dataset:
            axis_y.append(hist[date])

        fig, ax1 = plt.subplots()
        ax1.set_xlabel('Meses')
        ax1.set_ylabel('Bugs reportados', color='tab:red')
        ax1.plot(dataset, axis_y, color='tab:red')


        plt.suptitle(title)
    
        wb = Fit_Weibull_2P(failures=dataset,show_probability_plot=False,print_results=False)
        weibull = Weibull_Distribution(alpha=wb.alpha,beta=wb.beta)
        X = generate_X_array(dist=weibull, xvals=None, xmin=None, xmax=None)
        Y = ss.weibull_min.pdf(X, weibull.beta, scale=weibull.alpha, loc=weibull.gamma)
        
        print(dataset[-1])
        count = len([i for i in X if i < dataset[-1]+1 ])

        X = X[:count]
        Y = Y[:count]

        ax2 = ax1.twinx()
        ax2.set_ylabel('Função de densidade de probabilidade de Weibull', color='tab:blue')
        ax2.plot(X, Y, color='tab:blue')

        fig.tight_layout()
        plt.savefig(image_name)
