
#program to convert a .dimacs format CNF file into a form usable by pycoSAT
#reads in a text file and returns a List[List[int]] with extraneous info (comments, p line, 0s) removed
#@author Christian Martindale

FILE_NAME = "demo1.dimacs"

def read_dimacs(filename):
    with open(filename) as f:
        lines = [line.rstrip() for line in f]
        return lines

def strings_to_int_list(myList):
    separated = [x.split() for x in myList]
    for i, num in enumerate(separated):
        separated[i] = [int(y) for y in num]
    return separated

#strip comments, strip definition line, strip end of line zeroes, remove empty lines
def process_dimacs(filename):
    initial = read_dimacs(filename)
    only_numbers = [x for x in initial if (x[0] != ("c") and x[0] != ("p"))]
    no_zeroes = [y[:-1] for y in only_numbers]
    no_empties = [z for z in no_zeroes if len(z) != 0]

    int_list = strings_to_int_list(no_empties)

    return int_list

if __name__ == '__main__':
    print(process_dimacs(FILE_NAME))