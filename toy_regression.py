import numpy as np
from pylab import plt
import matplotlib as mp
import copy

from ttable import ttable

income = [ 31234,  53432,  69887,  65332,  70889,  75201, 90901, 195410]
grades = [30, 50, 90, 95, 70, 65, 50, 95]

def round_places(input_value,prec=4):
    from decimal import Decimal,ROUND_HALF_EVEN,Context
    ctx = Context(prec=prec, rounding=ROUND_HALF_EVEN)
    return float(ctx.create_decimal(input_value))

class Stats:
    def __init__(self,income,grades):
        # Set up the graph and draw the raw data
        self.income = income
        self.grades = grades
        plt.title("Parent income vs. student grade")
        plt.plot(self.income, self.grades, 'yo')
    
    def regress(self,prec=None,topcode=None,linecolor='k',linestyle='solid'):
        # Perform the regression, round the parameters (if requested), and
        # and draw the curve
        if topcode:
            self.income = [min(inc,topcode) for inc in self.income]
        self.fit = np.polyfit(self.income,self.grades,1)
        fit_fn = np.poly1d(self.fit)
        if prec:
            self.fit = [round_places(x,prec=prec) for x in self.fit]
        linex = [0, max(income)]
        legend = "y = {}x + {}".format(self.fit[0],self.fit[1])
        if topcode:
            legend += " (topcode={:,})".format(topcode)
        print("legend:",legend)
        plt.plot(linex, fit_fn(linex), color=linecolor, linestyle=linestyle,label=legend)
            
    def savefig(self,fname):
        # Graph using the parameters
        plt.xlim(0, max(self.income))
        plt.ylim(0,100)
        plt.legend(loc='lower right',fontsize=9)
        plt.xticks(rotation=20)
        #plt.axes().get_xaxis().set_major_formatter(mp.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
        plt.savefig(fname)

if __name__=="__main__":
    #
    # Write the data to a LaTeX file
    #

    topcode = 100000
    tab = ttable()
    tab.append_head(['parental income','grade'])
    tab.append_data(ttable.HR)
    for row in zip(income,grades):
        tab.append_data(row)
    tab.save_table("toy_regression_data.tex",mode='latex')

    # First show the regression with the real dat

    e = Stats(income, grades)
    e.regress()
    e.savefig("toy_regression.pdf")
    true_fit = copy.deepcopy(e.fit)

    # Now show the 4 regressions with a point the explores the state space

    # Now make a rounded version to 4 significant digits:
    g = copy.deepcopy(e)

    g.regress(prec=4,topcode=topcode,linecolor='red')
    g.savefig("toy_regression_rounded.pdf")

    # Explore the 4 areas
    fit_values = []             # array of fit values that we find
    linecolors = ['palegreen','aqua','dodgerblue','orange'] #  some colors
    
    tab = ttable()
    tab.append_head(['trial','income','grade'])

    # Run the regression at each of these values 
    i = 0
    for inc in [0,100000]:
        for gr in [0,100]:
            tab.append_data([i+1, inc, gr])
            g = copy.deepcopy(e)
            g.income.append(inc)
            g.grades.append(gr)
            g.regress(topcode=topcode,prec=4,linestyle='--',linecolor=linecolors[i])
            fit_values.append(copy.deepcopy(g.fit))
            i += 1
                     
    g.savefig("toy_regression_bounds.pdf")
    print("fit_values:",fit_values)

    G = []
    for i in range(0,2):
        values = [fit_value[i] for fit_value in fit_values]
        G.append(max(values) - min(values))

    tab.add_variable("Gzero",G[0])
    tab.add_variable("Gone",G[1])
    tab.save_table("toy_regression_extreme_data.tex",mode='latex')

    # Now let's show what adding noise looks like, at different values of epsilon
    n = len(income)
    tab = ttable()
    tab.append_head(['epsilon','true n','true $b_1$','true $b_0$',
                     'reported n','reported $G_1$','reported $G_0$'])
    tab.set_col_fmt(0,"","%2.1f","") # epsilon
    tab.set_col_fmt(2,"","%4.3e","") # b_1
    tab.set_col_fmt(3,"","%4.1f","") # b_0
    tab.set_col_fmt(5,"","%4.3e","") # b_1
    tab.set_col_fmt(6,"","%4.1f","") # b_0
    for ε in np.arange(0.1,2.0,.1):
        tab.append_data([ε, n, true_fit[0], true_fit[1],
                         int(n + np.random.normal(scale=1)/n),
                         round_places(true_fit[0] + np.random.normal(scale=G[0])/n),
                         round_places(true_fit[1] + np.random.normal(scale=G[1])/n)])
        print("e=",ε)
    tab.save_table("toy_regression_results.tex",mode='latex')

            
