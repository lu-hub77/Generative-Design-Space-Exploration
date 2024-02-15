# This script calculates the epsilon dominance and the diversity (#TODO) for the Pareto-optimal front of each DSE run (per case and instance)

import os
import time
from natsort import natsorted
import ctypes

OUTPUT_BASE_DIR = './results/paper1/experiment1/run1/evaluation'
OUTPUT_FILE_NAME = 'results.txt'
DESIGN_POINTS_FILE_NAME = 'designPoints.txt'

SOLUTION_STRING = 'solution'
EPSILON_STRING1 = 'epsilonSmallerOne'
EPSILON_STRING2 = 'epsilonLargerOne'
DIVERSITY_STRING = 'diversity'

class ARRAY(ctypes.Structure):
    _fields_ = [("length", ctypes.c_int), ("content", ctypes.POINTER(ctypes.POINTER(ctypes.c_double)))]

# Call C++ functionality as a library
cppLib = ctypes.cdll.LoadLibrary('./scripts/evaluation/qualityIndicators/epsilonDominance2.so')


def parse_data(inputLine):
    terms = inputLine.split(' ')
    for i in range(len(terms)):
        if "\n" in terms[i]:
            terms[i] = terms[i].replace('\n', '')

    return terms


def parse_solution_no_line(line):
    terms = line.split(' ')
    try:
        solution_no = int(terms[1])
    except ValueError:
        return -1  # Error parsing solution_no

    return solution_no


def parse_time_line(line):
    terms = line.split(' ')
    answerNumber = terms[1]
    time = terms[4]

    try:
        float(time)
    except ValueError:
        return [-1, "-1"] # Error parsing time

    if not answerNumber.isnumeric(): # Error parsing answer number
        return [-1, "-1"]

    return [int(answerNumber), time]


def translate_solution_line_to_ASP(line):
    line = line.replace("\n", ".\n")
    line = line.replace(" ", ".\n")

    return line


def get_maximum_value(vector,entry):
    max = 0.0
    for i in vector:
        if float(i[entry]) > max:
            max = float(i[entry])

    return max


def get_average_value(vector,entry):
    average = 0.0
    if len(vector) > 0:
        for i in vector :
            average = average + float(i[entry])
        average = average / len(vector)

    return average
                        

# Evaluation of the not dominated design points in a given vector
def get_pareto_front_from_vector(inputVector):
    frontNotDominated = []

    for i in inputVector:
        dominated = False
        for j in inputVector:
            if i[0]==j[0]:
                continue
            if int(i[1]) >= int(j[1]) and int(i[2]) >= int(j[2]) and int(i[3]) >= int(j[3]) :
                dominated = True
                break
        if dominated == False:
            frontNotDominated.append(i)

    return frontNotDominated


# Identify the not dominated Pareto front
# Functionality is called from a C++ library, which initializes as well as concatenates the vectors and does the dominance check
def get_pareto_front_from_path(inputPath):
    # Prepare usage of function from C++ library
    cppLib.initializeVector.restype = ARRAY
    referenceFrontArray = cppLib.initializeVector(bytes(inputPath, 'utf-8'))

    print("Received reference front:")
    for i in range(referenceFrontArray.length):
        print(str(referenceFrontArray.content[i][0]) + " " + str(referenceFrontArray.content[i][1]) + " " + str(referenceFrontArray.content[i][2]))

    return referenceFrontArray


