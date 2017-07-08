
#Uses statistics_generator.py to generate and display statistics based on a data set

import statistics_generator

if __name__ == '__main__':
    filename ="survey_responses_noise_added.txt"
    data = statistics_generator.read_file(filename)

    print("**RACIAL STATS**")
    #black stats
    black_count = statistics_generator.count_matches(data, "race", 1)
    print("Number of blacks is", black_count)
    filtered_blacks_only = statistics_generator.filter_data(data, "race", 1, "=")
    print("Average age of blacks is", statistics_generator.calc_avg(filtered_blacks_only, "age"))
    filtered_less_18 = statistics_generator.filter_data(filtered_blacks_only, "age", 18, "<")
    print("Number of black children is", len(filtered_less_18))
    filtered_black_parents = statistics_generator.filter_data(filtered_blacks_only, "gen", 1, "=")
    print("Number of black parents is", statistics_generator.count_people(filtered_black_parents))


    #white stats
    white_count = statistics_generator.count_matches(data, "race", 0)
    print("Number of whites is", white_count)
    filtered_whites_only = statistics_generator.filter_data(data, "race", 0, "=")
    print("Average age of whites is", statistics_generator.calc_avg(filtered_whites_only, "age"))
    filtered_less_18 = statistics_generator.filter_data(filtered_whites_only, "age", 18, "<")
    print("Number of white children is", len(filtered_less_18))
    filtered_white_parents = statistics_generator.filter_data(filtered_whites_only, "gen", 1, "=")
    print("Number of white parents is", statistics_generator.count_people(filtered_white_parents))


    print("**GENDER STATS**")
    #male stats
    filtered_males = statistics_generator.filter_data(data, "sex", 0, "=")
    male_count = statistics_generator.count_people(filtered_males)
    print("Number of males is", male_count)
    male_avg_age = statistics_generator.calc_avg(filtered_males, "age")
    print("Average age of males is", male_avg_age)

    #female stats
    filtered_females = statistics_generator.filter_data(data, "sex", 1, "=")
    female_count = statistics_generator.count_people(filtered_females)
    print("Number of females is", female_count)
    female_avg_age = statistics_generator.calc_avg(filtered_females, "age")
    print("Average age of females is", female_avg_age)

    print("**GENERATION STATS**")
    #generation stats
    filtered_children = statistics_generator.filter_data(data, "gen", 0, "=")
    child_count = statistics_generator.count_people(filtered_children)
    print("Number of children is", child_count)
    child_avg_age = statistics_generator.calc_avg(filtered_children, "age")
    print("Average age of children is", child_avg_age)
    filtered_male_children = statistics_generator.filter_data(filtered_children, "sex", 0, "=")
    print("Number of male children is", statistics_generator.count_people(filtered_male_children))
    filtered_female_children = statistics_generator.filter_data(filtered_children, "sex", 1, "=")
    print("Number of female children is", statistics_generator.count_people(filtered_female_children))
    print("Average age of male children is", statistics_generator.calc_avg(filtered_male_children, "age"))
    #comes from one person - redact
    #print("Average age of female children is", statistics_generator.calc_avg(filtered_female_children, "age"))

    filtered_parents = statistics_generator.filter_data(data, "gen", 1, "=")
    parent_count = statistics_generator.count_people(filtered_parents)
    print("Number of parents is", parent_count)
    parent_avg_age = statistics_generator.calc_avg(filtered_parents, "age")
    print("Average age of parents is", parent_avg_age)
    filtered_male_parents = statistics_generator.filter_data(filtered_parents, "sex", 0, "=")
    print("Number of male parents is", statistics_generator.count_people(filtered_male_parents))
    filtered_female_parents = statistics_generator.filter_data(filtered_parents, "sex", 1, "=")
    print("Number of female parents is", statistics_generator.count_people(filtered_female_parents))

    filtered_grandparents = statistics_generator.filter_data(data, "gen", 2, "=")
    grandparent_count = statistics_generator.count_people(filtered_grandparents)
    print("Number of grandparents is", grandparent_count)
    grandparent_avg_age = statistics_generator.calc_avg(filtered_grandparents, "age")
    print("Average age of grandparents is", grandparent_avg_age)


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
