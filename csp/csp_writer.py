#writes csp formatted files

def write(filename, n):
    f = open(filename, 'w')
    write_hh(f, n)
    write_age(f, n)
    write_sex(f, n)
    write_race(f, n)
    write_gen(f, n)
    f.close()

def write_hh(file, num):
    for i in range(1, num+1):
        file.write("(int H" + str(i) + " 1 10)")
        file.write("\n")

def write_age(file, num):
    for i in range(1, num+1):
        file.write("(int A" + str(i) + " 1 90)")
        file.write("\n")

def write_sex(file, num):
    for i in range(1, num+1):
        file.write("(int S" + str(i) + " 0 1)")
        file.write("\n")

def write_race(file, num):
    for i in range(1, num+1):
        file.write("(int R" + str(i) + " 0 1)")
        file.write("\n")

def write_gen(file, num):
    for i in range(1, num+1):
        file.write("(int G" + str(i) + " 0 2)")
        file.write("\n")

if __name__ == '__main__':
    write("encoded_stats.csp", 35)