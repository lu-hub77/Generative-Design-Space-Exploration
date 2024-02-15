# This script allows to execute the different GDSE approaches

import glob
import os
import sys

# Inputs parameter
# Read the input parameter defining the output filetype
try:
    run = sys.argv[1]
    print("Run number ", run)
except:
    print("This script is missing one input parameter\n")
    sys.exit()   

##########################
#### Define all paths ####
##########################

base_dir                    = os.getcwd()
# Benchmark Instance = Application Graph + Architecture Template + Resource Library + Generated Mapping Options + Information from Preprocessing
instance_dir                = base_dir + "/instances"
instance_taskgraph_dir      = instance_dir + "/taskGraph"           #  Application graph, generated mapping options, information from preprocessing
instance_architecture_dir   = instance_dir + "/gridArchitecture"    # Constraints on architecture template
instance_library_dir        = instance_dir + "/resourceLibrary"     # Resource library
# Encodings & Tools
preprocessing_dir           = base_dir + "/encodings/preprocessing"
encoding_dir                = base_dir + "/encodings"
dse_source_dir              = base_dir + "/src"
clingo_call                 = "clingo "
background_theory_call      = "python " + dse_source_dir + "/dseApp.py "
runlim_call                 = "../runlim-master/runlim -s 100000 -t 3600 "            # Set space limit (-s) and timeout (-t)
synthesis_allocation_call   = encoding_dir + "/allocation/allocation.lp "
# For binding 3 approaches are implemented (encoding)
# Encoding 1 and 2, each consists of partitioning (part a) and positioning (part b) encoding
# Some parts have two versions of encoding: Version one (depending on dynamic grounding) vs. Version two (Depending on static grounding + integrity constraint)
synthesis_binding_dir       = encoding_dir + "/binding"
# Selection of encoding for the binding
synthesis_binding_call      = synthesis_binding_dir + "/3_simpleGuessing.lp "
synthesis_routing_call      = encoding_dir + "/routing/encoding_hop_bound.lp "   # or encoding_hop_arb or encoding_xyz
synthesis_scheduling_call   = encoding_dir + "/scheduling/encoding_scheduling.lp " + encoding_dir + "/scheduling/priorities.lp "
synthesis_optimization_call = encoding_dir + "/preferences.lp "
template_constraints_call   = encoding_dir + "/routing/interconnection.lp "
show_call                   = encoding_dir + "/showDSE.lp "


#################################################
#### Get components from benchmark instances ####
#################################################

def extractSpecificFile(ending, library_name, taskgraph_name, taskgraph_dir):
    files = [ name for name in glob.glob(taskgraph_dir + "/*") 
                    if name.endswith(library_name + ending) and taskgraph_name in name ]
    if len(files) > 1:
        sys.exit("Too many files for task graph " + taskgraph_name + " found.")
    if len(files) == 0:
        sys.exit("No files for task graph " + taskgraph_name + " found.")
    return files[0]

def generatePreprocessingInformation(taskgraph_path, taskgraph_name, architecture_path, architecture_name, library_path, library_name, mappingOptions_path, preprocessing_path, output_path):
    preprocessing_file = output_path + "/" + taskgraph_name + "_" + architecture_name + "_" + library_name + "_preprocessed.lp"
    preprocessing_call = clingo_call + preprocessing_path + "/* " + taskgraph_path + " " + architecture_path + " " + library_path + " " + mappingOptions_path + " " + "-V0 --out-ifs='\n' --out-atomf=%s. | head -n -1 > " + preprocessing_file

    print("Preprocessing done. File saved at " + preprocessing_file)
    os.system(preprocessing_call)

    return preprocessing_file

architectures = glob.glob(instance_architecture_dir + "/*")
libraries = glob.glob(instance_library_dir + "/*")
taskgraphs = [ name for name in glob.glob(instance_taskgraph_dir + "/*") 
              if not name.endswith("Types.lp") and not name.endswith("preprocessed.lp") ]

