from reliability.Distributions import Weibull_Distribution
from reliability.Fitters import Fit_Weibull_2P
from reliability.Probability_plotting import plot_points
import matplotlib.pyplot as plt

data = Weibull_Distribution(alpha=25,beta=4).random_samples(30)
weibull_fit = Fit_Weibull_2P(failures=data,show_probability_plot=False,print_results=False)
weibull_fit.distribution.PDF(label='Fitted Distribution',color='steelblue')
plot_points(failures=data,func='PDF',label='failure data',color='red',alpha=0.7)

plt.legend()
plt.show()