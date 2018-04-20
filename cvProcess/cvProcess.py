# -*- coding: utf-8 -*-
import math
import numpy
import re
import sys

class cvProcess(object):
    """
    Description: 
        This script read in .txt file generated by CHI electrochemical
        workstation and output data of the last round.
        The result output in file end with _last_round.txt.

    Usage: 
            $ python cvProcess.py file_to_process

    Args:
        file_to_process (str): define which file to process.

    Attributes:
        self.file_to_process (str): define which file to process.
        self.data_raw (numpy.array): store all numerical data.
        self.info (list): info of every process step.
        self.headerlines (int): header lines before numerical data.
    code by zmzeng12 20180415
    """

    def __init__(self, py, file_to_process):
        self.file_to_process = file_to_process
        self.data_raw = []
        self.info = []
        self.headerlines = []
        print('------>  ' + 'The file to process is ' + self.file_to_process)

    def read_file(self):
        """detect headerlines and read numerical data using numpy"""
        with open(self.file_to_process, 'r') as file:
            line = file.readline()
            while line:
                if re.search('[-]*?\d*\.\d*, [-]*?\d\.\d*', line):
                    break
                self.headerlines.append(line)
                line = file.readline()
        self.data_raw = numpy.loadtxt(self.file_to_process, skiprows=len(self.headerlines), delimiter=',', comments='Segment')
        self.data_raw = self.data_raw.T

    def find_last_round(self):
        """the last round is the data from the second last maximum to the last maximum, if there is only
        one maximum found, then output all data"""
        self.sample_interval = math.fabs(self.data_raw[0][0] - self.data_raw[0][1])
        v_max = numpy.max(self.data_raw[0])
        index = len(self.data_raw[0]) -1
        index_last_max = []
        try:
            while index > 0 and len(index_last_max) < 2 :
                if v_max == self.data_raw[0][index]:
                    index_last_max.append(index)
                index -= 1
            self.data_raw = self.data_raw[:, index_last_max[1]:index_last_max[0]+1]
            self.info.append('------>  ' + 'last round found!')
        except IndexError:
            self.info.append('------>  ' + 'There is only one round in the file!')
        self.info.append('------>  ' + 'Vpeak = ' + str(v_max))

    def output_data(self):
        """output data with original headerlines"""
        numpy.savetxt(self.file_to_process[:-4] + "_last_round.txt", self.data_raw.T)

        with open(self.file_to_process[:-4] + "_last_round.txt", 'r') as f:
            lines = f.readlines()

        with open(self.file_to_process[:-4] + "_last_round.txt", 'w') as f:
            f.writelines(self.headerlines)
            f.writelines(lines)

    @property
    def response_info(self):
        return self.info
            
    def main(self):

        self.read_file()
        self.find_last_round()
        self.output_data()
        for i in self.info:
            print(i)

if __name__=='__main__':

    import os

    def get_file(filepath):
        path_dir = os.listdir(filepath)
        all_dir = []
        for every_dir in path_dir:
            child = os.path.join('%s%s' % (filepath, every_dir))
            all_dir.append(child)
        return all_dir

    allDir = get_file('D:/Code/Git/DataProcessing/cvProcess/test/')
    n = 0
    m = 0
    wrong = []
    for everyDir in allDir: 
        print('process.....' + everyDir)
        m += 1
        try:
            test = cvProcess('py', everyDir)
            test.main()
            print('done!')
            n += 1

        except Exception as e:
            print(e)
            wrong.append(everyDir)
    print('success %s/%s'%(n,m))
    with open('wrong.txt','w') as f:
        for i in wrong:
            f.write(i+'\n')

    # test = cvProcess(*sys.argv)
    # test.main()