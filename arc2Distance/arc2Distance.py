### Description: this script read in .arc file generated by Gulp
###              and calculate the distance betweent Zr-Ni for every
###              frame.
### Usage: python arc2Distance.py file.arc
### code by zmzeng12 20180202, refactor at 20180228

#coding :utf-8

import re, math, sys

class arc2Distance(object):

    def __init__(self, file2Process):
        print('\nThe file to process is ' + file2Process +'\n')
        self.file2Process = file2Process;
        self.listOfTime = []
        self.listOfZr = []
        self.listOfNi = []
        self.listOfDistance = []

    # get all Time and Zr, Ni coordinate in list
    def readFile(self):
        print('Read file...'+'\n')
        file = open(file2Process, 'r')
        line = file.readline()
        while line:
            if line.find('ps')!=-1:
                self.listOfTime.append(line.split()[0])
            elif line.find('ZR1')!=-1: 
                self.listOfZr.append(line.split()[1:4])
            elif line.find('NI1')!=-1:
                self.listOfNi.append(line.split()[1:4])
            line = file.readline()
        file.close()
        print('Number of frames:' + str(len(self.listOfNi)) +'\n')

    # difine distance Calculator
    def distanceCal(self, atom1, atom2):
        # get distance 
        d1 = math.pow(float(atom2[0]) - float(atom1[0]), 2)
        d2 = math.pow(float(atom2[1]) - float(atom1[1]), 2)
        d3 = math.pow(float(atom2[2]) - float(atom1[2]), 2)
        return str(math.sqrt(d1 + d2 + d3))

    # get the distance between Ni and the first Zr atom
    # There are 12 Zr and 1 Ni atoms in the structure of every time step
    def getDistance(self):
        print('Calculating distance...'+'\n')
        self.listOfDistance.append(self.distanceCal(self.listOfZr[0], self.listOfNi[0]))
        i=1
        while i < len(self.listOfTime):
            distance = self.distanceCal(self.listOfZr[i+11], self.listOfNi[i])
            self.listOfDistance.append(distance)
            i += 1

    # output all data
    def outputData(self):
        file = open(self.file2Process[0:-4] + '_Result.txt', 'w')
        file.write('Time    Distance(Ni-Zr)\n')
        for time, distance in zip(self.listOfTime, self.listOfDistance):
            file.write(time + '    ' + distance + '\n')
        file.close()
        print('all done!')
        print('result is stored in ' + self.file2Process[0:-4] + '_Result.txt \n')

    # conver arc to distance!
    def convert(self):
        self.readFile()
        self.getDistance()
        self.outputData()

if __name__=='__main__':

    file2Process = sys.argv[1];

    test = arc2Distance(file2Process)
    test.convert()

