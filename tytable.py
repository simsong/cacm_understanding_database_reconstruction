"""ttable.py:
Module for typesetting tables in ASCII, LaTeX, and HTML.  Perhaps even CSV!
Also creates LaTeX variables.

Simson Garfinkel, 2010-

This is really bad python. Let me clean it up before you copy it.

"""

TEXT  = 'text'
LATEX = 'latex'
HTML  = 'html'
LONGTABLE='longtable'
OPTION_TABLE = 'table'
OPTION_CENTER = 'center'


#
# Some basic functions
#

def isnumber(v):
    """Return true if we can treat v as a number"""
    try:
        return v==0 or v!=0
    except TypeError:
        return False

def latex_var(name,value,desc=None,xspace=True):
    """Create a variable NAME with a given VALUE.
    Primarily for output to LaTeX.
    Returns a string."""
    xspace_str = r"\xspace" if xspace else ""
    return "".join(['\\newcommand{\\',str(name),'}{',str(value),xspace_str,'}'] + ([' % ',desc] if desc else []) + ['\n'])

def text_var(name,value,desc=None):
    """Create a variable NAME with a given VALUE.
    Primarily for output to LaTeX.
    Returns a string."""
    return "".join(['Note: ',str(name),' is ',str(value)] + ([' (',desc,')'] if desc else []))

def icomma(i):
    """ Return an integer formatted with commas """
    if i<0:   return "-" + icomma(-i)
    if i<1000:return "%d" % i
    return icomma(i/1000) + ",%03d" % (i%1000)

# hr is the tag that we use for linebreaks 

class row:
    def __init__(self,data):
        self.data = data
    def __len__(self):
        return len(self.data)
    def __getitem__(self,n):
        return self.data[n]

class subhead(row):
    def __init__(self,val):
        self.data  = [val]
        self.text  = val

class raw(row):
    def __init__(self,data):
        self.data = data
    

