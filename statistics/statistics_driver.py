
#Uses statistics_generator.py to generate and display statistics based on a data set

import statistics_generator

if __name__ == '__main__':
    filename ="example_survey_responses.txt"
    data = statistics_generator.read_file(filename)

    print("**RACIAL STATS**")
    #black stats
    black_count = statistics_generator.count_matches(data, "race", 1)
    print("Number of blacks is", black_count)
    filtered_blacks_only = statistics_generator.filter_data(data, "race", 1, "=")
    print("Average age of blacks is", statistics_generator.calc_avg(filtered_blacks_only, "age"))
    filtered_less_18 = statistics_generator.filter_data(filtered_blacks_only, "age", 18, "<")
    print("Number of blacks under 18 is", len(filtered_less_18))
    filtered_black_parents = statistics_generator.filter_data(filtered_blacks_only, "gen", 1, "=")
    print("Number of black parents is", statistics_generator.count_people(filtered_black_parents))


    #white stats
    white_count = statistics_generator.count_matches(data, "race", 0)
    print("Number of whites is", white_count)
    filtered_whites_only = statistics_generator.filter_data(data, "race", 0, "=")
    print("Average age of whites is", statistics_generator.calc_avg(filtered_whites_only, "age"))
    filtered_less_18 = statistics_generator.filter_data(filtered_whites_only, "age", 18, "<")
    print("Number of whites under 18 is", len(filtered_less_18))
    filtered_white_parents = statistics_generator.filter_data(filtered_whites_only, "gen", 1, "=")
    print("Number of white parents is", statistics_generator.count_people(filtered_white_parents))


    print("**GENDER STATS**")
    #male stats
    filtered_males = statistics_generator.filter_data(data, "sex", 0, "=")
    male_count = statistics_generator.count_people(filtered_males)
    print("Number of males is", male_count)
    male_avg_age = statistics_generator.calc_avg(filtered_males, "age")

    #female stats
    filtered_females = statistics_generator.filter_data(data, "sex", 1, "=")
    female_count = statistics_generator.count_people(filtered_females)
    print("Number of females is", female_count)
    female_avg_age = statistics_generator.calc_avg(filtered_females, "age")


    print("**MISCELLANEOUS STATS**")
    #misc stats
    num_people = statistics_generator.count_people(data)
    print("Total number of people is", num_people)
    num_children = statistics_generator.count_matches(data, "gen", 0)
    print("Total number of children is", num_children)
    num_parents = statistics_generator.count_matches(data, "gen", 1)
    print("Total number of parents is", num_parents)
    num_gparents = statistics_generator.count_matches(data, "gen", 2)
    print("Total number of grandparents is", num_gparents)

    average_age = statistics_generator.calc_avg(data, "age")
    print("Average age is", average_age)
    average_hh_size = statistics_generator.calc_avg_hh_size(data)
    print("Average household size is", average_hh_size)
