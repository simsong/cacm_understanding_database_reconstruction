import numpy as np
from pylab import plt
import matplotlib as mp

income = [ 31234,  53432,  69887,  65332,  70889,  75201, 90901, 195410]
grades = [30,50,90,95,70,65,50,95]

def make_plot(income,grades,outfile):
    """Make the plot and return the regression coefficients"""
    fit = np.polyfit(income,grades,1)
    fit_fn = np.poly1d(fit)
    income0 = [0] + income
    plt.plot(income, grades, 'yo',
             income0, fit_fn(income0), '--k')
    plt.title("Parent income vs. student grade\n y = {}x + {}".
              format(fit[0],fit[1]))
    plt.xlim(0, max(income))
    plt.ylim(0,100)
    plt.xticks(rotation=20)
    print(dir(plt))
    plt.axes().get_xaxis().set_major_formatter(
        mp.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
    plt.savefig("toy_regression.pdf")
    return fit

if __name__=="__main__":
    fit = make_plot(income, grades, "toy_regression.png")
    
