# This script takes the results calculated by the script 'extractStatusInformation.sh' or by the script "HEPlot.py"
# This script takes one input argument deciding on the filetype being generated
# 1 - Status information only (Ordered according to instances)
# 2 - Status information only (Ordered according to encodings)

from curses import echo
import os
import sys

from natsort import natsorted

WORKDIR = './results/paper1/experiment1/run1/evaluation'
OUTPUTDIR = WORKDIR + '/mdfiles'

FILETYPE1 = 'status.md'
FILETYPE2 = 'statusV2.md'
FILETYPE1_SUMMARIZED = 'statusSummarized.md'
FILETYPE2_SUMMARIZED = 'statusSummarizedV2.md'

def getStatData(workdir,instance,case):
    inputFilePath = workdir + "/" + instance + "/" + case + "/" + "statInfo.txt"
    with open(inputFilePath, 'r') as inputFile:
        if inputFile.closed:
            print("file can not be opened: " + inputFilePath)
            return
        for line in inputFile:
            terms = line.split(' ')
            return [terms[0], terms[1], terms[2], terms[3], terms[4], terms[5].split(' \ ')[0]]


def getResultData(workdir,instance,case):
    inputFilePath = workdir + "/" + instance + "/" + case + "/" + "results.txt"
    with open(inputFilePath, 'r') as inputFile:
        if inputFile.closed:
            print("file can not be opened: " + inputFilePath)
            return
        line = inputFile.readlines()[-1]
        if "solution" not in line:
            terms = line.split(' ')
            if len(terms) == 3:
                return [terms[1], terms[2].split(' \ ')[0]]
            else:
                return [terms[1], terms[2], terms[3].split(' \ ')[0]]


def resetCount(statusCount):
    statusCount["Unsatisfiable"] = 0
    statusCount["GroundTimeout"] = 0
    statusCount["SolveTimeout"] = 0
    statusCount["SatisfiableTimeout"] = 0
    statusCount["SatisfiableNoTimeout"] = 0


def printSummarizedStati(_section, statusCount, fileType):
    outputPath = OUTPUTDIR + '/' +  fileType

    row = []
    with open(outputPath, 'a') as summarizedOutputfile:
        row.append('|' + _section + '|' + str(statusCount["SatisfiableNoTimeout"]) + '|' + str(statusCount["SatisfiableTimeout"]) + '|' + str(statusCount["SolveTimeout"]) + '|' + str(statusCount["GroundTimeout"]) + '|' + str(statusCount["Unsatisfiable"]))
        summarizedOutputfile.write(''.join(row) + '|\n')


