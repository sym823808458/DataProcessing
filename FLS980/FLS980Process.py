# -* coding:utf-8 *-
import numpy
import sys

class FLS980Process(object):
    """
    Description: 
        This script read in .txt file generated by FLS980
        and output all data normalized according to the maximum.
        The result output in file end with _Result.txt.

    Usage: 
            $ python FLS980Process.py file_to_process

    Args:
        file_to_process (str): define which file to process.

    Attributes:
        self.file_to_process (str): define which file to process.
        self.data_raw (numpy.array): store all numerical data.
        self.max (float): maximum value of all data.

    code by zmzeng12 20180323
    """
    def __init__(self, file_to_process):
        super(FLS980Process, self).__init__()
        self.file_to_process = file_to_process
        self.data_raw = []
        self.max = 0.0

    def read_file(self):
        self.data_raw = numpy.loadtxt(self.file_to_process, skiprows=3)
        self.data_raw = self.data_raw.T

    def find_max(self):
        self.max = self.data_raw[1][0]
        for i in range(1, len(self.data_raw)):
            for j in range(0, len(self.data_raw[i])):
                if self.max < self.data_raw[i][j]:
                    self.max = self.data_raw[i][j]

    def normalize_data(self):
        """value_normalized = value_original / maximum"""
        for i in range(1, len(self.data_raw)):
            self.data_raw[i] = self.data_raw[i] / self.max

    def output_data(self):
        """save data after normalization with headlines"""
        numpy.savetxt(self.file_to_process[:-4] + "_result.txt", self.data_raw.T)

        with open(self.file_to_process[:-4] + "_result.txt", 'r') as f:
            lines = f.readlines()

        with open(self.file_to_process, 'r') as f:
            headline = []
            headline.append(f.readline())
            f.readline()
            headline_temp = f.readline().replace('Ex1 ', '', 40)
            headline.append(headline_temp.replace('nm', '', 40))
            headline.append('\n')

        with open(self.file_to_process[:-4] + "_result.txt", 'w') as f: 
            f.writelines(headline)
            f.writelines(lines)
        
    def main(self):

        self.read_file()
        self.find_max()
        self.normalize_data()
        self.output_data()

if __name__ == '__main__':
    for i in range(1,len(sys.argv)):
        print('\n------>Now process ' + sys.argv[i])
        test = FLS980Process(sys.argv[i])
        test.main()
    input('\n------>all done!')


