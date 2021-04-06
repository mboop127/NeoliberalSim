#used to generate populations randomly
import random
import numpy.random as nrandom
import statistics as stats

#used to make graphs
import matplotlib.pyplot as plt

#settings
resources = 10000000000000000000000 #starting global resources
ecological_recovery_rate = 1.2 #1.2 #rate at which resources replenish year to year
parent = [0.00001,0.00001,0.00001] # starting extractiveness, exploitativeness, kindness of capitalists
population_size = 10000 #number of capitalists
distribution = .1 #porportion of wealth given to society
time_limit = 100
societal_resources = 0

time = 0 #starting time

#AI settings
chance = 1
magnitude = .001

def mutate(list):
    for i in range(len(list)):
        if random.random() < chance:
            change = list[i][0] * random.uniform(1-magnitude,1+magnitude)
            list[i][2] -= (change - list[i][0])/2
            list[i][1] -= (change - list[i][0])/2
            list[i][0] = change
        if random.random() < chance:
            change = list[i][1] * random.uniform(1-magnitude,1+magnitude)
            list[i][2] -= (change - list[i][1])/2
            list[i][0] -= (change - list[i][1])/2
            list[i][1] = change
        if random.random() < chance:
            change = list[i][2] * random.uniform(1-magnitude,1+magnitude)
            list[i][1] -= (change - list[i][2])/2
            list[i][0] -= (change - list[i][2])/2
            list[i][2] = change

    return list

#generate AIs
def generate(parent):
    capitalists = []
    for i in range(population_size):
        capitalists.append(parent.copy())

    return capitalists


#graph stuff
resource_list = []
exploitativeness_list = []
extractiveness_list = []
societal_resources_list = []
selflessness_list = []
time_list = []

while time < time_limit and resources > 1:

    capitalists = generate(parent)
    capitalists = mutate(capitalists)

    resources *= ecological_recovery_rate

    score_dictionary = {}
    for i in range(len(capitalists)):
        accumulation = resources * capitalists[i][0] + societal_resources * capitalists[i][1]
        selflessness = accumulation * capitalists[i][2]
        accumulation -= selflessness

        societal_resources += selflessness
        societal_resources -=  societal_resources * capitalists[i][1]

        resources -= (resources * capitalists[i][0])
        resources -= (selflessness)

        score = accumulation
        score_dictionary[accumulation] = i

    best = max(score_dictionary.keys())
    parent = capitalists[score_dictionary[best]].copy()

    resources = max(resources,0)
    societal_resources += resources * distribution
    resources -= resources * distribution

    resource_list.append(resources)
    societal_resources_list.append(societal_resources)
    exploitativeness_list.append(parent[1])
    extractiveness_list.append(parent[0])
    selflessness_list.append(parent[2])
    time_list.append(time)
    time += 1


#fig, ax1 = plt.subplots()

#ax1.plot(time_list,extractiveness_list,exploitativeness_list)

#ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
#
#ax2.plot(time_list, resource_list, societal_resources)
#fig.tight_layout()

plt.plot(time_list,resource_list,societal_resources_list)
plt.legend(['natural resources','societal resources'])
plt.show()

plt.plot(time_list,extractiveness_list,exploitativeness_list)
#plt.plot(time_list,selflessness_list)
plt.legend(['extractiveness','exploitation','selflessness'])
plt.show()