class ttable:
    """ Python class that prints formatted tables. It can also output LaTeX.
    Typesetting:
       Each entry is formatted and then typset.
       Formatting is determined by the column formatting that is provided by the caller.
       Typesetting is determined by the typesetting engine (text, html, LaTeX, etc).
       Numbers are always right-justified, text is always left-justified, and headings
       are center-justified.

       ## Data building functions:
       ttable() - Constructor. 
       .set_title(title) 
       .compute_col_totals(col_totals) - adds columns for specified columns
       add_head([row]) to one or more heading rows. 
       add_data([row]) to append data rows. 
       add_data(ttable.HR) - add a horizontal line

       ## Formatting functions:
       set_col_alignment(col,align) - where col=0..maxcols and align=ttable.RIGHT or ttable.LEFT or ttable.CENTER
                                (center is not implemented yet)
       set_col_totals([1,2,3,4]) - compute totals of columns 1,2,3 and 4

       ## Outputting
       typeset(mode=[TEXT,HTML,LATEX]) to typeset. returns table
       save_table(fname,mode=)
       add_variable(name,value)  -- add variables to output (for LaTeX mostly)
       set_latex_colspec(str)    -- sets the LaTeX column specification, rather than have it auto calculated
    """
    HR = "<hr>"
    SUPPRESS_ZERO="suppress_zero"
    RIGHT="RIGHT"
    LEFT="LEFT"
    CENTER="CENTER"
    NL = {TEXT:'\n', LATEX:"\\\\ \n", HTML:''} # new line
    VALID_MODES = set([TEXT,LATEX,HTML])
    VALID_OPTIONS = set([LONGTABLE,SUPPRESS_ZERO,OPTION_TABLE])
    DEFAULT_ALIGNMENT_NUMBER = RIGHT
    DEFAULT_ALIGNMENT_STRING = LEFT
    HTML_ALIGNMENT = {RIGHT:"style='text-align:right;'",
                      LEFT:"style='text-align:left;'",
                      CENTER:"style='text-align:center;'"}

    def __init__(self):
        self.col_headings = []          # the col_headings; a list of lists
        self.data         = []          # the raw data; a list of lists
        self.omit_row     = []          # descriptions of rows that should be omitted
        self.col_widths   = []          # a list of how wide each of the formatted columns are
        self.col_margin   = 1
        self.col_fmt_default  = "{:,}"  # default format gives numbers
        self.col_fmt      = {}          # format for each column
        self.title        = ""
        self.num_units    = []
        self.footer       = ""
        self.header       = None # 
        self.heading_hr_count = 1       # number of <hr> to put between heading and table body
        self.options      = set()
        self.col_alignment = {}
        self.variables    = {}  # additional variables that may be added
        self.label        = None
        self.caption      = None

    ## Data adding functions

    ## User specified formatting functions:
        
    def set_mode(self,mode):
        assert mode in self.VALID_MODES
        self.mode = mode
    def add_option(self,o): self.options.add(o)
    def set_data(self,d): self.data = d
    def set_title(self,t): self.title = t
    def set_label(self,l): self.label = l
    def set_footer(self,footer): self.footer = footer
    def set_caption(self,c): self.caption = c
    def set_col_alignment(self,col,align): self.col_alignment[col] = align
    def set_col_totals(self,totals): self.col_totals = totals
    def set_col_fmt(self,col,fmt):
        """Set the formatting for colum COL. Format is specified with a Python format string.
        You can create a prefix and suffix by putting them on either side of the formatter.
        e.g. prefix{:,}suffix.
        """
        self.col_fmt[col] = fmt
    def set_latex_colspec(self,latex_colspec):
        self.latex_colspec = latex_colspec

    def add_head(self,values):
        """ Append a row of VALUES to the table header. The VALUES should be a list of columsn."""
        assert type(values)==type([]) or type(values)==type(())
        self.col_headings.append(values)

    def add_data(self,values):
        """ Append a ROW to the table body. The ROW should be a list of each column."""
        self.data.append(row(values))

    def add_subhead(self,values):
        self.data.append(subhead(values))

    def add_raw(self,val):
        self.data.append(raw(val))

    def ncols(self):
        " Return the number of maximum number of cols in the data"
        return max([len(r) for r in self.data])


    ################################################################

    def format_cell(self,value,colNumber):
        """ Format a value that appears in a given colNumber. The first column Number is 0.
        Returns (value,alignment)
        """
        formatted_value = None
        if value==None:
            return ("",self.LEFT)
        if value==0 and self.SUPPRESS_ZERO in self.options:
            return ("",self.LEFT)
        if isnumber(value):
            try:
                formatted_value   = self.col_fmt.get(colNumber, self.col_fmt_default).format(value)
                default_alignment = self.DEFAULT_ALIGNMENT_NUMBER
            except ValueError:
                pass            # will be formatted below
        if not formatted_value:
            formatted_value   = str(value)
            default_alignment = self.DEFAULT_ALIGNMENT_STRING 
        return (formatted_value, self.col_alignment.get(colNumber, default_alignment))

    def col_formatted_width(self,colNum):
        " Returns the width of column number colNum "
        maxColWidth = 0
        for r in self.col_headings:
            try:
                maxColWidth = max(maxColWidth, len(self.format_cell(r[colNum],colNum)[0]))
            except IndexError:
                pass
        for r in self.data:
            try:
                maxColWidth = max(maxColWidth, len(self.format_cell(r[colNum],colNum)[0]))
            except IndexError:
                pass
        return maxColWidth

    ################################################################

    def typeset_hr(self):
        "Output a HR."
        if self.mode==LATEX:
            return "\\hline\n "
        elif self.mode==TEXT:
            return "+".join(["-"*self.col_formatted_width(col) for col in range(0,self.cols)]) + "\n"
        elif self.mode==HTML:
            return ""                   # don't insert
        raise ValueError("Unknown mode '{}'".format(self.mode))        

    def typeset_cell(self,formattedValue,colNumber):
        "Typeset a value for a given column number."
        import math
        align = self.col_alignment.get(colNumber,self.LEFT)
        if self.mode==HTML: return formattedValue
        if self.mode==LATEX: return formattedValue
        if self.mode==TEXT: 
            try:
                fill = (self.col_formatted_widths[colNumber]-len(formattedValue))
            except IndexError:
                fill=0
            if align==self.RIGHT:
                return " "*fill+formattedValue
            if align==self.CENTER:
                return " "*math.ceil(fill/2.0)+formattedValue+" "*math.floor(fill/2.0)
            # Must be LEFT
            if colNumber != self.cols-1: # not the last column
                return formattedValue + " "*fill
            return formattedValue               #  don't indent last column


    def typeset_row(self,row):
        "row is a an array. It should be typset. Return the string. "
        ret = []
        if isinstance(row,raw):
            return row[0]
        if isinstance(row,subhead):
            # Do a blank line
            if self.mode==TEXT:
                ret.append("\n")
                ret.append(r.text)
            elif self.mode==LATEX:
                ret.append("\\\\\n")
                ret.append(r.text)
            elif self.mode==HTML:
                ret.append('<tr><th colspace={} class="subhead">{}</th></tr>'.format((self.cols,row.text)))
            ret.append(self.NL[self.mode])
            return "".join(ret)

        if self.mode==HTML:
            ret.append("<tr>")
        for colNumber in range(0,len(row)):
            if colNumber > 0:
                if self.mode==LATEX:
                    ret.append(" & ")
                ret.append(" "*self.col_margin)
            (fmt,just)      = self.format_cell(row[colNumber],colNumber)
            val             = self.typeset_cell(fmt,colNumber)

            if self.mode==TEXT:
                ret.append(val)
            elif self.mode==LATEX:
                ret.append(val.replace('%','\\%'))
            elif self.mode==HTML:
                ret.append('<{} {}>{}</{}>'.format(self.html_delim,
                                                   self.HTML_ALIGNMENT[just],
                                                   val,
                                                   self.html_delim))
        if self.mode==HTML:
            ret.append("</tr>")
        ret.append(self.NL[self.mode])
        return "".join(ret)
        

    ################################################################

    def calculate_col_formatted_widths(self):
        " Calculate the width of each formatted column and return the array "
        self.col_formatted_widths = []
        for i in range(0,self.cols):
            self.col_formatted_widths.append(self.col_formatted_width(i))
        return self.col_formatted_widths

    def should_omit_row(self,r):
        if r.data==self.HR: return True
        for (a,b) in self.omit_row:
            if r[a]==b: return True
        return False

    def compute_col_totals(self,col_totals):
        " Add totals for the specified cols"
        self.cols = self.ncols()
        totals = [0] * self.cols
        for r in self.data:
            if self.should_omit_row(r):
                continue
            for col in col_totals:
                totals[col] += r[col]
        row = ["Total"]
        for col in range(1,self.cols):
            if col in col_totals:
                row.append(totals[col])
            else:
                row.append("")
        self.add_data(self.HR)
        self.add_data(row)

    ################################################################
    def typeset_headings(self):
        #
        # Typeset the headings
        #
        ret = []
        if self.mode==HTML:
            self.html_delim = 'th'
        if self.col_headings:
            for heading_row in self.col_headings:
                ret.append(self.typeset_row(heading_row))
            for i in range(0,self.heading_hr_count):
                ret.append(self.typeset_hr())
        return ret
        
    def typeset(self,mode=TEXT,option=None):
        """ Returns the typset output of the entire table. Builds it up in """

        self.set_mode(mode)
        print("option=",option)
        if option:
            self.add_option(option)
            print("add option",option)
        self.cols = self.ncols() # cache
        if self.mode not in [TEXT,LATEX,HTML]:
            raise ValueError("Invalid typsetting mode "+self.mode)

        ret = [""]              # array of strings that will be concatenatted

        # Precalc any table widths if necessary 
        if self.mode==TEXT:
            self.calculate_col_formatted_widths()
            if self.title: ret.append(self.title + ":" + "\n")

        #
        # Start of the table 
        #
        if self.mode==LATEX:
            try:
                colspec = self.latex_colspec
            except AttributeError:
                colspec = "r"*self.cols 
            if LONGTABLE not in self.options:
                if OPTION_TABLE in self.options:
                    ret.append("\\begin{table}")
                if OPTION_CENTER in self.options:
                    ret.append("\\begin{center}")
                if LONGTABLE not in self.options:
                    if self.caption: ret += ["\\caption{",self.caption, "}\n"]
                    if self.label:
                        ret.append("\\label{")
                        ret.append(self.label)
                        ret.append("}")
                ret += ["\\begin{tabular}{",colspec,"}\n"]
                ret += self.typeset_headings()
            if LONGTABLE in self.options:
                ret += ["\\begin{longtable}{",colspec,"}\n"]
                ret += self.typeset_headings()
                ret.append("\\endfirsthead\n")
                ret += self.typeset_headings()
                ret.append("\\endhead\n")
                ret.append(self.footer)
                ret.append("\\endfoot\n")
                ret.append(self.footer)
                ret.append("\\endlastfoot\n")
        elif self.mode==HTML:
            ret.append("<table>\n")
            ret += self.typeset_headings()
        elif self.mode==TEXT:
            if self.header:
                ret.append(self.header)
                ret.append("\n")
            ret += self.typeset_headings()


        #
        # typeset each row.
        # computes the width of each row if necessary
        #
        if self.mode==HTML:
            self.html_delim = 'td'

        for row in self.data:

            # See if we should omit this row
            if self.should_omit_row(row):
                continue

            # See if this row demands special processing
            if row.data==self.HR:
                ret.append(self.typeset_hr())
                continue

            ret.append(self.typeset_row(row))

            # If we need to calculate col totals, do that.
            # This should be redone elsewhere
            if hasattr(self,"col_totals"):
                for col in self.col_totals:
                    totals[col] += row[col]

        if self.mode==LATEX:
            if LONGTABLE not in self.options:
                ret.append("\\end{tabular}\n")
                if OPTION_CENTER in self.options:
                    ret.append("\\end{center}")
                if OPTION_TABLE in self.options:
                    ret.append("\\end{table}")
            else:
                ret.append("\\end{longtable}\n")
        elif self.mode==HTML:
            ret.append("</table>\n")
        elif self.mode==TEXT:
            if self.footer:
                ret.append(self.footer)
                ret.append("\n")
            
        # Finally, add any variables that have been defined
        for (name,value) in self.variables.items():
            if self.mode==LATEX:
                ret += latex_var(name,value)
            if self.mode==HTML:
                ret += ["Note: ",name," is ", value, "<br>"]
        print(ret)
        return "".join(ret)

    def add_variable(self,name,value):
        self.variables[name] = value

    def save_table(self,fname,mode=LATEX,option=None):
        with open(fname,"w") as f:
            f.write(self.typeset(mode=mode,option=option))