###################
#### Execution ####
###################

print("Experiment 1")

## First: Iterate over all architectures with a fixed library
library = "library4Types.lp"
library_name = library[7:-3] 

for taskgraph in taskgraphs:

    taskgraph_name = os.path.basename(taskgraph)[:-3]
    mappingOptions = extractSpecificFile(".lp", library_name, taskgraph_name, instance_taskgraph_dir) 

    # Output path
    results_dir = "results/experiment1/run" + run + "/" + taskgraph_name

    try:
        os.makedirs(results_dir)
        print("Directory '%s' created successfully" % results_dir)
    except:
        print("Directory '%s' can not be created" % results_dir) 

    for architecture in architectures:
        architecture_name = os.path.basename(architecture)[:-3]
        preprocessingInformation = generatePreprocessingInformation(taskgraph, taskgraph_name, architecture, architecture_name, instance_library_dir + "/" + library, library_name, mappingOptions, preprocessing_dir, instance_taskgraph_dir)
        instance =  (taskgraph + " " +
                    mappingOptions + " " + 
                    preprocessingInformation + " " + 
                    architecture + " " + 
                    instance_library_dir + "/" + library + " ")
        
        # Output files
        runlim_file = results_dir + "/" + architecture_name + ".runlim_watcher "
        result_file = results_dir + "/" + architecture_name + ".lp "
        error_file  = results_dir + "/" + architecture_name + ".error "

        # Finally the instance execution
        print("###############################################")
        print("Next instance: " + instance)
        
        encoding_call = runlim_call + "-o " + runlim_file + background_theory_call + instance + synthesis_allocation_call + synthesis_binding_dir + "/3_simpleGuessing.lp " + synthesis_routing_call + synthesis_scheduling_call + synthesis_optimization_call + template_constraints_call + show_call + "-q > " + result_file + "2> " + error_file
        os.system(encoding_call)
        #input("Output ok?")

print("Experiment 2")

## Second Iterate over all libraries with a fixed architecture
architecture = "grid2_2_1.lp"
architecture_name = architecture[0:-3]

for taskgraph in taskgraphs:

    taskgraph_name = os.path.basename(taskgraph)[:-3]

    # Output path
    results_dir = "results/experiment2/run" + run + "/" + taskgraph_name
    try:
        os.makedirs(results_dir)
        print("Directory '%s' created successfully" % results_dir)
    except:
        print("Directory '%s' can not be created" % results_dir)

    for library in libraries:

        library_name = os.path.basename(library)[7:-3]
        mappingOptions = extractSpecificFile(".lp", library_name, taskgraph_name, instance_taskgraph_dir) 
        preprocessingInformation = generatePreprocessingInformation(taskgraph, taskgraph_name, instance_architecture_dir + "/" + architecture, architecture_name, library, library_name, mappingOptions, preprocessing_dir, instance_taskgraph_dir)

        instance =  (taskgraph + " " +
                    mappingOptions + " " + 
                    preprocessingInformation + " " + 
                    instance_architecture_dir + "/" + architecture + " " + 
                    library + " ")

        # Output files
        runlim_file = results_dir + "/" + library_name + ".runlim_watcher "
        result_file = results_dir + "/" + library_name + ".lp "
        error_file  = results_dir + "/" + library_name + ".error "

        # Finally the instance execution
        print("###############################################")
        print("Next instance: " + instance)

        encoding_call = runlim_call + "-o " + runlim_file + background_theory_call + instance + synthesis_allocation_call + synthesis_binding_dir + "/3_simpleGuessing.lp " + synthesis_routing_call + synthesis_scheduling_call + synthesis_optimization_call + template_constraints_call + show_call + "-q > " + result_file + "2> " + error_file
        os.system(encoding_call)
        #input("Output ok?") 

    
sys.exit()
