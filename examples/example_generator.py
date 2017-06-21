import random

#goal is to generate and write arbitrary length file with each line representing a person and his data
#assumptions made: age ranges for generations, household sizes are [2,5], no limitations on unrealistic households
#problem: how to make sure system is satisfiable?
#@author Christian Martindale



def write_to_file(filename, houses_list):
    datafile = open(filename, 'w')
    for household in houses_list:
        for guy in household:
            datafile.write(stringify_person(guy))
            datafile.write("\n")
    datafile.close()

class person(object):
    def __init__(self):
        self.traits = {"id": 0, "hh": 0, "age": 0, "sex": 0, "race": 0, "gen": 0}

def stringify_person(person):
    master_str = ""
    for key in person.traits:
        master_str = master_str + str(person.traits[key]) + " "

    return master_str.strip(" ")

def generate_rand_person(generation):
    me = person()
    me.traits["age"] = 0
    me.traits["gen"] = generation

    if generation == 0: #child
        me.traits["age"] = random.randint(1,17)
    elif generation == 1: #parent
        me.traits["age"] = random.randint(18, 60)
    else:
        me.traits["age"] = random.randint(61, 90)

    me.traits["sex"] = random.randint(0,1)
    me.traits["race"] = random.randint(0,1)

    return me



# generates a list of lists representing a household of people
def generate_household(size, household_id):
    person_list = []
    i = 0
    while i < size:
        next = generate_rand_person(random.randint(0,2))
        next.traits["hh"] = household_id
        person_list.append(next)
        i +=1
    return person_list


# makes master list of person lists, gives IDs to people, used for writing to file
def create_person_array(num_households):
    household_list = []
    i = 0
    while i < num_households:
        household_list.append(generate_household(random.randint(2,5), i + 1))
        i += 1

    id = 1
    for household in household_list:
        for person in household:
            person.traits["id"] = id
            id += 1

    #print(household_list[0][0].traits)
    return household_list


if __name__ == '__main__':
    FILE_NAME = "new_example_survey_responses.txt"
    houses = create_person_array(10)
    write_to_file(FILE_NAME, houses)