def calculate_epsilon_dominance(inputPath, referenceFront):
    epsilonSmallerOne = -1.0
    epsilonLargerOne = -1.0

    solutionNumber = -1
    solutionDesignPoint = []
    resultDictionary = {}

    inputFilePath = inputPath + "/designPoints.txt"

    with open(inputFilePath, 'r') as inputFile:
        if inputFile.closed:
            print("file can not be opened: " + inputFilePath)
            return

        # Read values of each design point from input file
        for line in inputFile:
            # Skip first line in file
            if SOLUTION_STRING in line:
                continue
            # Get data per entry in file
            terms = parse_data(line)
            solutionNumber = terms[0]

            # Extent list of design points step by step
            # Every list element is an array with 3 ctypes.c_double values
            solutionDesignPoint.append( (ctypes.c_double * 3)() )
            solutionDesignPoint[-1][0] = ctypes.c_double(float(terms[1]))
            solutionDesignPoint[-1][1] = ctypes.c_double(float(terms[2]))
            solutionDesignPoint[-1][2] = ctypes.c_double(float(terms[3]))

            # Prepare approximatedFrontArray, which is input to epsilon dominance calculation
            # approximatedFront is an array where each element is a pointer to one design point (array of 3 ctypes.c_double values)
            # Casting is needed to remove information of length of array from pointer type and to only receive pointer to first element of array  
            approximatedFront = (ctypes.POINTER(ctypes.c_double)*len(solutionDesignPoint))()
            for i in range(len(solutionDesignPoint)):
                solutionDesignPointPointer = ctypes.pointer(solutionDesignPoint[i])
                solutionDesignPointPointer = ctypes.cast(solutionDesignPointPointer,ctypes.POINTER(ctypes.c_double))
                approximatedFront[i] = solutionDesignPointPointer
            # approximatedFrontPointer is a pointer to the first element of the array approximatedFront
            approximatedFrontPointer = ctypes.pointer(approximatedFront)
            approximatedFrontPointer = ctypes.cast(approximatedFrontPointer,ctypes.POINTER(ctypes.POINTER(ctypes.c_double)))

            # Build approximatedFrontArray
            approximatedFrontArray = ARRAY()
            approximatedFrontArray.length = ctypes.c_int(len(approximatedFront))
            approximatedFrontArray.content = approximatedFrontPointer

            # Calculate two kind of epsilon dominance: I(Pareto,Approximation) < 1 and I(Approximation,Pareto) > 1
            cppLib.epsilonDominance.argtypes = (ARRAY,ARRAY)
            cppLib.epsilonDominance.restype = ctypes.c_double
            epsilonSmallerOne = cppLib.epsilonDominance(referenceFront,approximatedFrontArray)
            epsilonLargerOne = cppLib.epsilonDominance(approximatedFrontArray,referenceFront)

            # Save result connected to solutionNumber
            resultDictionary[solutionNumber] = [epsilonSmallerOne, epsilonLargerOne]

        return resultDictionary

    # # Read from output file and add values of new results (2x epsilon dominance) to each line (regarding the solutionNumber)
    # lines = []
    # with open(outputFilePath, 'r') as outputFile:
    #     if outputFile.closed:
    #         print("file can not be opened: " + outputFilePath)
    #         return
    #     for line in outputFile:
    #         # Skip first line in file
    #         if SOLUTION_STRING in line:
    #             lines.append(line)
    #             continue
    #         terms = parse_data(line)
    #         line = ""
    #         # Skip the last values, because they are exchanged with the new values
    #         # Nicer way: range(len(terms)) (when script started from scratch) or range(len(terms)-2) (when epsilon dominance values have been already written to output file in a previous run)
    #         for i in range(8):
    #             line = line + str(terms[i]) + " "
    #         line = line + str(resultDictionary[terms[0]][0]) + " " + str(resultDictionary[terms[0]][1]) + "\n"
    #         lines.append(line)

    # # Write adapted content to output file
    # with open(outputFilePath, 'w') as outputFile:
    #     if outputFile.closed:
    #         print("file can not be opened: " + outputFilePath)
    #         return
    #     for line in lines:
    #         outputFile.write(line)


def main():

    instances = {entry.name for entry in os.scandir(OUTPUT_BASE_DIR) if entry.is_dir() and entry.name != "mdfiles"}
    instances = natsorted(instances)

    for instance in instances:
        casesPath = OUTPUT_BASE_DIR + '/' + instance
        cases = { entry.name for entry in os.scandir(casesPath) if entry.is_dir()}
        cases = natsorted(cases)

        # Get the Pareto front from all design points of all cases
        referenceFront = get_pareto_front_from_path(casesPath)

        for case in cases:
            epsilonDictionary = calculate_epsilon_dominance(casesPath + "/" + case, referenceFront)

            outputFilePath = casesPath + "/" + case + "/" + OUTPUT_FILE_NAME

            with open(outputFilePath, 'w') as outputFile:
                if outputFile.closed:
                    print("file can not be opened: " + outputFilePath)
                    return
                    
                # Write header of the file
                outputFile.write(SOLUTION_STRING + ' ' + EPSILON_STRING1 + ' ' + EPSILON_STRING2 + ' ' + DIVERSITY_STRING + '\n')

                for key in epsilonDictionary:
                    outputFile.write(str(key) + " " + str(epsilonDictionary[key][0]) + " " + str(epsilonDictionary[key][1]) + '\n')

        # Free the memory used by C++ library
        cppLib.freeVector(referenceFront)

    exit(0)

    #TODO Calculate and output diversity metric
    #TODO Check for obsolete functions and variables


if __name__ == '__main__':
    main()
    