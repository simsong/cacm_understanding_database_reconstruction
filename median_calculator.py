import statistics
import tytable

MEDIAN=30
MEAN=44

if __name__=="__main__":
    count = 0
    considered = 0
    rows = []
    for a in range(1,115):
        for b in range(a,115):
            for c in range(b,115):
                mean = statistics.mean([a,b,c])
                median = statistics.median([a,b,c])
                considered += 1
                if median==MEDIAN and mean==MEAN:
                    rows.append([a,b,c])
                    count += 1
    # Now build a multicolumn table
    COLUMNS = 3

    tt = tytable.ttable()
    tt.add_variable("mymedian",MEDIAN)
    tt.add_variable("mymean",MEAN)

    tt.add_head(['a','b','c'] * COLUMNS)
    total_rows = len(rows)
    for i in range(total_rows//COLUMNS):
        row = []
        for col in range(0,3):
            offset = (total_rows * col)//COLUMNS + i
            if offset < len(rows):
                row += rows[offset]
            else:
                row += ['']*len(rows[0])
        tt.add_data(row)
    tt.set_latex_colspec('|'.join(['rrr'] * COLUMNS))
    tt.add_variable("myconsidered",considered)
    tt.add_variable("mycount",count)
    tt.set_caption("The {} possible ages for which the median is {} and the mean is {}".format(count,MEDIAN,MEAN))
    tt.set_label("medians")
    tt.add_option(tytable.OPTION_TABLE)
    tt.add_option(tytable.OPTION_CENTER)

    with open("medians.tex","w") as f:
        f.write(tt.typeset(mode=tytable.LATEX))


