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
    def __init__(self,incomes,grades):
        # Set up the graph and draw the raw data
        self.incomes = incomes
        self.grades = grades
    
    def add_data(self,income,grade,color='yellow',markersize=25,markertext=None):
        """Add a value and plot it"""
        self.incomes.append(income)
        self.grades.append(grade)
        plt.plot([income],[grade],color=color,marker='o',markersize=markersize)
        if markertext:
            plt.annotate(markertext, xy=(income,grade),
                         horizontalalignment='center', verticalalignment='center')

    def plot_data(self):
        plt.clf()               # clear the figure
        plt.title("Parent incomes vs. student grade")
        plt.plot(self.incomes, self.grades, color='orange', marker='o', linestyle='')

    def topcode(self,topcode=None):
        if topcode:
            self.incomes = [min(inc,topcode) for inc in self.incomes]

    def regress(self,prec=None,topcode=None,linecolor='k',linestyle='solid'):
        # Perform the regression, round the parameters (if requested), and
        # and draw the curve
        self.topcode(topcode)
        self.fit = np.polyfit(self.incomes,self.grades,1)
        fit_fn = np.poly1d(self.fit)
        if prec:
            self.fit = [round_places(x,prec=prec) for x in self.fit]
        linex = [0, max(self.incomes)]
        liney = fit_fn(linex)
        legend = "y = {}x + {}".format(self.fit[0],self.fit[1])
        if topcode:
            legend += " (topcode={:,})".format(topcode)
        # Plot the regression line and save the legend
        plt.plot(linex, liney, color=linecolor,
                 linestyle=linestyle,label=legend)
            
    def savefig(self,fname):
        # Graph using the parameters
        plt.xlim(-1000, max(self.incomes) * 1.05) # make it a little bigger than needed
        plt.ylim(-5,105)
        plt.legend(loc='lower center',fontsize=9)
        plt.xticks(rotation=20)
        plt.axes().get_xaxis().set_major_formatter(
            mp.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
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
    e.plot_data()
    e.regress()
    e.savefig("toy_regression.pdf")
    true_fit = copy.deepcopy(e.fit)

    # Now show the 4 regressions with a point the explores the state space

    # Now make a rounded version to 4 significant digits:
    g = copy.deepcopy(e)
    g.regress(prec=4,topcode=topcode,linecolor='red')

    # This is bogus; why isn the last value not being plotted somtimes?
    plt.plot([g.incomes[-1]], [g.grades[-1]], color='orange', marker='o')
    g.savefig("toy_regression_rounded.pdf")

    # Now we are going to create the
    e.topcode(topcode)
    e.plot_data()               # replot the data
    e.regress(topcode=topcode,prec=4,linestyle='-',linecolor='black')

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
            g.add_data(inc,gr,color=linecolors[i],markertext=str(i+1),markersize=15)
            g.regress(topcode=topcode,prec=4,linestyle='--',linecolor=linecolors[i])
            fit_values.append(g.fit)
            i += 1
                     
    g.savefig("toy_regression_bounds.pdf")

    G = []
    for i in range(0,2):
        values = [fit_value[i] for fit_value in fit_values]
        G.append(max(values) - min(values))

    tab.add_variable("Gzero",round_places(G[0],8))
    tab.add_variable("Gone", round_places(G[1],8))
    tab.save_table("toy_regression_extreme_data.tex",mode='latex')

    # Now let's show what adding noise looks like, at different values of epsilon
    n = len(income)
    tab = ttable()
    tab.append_head(['epsilon','true n','true $b_1$','true $b_0$',
                     'reported n','reported $b_1$','reported $b_0$'])
    tab.set_col_fmt(0,"","%2.1f","") # epsilon
    tab.set_col_fmt(2,"","%4.3e","") # b_1
    tab.set_col_fmt(3,"","%4.1f","") # b_0
    tab.set_col_fmt(5,"","%4.3e","") # b_1
    tab.set_col_fmt(6,"","%4.1f","") # b_0
    for ε in np.arange(0.2,4.0,.2):
        tab.append_data([ε, n, true_fit[0], true_fit[1],
                         int(n + np.random.normal(scale=1)/n),
                         round_places(true_fit[0] + np.random.normal(scale=G[0])/n),
                         round_places(true_fit[1] + np.random.normal(scale=G[1])/n)])
    tab.save_table("toy_regression_results.tex",mode='latex')

            
