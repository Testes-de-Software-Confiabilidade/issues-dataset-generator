from reliability.Fitters import Fit_Weibull_2P
from reliability.Utils import generate_X_array

from firebase import Firebase
from rq import get_current_job

import matplotlib.pyplot as plt
from collections import Counter
import scipy.stats as ss


class GraphGenerator:

    def __init__(self, dataset_generator):
        self.dg = dataset_generator
    
    # def linear_regression(self, axis_x, axis_y):
    #     from sklearn import linear_model
    #     axis_x = np.array(axis_x).reshape((-1, 1))
    #     axis_y = np.array(axis_y)

    #     model = linear_model.LinearRegression().fit(axis_x, axis_y)
        
    #     line_y = model.predict(axis_x)
    #     plt.plot(axis_x, line_y,  color='blue', linewidth=1)

    #     plt.suptitle('Regressão Linear no último terço do repositório do software Spring')
    #     plt.savefig(self.dg.repository.chart_name_linear)

    def weibull(self):

        months = self.dg.get_issue_months()

        hist = Counter(months)
        axis_y = [hist[month] for month in months]
        
        fig, ax1 = plt.subplots()

        ax1.set_xlabel('Meses')
        ax1.set_ylabel('Bugs reportados', color='tab:red')
        ax1.plot(months, axis_y, color='tab:red')

        # Gerar gráfico para regressão linear do último terço
        # _size = len(months)//3
        # self.linear_regression(months[2*_size:], axis_y[2*_size:])

        plt.suptitle('Padrão de chegada de issues de\nBug do Repositório %s' % (self.dg.repository.name))
    
        wb = Fit_Weibull_2P(failures=months,show_probability_plot=False,print_results=True)
        weibull = wb.distribution

        X = generate_X_array(dist=weibull, xvals=None, xmin=None, xmax=None)
        Y = ss.weibull_min.pdf(X, weibull.beta, scale=weibull.alpha, loc=weibull.gamma)

        count = len([i for i in X if i < months[-1]+1 ])

        X = X[:count]
        Y = Y[:count]

        ax2 = ax1.twinx()
        ax2.set_ylabel('Função de densidade de probabilidade de Weibull', color='tab:blue')
        ax2.plot(X, Y, color='tab:blue')

        fig.tight_layout()
        plt.savefig(self.dg.repository.chart_name)
        
        job = get_current_job()
        job.meta['image_name'] = self.dg.repository.chart_name
        job.save_meta()

        # plt.show()

