# From experimental results, this script is extracting all design points (cost, latency, energy for each answer) from the resulting Pareto front
# These information are stored in files which are used by the script calculateIndicators.py later on

import os
from natsort import natsorted

OUTPUT_BASE_DIR = './results/paper1/experiment2/run1/evaluation'
OUTPUT_FILE_NAME = 'designPoints.txt'
INPUT_BASE_DIR = './results/paper1/experiment2/run1'

SEARCH_DATA_STRING = 'Answer '
LATENCY_STRING = 'latency'
ENERGY_STRING = 'energy'
COST_STRING = 'cost'
SOLUTION_STRING = 'solution'


def get_data_from_string(string):
    content = string.split('(')[1].split(')')[0]  # Keep only content within brackets.
    content = content.split(',')[2]
    try:
        int(content)
    except :
        return "-1"  # Error parsing time
    return str(int(content))


def parse_solution_number_line(line):
    terms = line.rsplit(' ',1)
    try:
        solution = int(terms[1])
    except ValueError:
        return -1  # Error parsing time
    return solution


def parse_solution_line(line):
    terms = line.split(' ')
    latency = -1
    energy = -1
    cost = -1

    for term in terms:
        if LATENCY_STRING in term:
            latency = get_data_from_string(term)
        if ENERGY_STRING in term:
            energy = get_data_from_string(term)
        if COST_STRING in term:
            cost = get_data_from_string(term)
    return [latency, energy, cost]

            
def write_design_points(instance, case, inputFilePath):

    # Remove '.txt' from file name
    case = case.split('.')[0]

    outputFilePath = OUTPUT_BASE_DIR + '/' + instance + '/' + case + '/' + OUTPUT_FILE_NAME

    # solutions [ solution, cost, latency, energy ]
    solutions = []

    with open(inputFilePath, 'r') as inputFile:
        if inputFile.closed:
            print("file can not be opened: " + inputFilePath)
            return

        with open(outputFilePath, 'w') as outputFile:
            if outputFile.closed:
                print("file can not be opened: " + outputFilePath )
                return

            # Write header in the output file
            outputFile.write(SOLUTION_STRING + ' ' + LATENCY_STRING + ' ' + ENERGY_STRING + ' ' + COST_STRING + '\n')

            for line in inputFile:
                solutionNumber = -1
                solutionData = -1

                ## Extract data from output file of the DSE ##
                # Check if line contains an answer
                if SEARCH_DATA_STRING in line:
                    solutionNumber = parse_solution_number_line(line)
                    solutionData = parse_solution_line(next(inputFile))
                    if solutionNumber == -1 or -1 in solutionData:
                        print("Warning, unexpected value in :" + inputFilePath)
                        continue

                # Store the values in the list "solutions"
                if solutionNumber != -1:
                    while len(solutions) < int(solutionNumber):
                        solutions.append([solutionNumber, "-1", "-1", "-1"])

                    solutions[solutionNumber - 1][0] = solutionNumber

                    solutions[solutionNumber - 1][1] = solutionData[0]
                    solutions[solutionNumber - 1][2] = solutionData[1]
                    solutions[solutionNumber - 1][3] = solutionData[2]

            # When all solutions have been read, print them on the file
            for solution in solutions:
                outputFile.write(str(solution[0]) + ' ' + solution[1] + ' ' + solution[2] + ' ' + solution[3] + '\n')

def main():
    
    instances = {entry.name for entry in os.scandir(INPUT_BASE_DIR) if entry.is_dir() and entry.name != "evaluation" }
    instances = natsorted(instances)

    for instance in instances:
        cases = {entry.name for entry in os.scandir(INPUT_BASE_DIR + '/' + instance) if ".lp" in entry.name }
        cases = natsorted(cases)

        for case in cases:
            filePath = INPUT_BASE_DIR + '/' + instance + '/' + case
            write_design_points(instance, case, filePath)
    
    exit(0)


if __name__ == '__main__':
    main()