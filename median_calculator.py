import statistics
import tytable

MEDIAN=30
MEAN=44

if __name__=="__main__":
    tt = tytable.ttable()
    tt.add_variable("mymedian",MEDIAN)
    tt.add_variable("mymean",MEAN)
    tt.add_head(['a','b','c'])
    count = 0
    considered = 0
    for a in range(1,115):
        for b in range(a,115):
            for c in range(b,115):
                mean = statistics.mean([a,b,c])
                median = statistics.median([a,b,c])
                considered += 1
                if median==MEDIAN and mean==MEAN:
                    tt.add_data([a,b,c])
                    count += 1
    tt.add_variable("myconsidered",considered)
    tt.add_variable("mycount",count)
    tt.set_caption("The {} possible ages for which the median is {} and the mean is {}".format(count,MEDIAN,MEAN))
    tt.set_label("medians")
    tt.add_option(tytable.OPTION_TABLE)
    tt.add_option(tytable.OPTION_CENTER)

    with open("medians.tex","w") as f:
        f.write(tt.typeset(mode=tytable.LATEX))


