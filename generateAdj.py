
import csv

'''
 Parses the input file for calculating the cost of war
 Start Year of War, Total Battle Field Deaths, Year, Per Capita GDP, Adjusted Woman Fertility
'''
def parseFile(file):
    file = open(file, 'rU')
    adjFile = csv.reader(file, delimiter=',')
    
    deaths = {}
    perCapitaGDP = {}
    adjFertility = {}

    for row in adjFile:
        if not deaths.has_key(row[0]):        # If dictionary already contains war year
            deaths[int(row[0])] = 0           # Initialize the death count
        deaths[int(row[0])] += int(row[1])    # Add to death count

        if row[2] is not "":
            perCapitaGDP[int(row[2])] = int(row[3])
            adjFertility[int(row[2])] = float(row[4])

    return deaths, perCapitaGDP, adjFertility

'''
 Calculates total cost of single year of war
 Assuming an average of 25 years more of labor (regardless of age)
 Assuming single generation is 25 years, pretty close to definition
'''
def calc_single_war_cost(year, deaths, capitaGDP, adjFert):
    total = 0.0
    gen = 25
    if year + gen > 2007:
        gen = 2007 - year

    for i in range(0, gen):
        total += capitaGDP[year + i] * deaths

    if (year + 25) < 2007:
        year += 25
        lostBirths = int(float(deaths) * adjFert[year])
        return total + calc_single_war_cost(year, lostBirths, capitaGDP, adjFert)
    return total


'''
 Caluclates the total cost
'''
def calc_total_war_cost(deaths, capitaGDP, adjFert):
    total = 0.0
    yearlyCosts = {}
    for year in deaths:
        totalYear = calc_single_war_cost(year, deaths[year], capitaGDP, adjFert)
        yearlyCosts[year] = totalYear
        total += totalYear
    writeCosts(yearlyCosts)
    return total


'''
 Ouputs the yearly cost in a csv file
'''
def writeCosts(yearlyCost):
    file = open('yearly_adj_war_cost.csv', 'w')
    file.write('Year,Cost of Wars\n')
    for year in yearlyCost:
        file.write(str(year) + ',' + str(yearlyCost[year]) + '\n')

deaths, perCapitaGDP, adjFertility  = parseFile('Adjusted-War-Cost.csv')

totalGDP = calc_total_war_cost(deaths, perCapitaGDP, adjFertility)
print totalGDP






