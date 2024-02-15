import os
from natsort import natsorted

WORKDIR = 'results/paper1/experiment2'
OUTPUT_FILE = 'results/paper1/experiment2'

class StatInfo():
    def __init__(self):
        self.overallTime_ = []
        self.groundTime_ = []
        self.timeFirstSolution_ = []
        self.solvingTime_ = []
        self.number_points_ = []

        self.number_of_data_sets = 0

    def read_and_store_data_of_file(self, filepath):
        with open(filepath, 'r') as inputFile:
            if inputFile.closed:
                print("file can not be opened: " + filepath)
                return

            terms = inputFile.readline().rsplit(' ')
            try:
                self.overallTime_.append(float(terms[1]))
                self.groundTime_.append(float(terms[2]))
                self.timeFirstSolution_.append(float(terms[3]))
                self.solvingTime_.append(float(terms[4]))
                self.number_points_.append(float(terms[5]))

                self.number_of_data_sets += 1
            except ValueError:
                print("data could not be parsed on: " + filepath)
                return -1  # Error parsing time

    def print_average_data_on_file(self, filepath):
        with open(filepath, 'w') as outputFile:
            if outputFile.closed:
                print("file can not be opened: " + filepath)
                return
            if self.number_of_data_sets != 5:
                print("Warning, less than 5 runs have been analyzed")

            outputFile.write("overallTime groundTime timeFirstSolution solvingTime numberOfDesignPoints\n")
            if self.number_of_data_sets == 0:
                print("no data to print")
                return

            outputFile.write(str(sum(self.overallTime_) / self.number_of_data_sets) + ' '
                             + str(sum(self.groundTime_) / self.number_of_data_sets) + ' '
                             + str(sum(self.timeFirstSolution_) / self.number_of_data_sets) + ' '
                             + str(sum(self.solvingTime_) / self.number_of_data_sets) + ' '
                             + str(sum(self.number_points_) / self.number_of_data_sets) + '\n')
    def calculate_stdev(self, list):
        average = sum(list) / self.number_of_data_sets
        y = sum((x - average) ** 2 for x in list)
        stdev = (y / self.number_of_data_sets) ** 0.5
        return stdev

    def print_stdev_data_on_file(self, filepath):
        with open(filepath, 'w') as outputFile:
            if outputFile.closed:
                print("file can not be opened: " + filepath)
                return
            if self.number_of_data_sets != 5:
                print("Warning, less than 5 runs have been analyzed")

            outputFile.write("overallTime groundTime timeFirstSolution solvingTime numberOfDesignPoints\n")
            if self.number_of_data_sets == 0:
                print("no data to print")
                return

            outputFile.write(str(self.calculate_stdev(self.overallTime_)) + ' '
                             + str(self.calculate_stdev(self.groundTime_)) + ' '
                             + str(self.calculate_stdev(self.timeFirstSolution_)) + ' '
                             + str(self.calculate_stdev(self.solvingTime_)) + ' '
                             + str(self.calculate_stdev(self.number_points_)) + '\n')
class Result():
    def __init__(self):
        self.epsilonSmallerOne_ = []
        self.epsilonBiggerOne_ = []

        self.number_of_data_sets_ = 0

    def read_and_store_data_of_file(self, filepath):
        with open(filepath, 'r') as inputFile:
            if inputFile.closed:
                print("file can not be opened: " + filepath)
                return

            try:
                for readline in inputFile:  # read only last line
                    pass
                terms = readline.rsplit(' ')
                self.epsilonSmallerOne_.append(float(terms[1]))
                self.epsilonBiggerOne_.append(float(terms[2]))
                self.number_of_data_sets_ += 1
            except:
                print("data could not be parsed on: " + filepath)
                return

    def calculate_stdev(self, list):
        average = sum(list) / self.number_of_data_sets_
        y = sum((x - average) ** 2 for x in list)
        stdev = (y / self.number_of_data_sets_) ** 0.5
        return stdev

    def print_average_data_on_file(self, filepath):
        with open(filepath, 'w') as outputFile:
            if outputFile.closed:
                print("file can not be opened: " + filepath)
                return
            if self.number_of_data_sets_ != 5:
                print("Warning, less than 5 runs have been analyzed")

            outputFile.write("epsilonSmallerOne epsilonBiggerOne\n")
            if self.number_of_data_sets_ != 0:
                outputFile.write(str(sum(self.epsilonSmallerOne_) / self.number_of_data_sets_) + ' '
                                 + str(sum(self.epsilonBiggerOne_) / self.number_of_data_sets_) + '\n')


    def print_stdev_data_on_file(self, filepath):
        with open(filepath, 'w') as outputFile:
            if outputFile.closed:
                print("file can not be opened: " + filepath)
                return
            if self.number_of_data_sets_ != 5:
                print("Warning, less than 5 runs have been analyzed")

            outputFile.write("epsilonSmallerOne epsilonBiggerOne\n")
            if self.number_of_data_sets_ != 0:
                outputFile.write(str(self.calculate_stdev(self.epsilonSmallerOne_)) + ' '
                                 + str(self.calculate_stdev(self.epsilonBiggerOne_)) + '\n')

def main(workdir, outputdir):
    try:
        runs = {entry.name for entry in os.scandir(workdir) if entry.is_dir() and "run" in entry.name}
        runs = natsorted(runs)
        reference_run = runs[0]
    except:
        print("no 'run' folders found in given path")
        return

    cases = {entry.name for entry in os.scandir(workdir + '/' + reference_run + '/evaluation') if "mdfiles" not in entry.name}
    cases = natsorted(cases)
    for case in cases:
        grids = {entry.name for entry in os.scandir(workdir + '/' + reference_run + '/evaluation/' + case)}
        grids = natsorted(grids)
        for grid in grids:
            statinfo = StatInfo()
            result = Result()
            for run in runs:  # read all files
                info_file_path = workdir + '/' + run + '/evaluation/' + case + '/' + grid + '/statInfo.txt'
                result_file_path = workdir + '/' + run + '/evaluation/' + case + '/' + grid + '/results.txt'
                statinfo.read_and_store_data_of_file(info_file_path)
                result.read_and_store_data_of_file(result_file_path)

            # write data to the output directory
            output_info_file_path_avg = outputdir + '/average/' + case + '/' + grid + '/statInfo.txt'
            output_result_file_path_avg = outputdir + '/average/' + case + '/' + grid + '/results.txt'
            output_info_file_path_stdev = outputdir + '/deviation/' + case + '/' + grid + '/statInfo.txt'
            output_result_file_path_stdev = outputdir + '/deviation/' + case + '/' + grid + '/results.txt'

            os.makedirs(os.path.dirname(output_info_file_path_avg), exist_ok=True)
            os.makedirs(os.path.dirname(output_result_file_path_avg), exist_ok=True)
            os.makedirs(os.path.dirname(output_info_file_path_stdev), exist_ok=True)
            os.makedirs(os.path.dirname(output_result_file_path_stdev), exist_ok=True)

            statinfo.print_average_data_on_file(output_info_file_path_avg)
            result.print_average_data_on_file(output_result_file_path_avg)

            statinfo.print_stdev_data_on_file(output_info_file_path_stdev)
            result.print_stdev_data_on_file(output_result_file_path_stdev)


if __name__ == '__main__':
    main(WORKDIR, OUTPUT_FILE)