def generateMarkdown(workdir, outputfile, type):
    # Count DSE stati
    statusCount = {}

    instances = {entry.name for entry in os.scandir(workdir) if "." not in entry.name and "mdfiles" not in entry.name}
    instances = natsorted(instances)
    defaultInstance = workdir + "/" + instances[0]

    encodings = { entry.name for entry in os.scandir(defaultInstance) if "uniformScaling" not in entry.name and entry.is_dir() }
    encodings = natsorted(encodings)

    # Prepare md file for summarized results and for averaged results
    if type == '1':
        outputPath = OUTPUTDIR + '/' +  FILETYPE1_SUMMARIZED
        with open(outputPath, 'w') as summarizedOutputfile:
            summarizedOutputfile.write(''.join(['|Instance|SatisfiableNoTimeout|SatisfiableTimeout|SolveTimeout|GroundTimeout|Unsatisfiable|']) + '\n')
            summarizedOutputfile.write(''.join(['|:---:|:---:|:---:|:---:|:---:|:---:|']) + '\n')

    if type == '2':
        outputPath = OUTPUTDIR + '/' +  FILETYPE2_SUMMARIZED
        with open(outputPath, 'w') as summarizedOutputfile:
            summarizedOutputfile.write(''.join(['|Case|SatisfiableNoTimeout|SatisfiableTimeout|SolveTimeout|GroundTimeout|Unsatisfiable|']) + '\n')
            summarizedOutputfile.write(''.join(['|:---:|:---:|:---:|:---:|:---:|:---:|']) + '\n')

    section = ''
    with open(outputfile, 'w') as outputfile:
        if type == '1':           

            for _section in instances: 
                # Reset counter per section
                resetCount(statusCount)
                # Write markdown (sub)header if section/subsection changed since last loop iteration
                if _section != section:
                    section = _section
                    # For each entry in instances, compose a section
                    outputfile.write('# {}\n\n'.format(section))

                # Output status information only (Ordered according to instances)
                if type == '1':
                    # First row contains head of status table
                    outputfile.write(''.join(['|Case|Status|Overall time|Grounding time|Time first solution|Solving time|Eps<1|Eps>1|    |']) + '\n')
                    outputfile.write(''.join(['|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|']) + '\n')

                    # Rows afterwards are made from encodings and corresponding information
                    row = []
                    for case in encodings:
                        statData = getStatData(WORKDIR,_section,case)
                        if(statData[0] == "Unsatisfiable"):
                            row.append('|' + case + '|' + "<span style=\"color: red;\">" + statData[0] + "</span>" + '|' + statData[1] + '|' + statData[2] + '|' + statData[3] + '|' + statData[4] + '|' + "-1" + '|' + "-1\n" )
                            statusCount["Unsatisfiable"] = statusCount["Unsatisfiable"]+1
                        elif(statData[0] == "SolveTimeout" or statData[0] == "GroundTimeout"):
                            row.append('|' + case + '|' + "<span style=\"color: orange;\">" + statData[0] + "</span>" + '|' + statData[1] + '|' + statData[2] + '|' + statData[3] + '|' + statData[4] + '|' + "-1" + '|' + "-1\n")
                            if statData[0] == "SolveTimeout":
                                statusCount["SolveTimeout"] = statusCount["SolveTimeout"]+1
                            else:
                               statusCount["GroundTimeout"] = statusCount["GroundTimeout"]+1
                        elif(statData[0] == "SatisfiableTimeout" or statData[0] == "SatisfiableNoTimeout"):
                            resultData = getResultData(WORKDIR,_section,case)
                            row.append('|' + case + '|' + "<span style=\"color: green;\">" + statData[0] + "</span>" + '|' + statData[1] + '|' + statData[2] + '|' + statData[3] + '|' + statData[4] + '|' + resultData[0] + '|' + resultData[1])
                            if statData[0] == "SatisfiableTimeout":
                                statusCount["SatisfiableTimeout"] = statusCount["SatisfiableTimeout"]+1
                            else:
                               statusCount["SatisfiableNoTimeout"] = statusCount["SatisfiableNoTimeout"]+1

                    outputfile.write(''.join(row))

                    printSummarizedStati(_section, statusCount, FILETYPE1_SUMMARIZED)

        elif type == '2':
            for _section in encodings: 
                # Reset counter per section
                resetCount(statusCount)

                # Write markdown (sub)header if section/subsection changed since last loop iteration
                if _section != section:
                    section = _section
                    # For each entry in encodings, compose a section
                    outputfile.write('# {}\n\n'.format(section))

                # Output status information only (Ordered according to encodings)
                if type == '2':
                    # First row contains head of status table
                    outputfile.write(''.join(['|Instance|Status|Overall time|Grounding time|Time first solution|Solving time|Eps<1|Eps>1|    |']) + '\n')
                    outputfile.write(''.join(['|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|']) + '\n')

                    # Rows afterwards are made from instances and corresponding information
                    row = []
                    for instance in instances:
                        statData = getStatData(WORKDIR,instance,_section)
                        if(statData[0] == "Unsatisfiable"):
                            row.append('|' + instance + '|' + "<span style=\"color: red;\">" + statData[0] + "</span>" + '|' + statData[1] + '|' + statData[2] + '|' + statData[3] + '|' + statData[4] + '|' + "-1" + '|' + "-1\n")
                            statusCount["Unsatisfiable"] = statusCount["Unsatisfiable"]+1
                        elif(statData[0] == "SolveTimeout" or statData[0] == "GroundTimeout"):
                            row.append('|' + instance + '|' + "<span style=\"color: orange;\">" + statData[0] + "</span>" + '|' + statData[1] + '|' + statData[2] + '|' + statData[3] + '|' + statData[4] + '|' + "-1" + '|' + "-1\n")
                            if statData[0] == "SolveTimeout":
                                statusCount["SolveTimeout"] = statusCount["SolveTimeout"]+1
                            else:
                               statusCount["GroundTimeout"] = statusCount["GroundTimeout"]+1
                        elif(statData[0] == "SatisfiableTimeout" or statData[0] == "SatisfiableNoTimeout"):
                            resultData = getResultData(WORKDIR,instance,_section)
                            row.append('|' + instance + '|' + "<span style=\"color: green;\">" + statData[0] + "</span>" + '|' + statData[1] + '|' + statData[2] + '|' + statData[3] + '|' + statData[4] + '|' + resultData[0] + '|' + resultData[1])
                            if statData[0] == "SatisfiableTimeout":
                                statusCount["SatisfiableTimeout"] = statusCount["SatisfiableTimeout"]+1
                            else:
                               statusCount["SatisfiableNoTimeout"] = statusCount["SatisfiableNoTimeout"]+1

                    outputfile.write(''.join(row) + '|\n')

                    printSummarizedStati(_section, statusCount, FILETYPE2_SUMMARIZED)

            outputfile.write('\n')


def main():
    if not os.path.exists(OUTPUTDIR):
        os.makedirs(OUTPUTDIR)

    # Read the input parameter defining the output filetype
    try:
        type = sys.argv[1]
        print("Filetype", type, "has been chosen.")
        if type == '1':
           outputfile = OUTPUTDIR + '/' + FILETYPE1
        elif type == '2':
            outputfile = OUTPUTDIR + '/' + FILETYPE2
        else:
            print("The input parameter didn't match any case")
            sys.exit()
    except:
        print("This script is missing one input parameter\n")
        sys.exit()   
         
    generateMarkdown(WORKDIR, outputfile, type)

if __name__ == '__main__':
    main()
