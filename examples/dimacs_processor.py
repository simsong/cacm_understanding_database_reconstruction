
#program to convert a .dimacs format CNF file into a form usable by pycoSAT
#reads in a text file and returns a List[List[int]] with extraneous info (comments, p line, 0s) removed
#@author Christian Martindale

FILE_NAME = "demo2.dimacs"

def read_dimacs(filename):
    with open(filename) as f:
        lines = [line.rstrip() for line in f if not line.isspace()]
        return lines

def strings_to_int_list(myList):
    separated = [x.split() for x in myList]
    for i, num in enumerate(separated):
        separated[i] = [int(y) for y in num]
    return separated

#strip comments, strip definition line, strip end of line zeroes, remove empty lines
def process_dimacs(filename):
    initial = read_dimacs(filename)
    only_numbers = [x for x in initial if (x[0] != ("c") and x[0] != ("p") and len(x) != 0)]
    no_empties = [z for z in only_numbers if len(z) != 0]
    to_split_zeroes = " ".join(no_empties)
    split_by_zeroes = to_split_zeroes.split(" 0")
    zeroes_no_spaces = [x.strip(" ") for x in split_by_zeroes]
    remove_nulls = [y for y in zeroes_no_spaces if(y != "" and y!= " ")]
    int_list = strings_to_int_list(remove_nulls)

    return int_list

if __name__ == '__main__':
    print(process_dimacs(FILE_NAME))