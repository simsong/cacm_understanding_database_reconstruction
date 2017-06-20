# -*- coding: utf-8 -*-
import example_generator


#reads in a file of PII data and generates statistics for mock publication
#input format:
    # 1 categories (in order)
    # 2-N each line represents a person, data values are ints separated by spaces

#Categories (update as new categories are added):
categories = {"id":0, "hh": 1, "age":2, "sex":3, "race":4, "gen":5}


def read_file(filename):
    with open(filename) as f:
        lines = [line.rstrip() for line in f if not line.isspace()]
        return lines[1:]

#just for readability's sake later
def count_people(data):
    return len(data)

#creates a list with only people matching the filter criteria in it
def filter_data(data, param_name, value):
    filtered = []
    for line in data:
        person = line.split()
        if int(person[categories[param_name]]) == value:
            filtered.append(line)
    return filtered

#counts the number of people in the file matching a description
def count_matches(data, param_name, value):
    ans = 0
    for line in data:
        person = line.split()
        if int(person[categories[param_name]]) == value:
            ans += 1
    return ans

#calculates the percent of people matching criteria 2 that also match 
#criteria 1
def calc_percent(data, param_name_1, value_1, param_name_2, value_2):
    numerator = count_matches(param_name_1, value_1)
    denominator = count_matches(param_name_2, value_2)
    return numerator / denominator
    
#calculates the average value of a trait in a certain population
def calc_avg(filtered_data, param_name):
    population_size = len(filtered_data)
    running_total = 0
    for line in filtered_data:
        person = line.split()
        running_total += int(person[categories[param_name]])
    return running_total / population_size

if __name__ == '__main__':
    filename ="example_survey_responses.txt"
    data = read_file(filename)
    param_name = "race"
    race_value = 1
    count = count_matches(data, param_name, race_value)
    print("Number of people with", param_name, "value", race_value, "is", count)
    filtered_whites_only = filter_data(data, "race", 1)
    print("Average age of whites is", calc_avg(filtered_whites_only, "age"))