from reliability.Distributions import Weibull_Distribution
from reliability.Fitters import Fit_Weibull_2P
from reliability.Probability_plotting import plot_points
import matplotlib.pyplot as plt
from collections import Counter


class GraphGenerator:

    def get_dataset(file_name):
        with open(file_name) as file:
            dataset = [int(date.strip()) for date in file]
        return dataset


    @staticmethod
    def export_graphs(dataset_file, image_name):
        dataset = GraphGenerator.get_dataset(dataset_file)

        hist = Counter()
        axis_y = []
        for date in dataset:
            hist[date] += 1

        for date in dataset:
            axis_y.append(hist[date])

        plt.suptitle('Padrão de chegada de bugs')
        plt.xlabel('Meses')
        plt.ylabel('Bugs reportados')

        plt.plot(dataset, axis_y)
        plt.savefig(image_name)

# dataset = get_dataset('vue_dataset.txt')

# hist = Counter()
# axis_y = []
# for date in dataset:
#     hist[date] += 1

# for date in dataset:
#     axis_y.append(hist[date])

# plt.suptitle('Padrão de chegada de bugs')
# plt.ylabel('bugs reportados')
# plt.xlabel('meses')
# plt.plot(dataset, axis_y)
# plt.savefig('vuejs_bugs_reports.png')

# # data = Weibull_Distribution(alpha=25,beta=4).random_samples(30)
# weibull_fit = Fit_Weibull_2P(failures=dataset, show_probability_plot=False,print_results=False)

# print(weibull_fit.alpha)

# weibull_fit.distribution.PDF(label='Fitted Distribution',color='steelblue')
# plot_points(failures=dataset,func='PDF',label='failure data',color='red',alpha=0.7)

# plt.legend()