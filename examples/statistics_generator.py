# -*- coding: utf-8 -*-
import example_generator


#reads in a file of PII data and generates statistics for mock publication
#input format:
    # 1 CATEGORIES
    # 2-N each line represents a person, data values are ints separated by spaces

#Categories (update as new categories are added):
categories = {"id":0, "hh": 1, "age":2, "sex":3, "race":4, "gen":5}


def read_file(filename):
    with open(filename) as f:
        lines = [line.rstrip() for line in f if not line.isspace()]
        return lines[1:]

#counts the number of people in the file matching a description
def count_matches(data, param_name, value):
    ans = 0
    for line in data:
        person = line.split()
        if int(person[categories[param_name]]) == value:
            ans += 1
    return ans

if __name__ == '__main__':
    filename ="example_survey_responses.txt"
    data = read_file(filename)
    param_name = "race"
    value = 1
    count = count_matches(data, param_name, value)
    print("Number of", param_name, "with value", value, "is", count)