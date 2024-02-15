#!/bin/bash

# From experimental results, this script is extracting all relevant status information for the evaluation afterwards
# These information are stored in files which are used by the script markdownGenerator.py later on

BASE_DIR="${PWD}/results/paper1/experiment2/run1"
OUTPUT="${BASE_DIR}/evaluation"
CASES="${BASE_DIR}"

# Organize the folder structure
echo "###############################################################"
echo "Get the name of the encodings and create folders for them"
echo "Get the name of the cases and create folders for them"
echo "###############################################################"

instances=( $( find ${CASES} -type f | grep ".lp" ) )
for instance in ${instances[@]}
do 
    instanceName=$( echo ${instance} | rev | cut -d/ -f2 | rev )
    architectureName=$( echo ${instance} |cut -d. -f1 | rev | cut -d/ -f1 | rev )

    # Check if directory exists, if not found create it
    [ ! -d "${OUTPUT}/${instanceName}" ] && mkdir -p "${OUTPUT}/${instanceName}"

    # Check if sub-directory exists, if not found create it
    [ ! -d "${OUTPUT}/${instanceName}/${architectureName}" ] && mkdir -p "${OUTPUT}/${instanceName}/${architectureName}"

    # Check if output files exist, if not found create them
    if [[ ! -f "${OUTPUT}/${instanceName}/${architectureName}/statInfo.txt" ]]; then
        > "${OUTPUT}/${instanceName}/${architectureName}/statInfo.txt"
    fi
    if [[ ! -f "${OUTPUT}/${instanceName}/${architectureName}/designPoints.txt" ]]; then
        > "${OUTPUT}/${instanceName}/${architectureName}/designPoints.txt"
    fi
    if [[ ! -f "${OUTPUT}/${instanceName}/${architectureName}/results.txt" ]]; then
        > "${OUTPUT}/${instanceName}/${architectureName}/results.txt"
    fi
done

cd ${CASES}
echo "###############################################################"
echo "Extract statistical information"
echo "###############################################################"
statusType1=$( grep -r -d recurse -l -m1 Answer * )     # Satisfiable
statusType2=$( grep -d recurse -l UNSAT * )             # Unsatisfiable
statusType3a=$( grep -d recurse -l UNKNOWN * )          # Interrupted while Grounding
statusType3b=$( grep -d recurse -L 'Answer\|UNSAT\|UNKNOWN\|NoneType' * | grep ".lp" ) # Interrupted before Searching (so also while Grounding)
statusType4=$( grep -d recurse -l NoneType * )          # Interrupted while Solving
statusType5=$( grep -d recurse "Pareto front:" * | grep -v "Approximate" | cut -d: -f 1 ) # Satisfiable before timeout

timeout=3600
timeFirstAnswer=-1

# Output will be the following: Status OverallTimeSpend GroundingTime TimeToFirstSolution SolvingTime ModelsFound

# The unsuccessful DSEs (type 2-4) get the default information
for type2 in ${statusType2[@]}
do
    instanceName=( $( echo ${type2} | cut -d/ -f1 ) )
    architectureName=( $( echo ${type2} | cut -d. -f1 | cut -d/ -f2 ) )

    overallTime=( $( cat ${type2} | grep "Solving:" | cut -d: -f2 | cut -d" " -f2 | rev | cut -ds -f2 | rev ) )
    solvingTime=( $( cat ${type2} | grep "Solving:" | cut -d: -f3 | cut -d" " -f2 | rev | cut -ds -f2 | rev ) )

    groundTime=$(echo $overallTime - $solvingTime | bc -l)

    echo "Unsatisfiable" ${overallTime} ${groundTime} ${timeFirstAnswer} ${solvingTime} "0" > ${OUTPUT}/${instanceName}/${architectureName}/statInfo.txt
done

for type3a in ${statusType3a[@]}
do
    instanceName=( $( echo ${type3a} | cut -d/ -f1 ) )
    architectureName=( $( echo ${type3a} | cut -d. -f1 | cut -d/ -f2 ) )

    echo "GroundTimeout" ${timeout} ${timeout} ${timeFirstAnswer} "-1" "0" > ${OUTPUT}/${instanceName}/${architectureName}/statInfo.txt
done

for type3b in ${statusType3b[@]}
do
    instanceName=( $( echo ${type3b} | cut -d/ -f1 ) )
    architectureName=( $( echo ${type3b} | cut -d. -f1 | cut -d/ -f2 ) )

    echo "GroundTimeout" ${timeout} ${timeout} ${timeFirstAnswer} "-1" "0" > ${OUTPUT}/${instanceName}/${architectureName}/statInfo.txt
done

for type4 in ${statusType4[@]}
do
    instanceName=( $( echo ${type4} | cut -d/ -f1 ) )
    architectureName=( $( echo ${type4} | cut -d. -f1 | cut -d/ -f2 ) )

    overallTime=( $( cat ${type4} | grep "Solving:" | cut -d: -f2 | cut -d" " -f2 | rev | cut -ds -f2 | rev ) )
    solvingTime=( $( cat ${type4} | grep "Solving:" | cut -d: -f3 | cut -d" " -f2 | rev | cut -ds -f2 | rev ) )

    groundTime=$(echo $overallTime - $solvingTime | bc -l)

    echo "SolveTimeout" ${timeout} ${groundTime} ${timeFirstAnswer} ${solvingTime} "0" > ${OUTPUT}/${instanceName}/${architectureName}/statInfo.txt
done

# First type DSE has found answers, so we extract the searching time up to the first answer and the number of found design points
for type1 in ${statusType1[@]}
do
    instanceName=( $( echo ${type1} | cut -d/ -f1 ) )
    architectureName=( $( echo ${type1} | cut -d. -f1 | cut -d/ -f2 ) )

    #timeFirstAnswer=( $(cat ${type1} | grep "Answer 1 found after" | cut -d" " -f5) ) # Version for runlim tool
    timeFirstAnswer=( $( cat ${type1} | grep "Solving:" | cut -d: -f4 | cut -d" " -f2 | rev | cut -ds -f2 | rev ) )

    #numberDesignPoints=( $(cat ${type1} | grep "found after" | tail -1 | cut -d" " -f2) ) # Version for runlim tool

    overallTime=( $( cat ${type1} | grep "Solving:" | cut -d: -f2 | cut -d" " -f2 | rev | cut -ds -f2 | rev ) )
    solvingTime=( $( cat ${type1} | grep "Solving:" | cut -d: -f3 | cut -d" " -f2 | rev | cut -ds -f2 | rev ) )

    groundTime=$(echo $overallTime - $solvingTime | bc -l)

    # If entry is also of type5, we extract the searching time
    check=0
    for type5 in ${statusType5[@]}
    do
        if [[ "${type5}" == "${type1}" ]]; then
            numberDesignPoints=( $(grep "Models" $type1 | cut -d: -f2 | cut -c2- ) )
            echo "SatisfiableNoTimeout" ${overallTime} ${groundTime} ${timeFirstAnswer} ${solvingTime} ${numberDesignPoints} > ${OUTPUT}/${instanceName}/${architectureName}/statInfo.txt
            check=1
        fi
    done
    if [[ $check == 0 ]]; then
        numberDesignPoints=( $(grep "Models" $type1 | cut -d: -f2 | cut -c2- | rev | cut -c2- | rev) )
        echo "SatisfiableTimeout" ${timeout} ${groundTime} ${timeFirstAnswer} ${solvingTime} ${numberDesignPoints} > ${OUTPUT}/${instanceName}/${architectureName}/statInfo.txt
    fi
done

cd ${BASE_DIR}
