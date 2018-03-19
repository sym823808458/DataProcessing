# -*- coding: utf-8 -*-

import re, math, sys
import matplotlib.pyplot as plt

class xyz2Distance(object):
    """
    Description: 
        This script read in .xyz file generated by Lammps
        and calculate the distance betweent the specified atom 
        and Ni for every frame.
        The result will be plot and output in file end with _Result.txt.

    Usage: 
            $ python xyz2Distance.py file2Process step2time atom2cal atomRepeat

    Args:
        file2Process (str): define which file to process.
        step2time (int, optional): define how much time in a step. default is 2000step/ps.
        atom2cal (str, optional): atom type to calculate distance between Ni, default is Hf.
        atomRepeat (int, optional): how many atom defined by atom2cal in a frame, default is 24.

    Attributes:
        self.file2Process (str): define which file to process.
        self.step2time (int): define how much time in a step. default is 2000step/ps.
        self.atom2cal (str): atom type to calculate distance between Ni, default is Hf.
        self.atomRepeat (int): how many atom defined by atom2cal in a frame, default is 24.
        self.listOfTime (list)：list of all time data.
        self.listOfatom2cal (list): list of coordinate of atom2cal.
        self.listOfNi (list): list of coordinate of Ni.
        self.listOfDistance (list): list of distance betwent atom2cal and Ni.

    code by zmzeng12 20180303
    add atomRepeat parameter and modified output info by zmzeng12 20180316
    """
    def __init__(self, pyname, file2Process, step2time=2000, atom2cal='Hf', atomRepeat=24):

        print('\n------>  ' + 'The file to process is ' + file2Process )
        print('------>  ' + 'step of time is set to ' + str(step2time))
        print('------>  ' + 'atom is set to ' + atom2cal)
        print('------>  ' + 'atom repeat time is set to ' + str(atomRepeat))
        self.file2Process = file2Process;
        self.listOfTime = []
        self.listOfatom2cal = []
        self.listOfNi = []
        self.listOfDistance = []
        self.step2time = step2time
        self.atom2cal = atom2cal
        self.atomRepeat = atomRepeat

    def readFile(self):
        """read file2Process and put data into related lists.
        """
        file = open(self.file2Process, 'r')
        line = file.readline()
        while line:
            if line.find('Timestep')!=-1:
                Timestep = int(line.split()[2])
                # convert timestep to time
                self.listOfTime.append(Timestep/int(self.step2time))
            elif line.find(self.atom2cal)!=-1: 
                coordinate = [float(i) for i in line.split()[1:4]]
                self.listOfatom2cal.append(coordinate)
            elif line.find('Ni')!=-1:
                coordinate = [float(i) for i in line.split()[1:4]]
                self.listOfNi.append(coordinate)
            line = file.readline()
        file.close()
        print('\n------>  ' +'Number of frames:' + str(len(self.listOfNi)))
        print('------>  ' +'Number of Ni:' + str(len(self.listOfNi)))
        print('------>  ' +'Number of '+ self.atom2cal + ':' + str(len(self.listOfatom2cal)))


    
    def distanceCal(self, atom1, atom2):
        """calculate distance between two atom.
        Args:
            atom1 (list): coordinate of a atom, consists of three float number.
            atom2 (list): same as atom1.
        Returns:
            float, distance between the two coordinate.
        """
        d1 = math.pow(float(atom2[0]) - float(atom1[0]), 2)
        d2 = math.pow(float(atom2[1]) - float(atom1[1]), 2)
        d3 = math.pow(float(atom2[2]) - float(atom1[2]), 2)
        return math.sqrt(d1 + d2 + d3)

    def getDistance(self):
        """get the distance between Ni and the first atom2cal in every frame.
        """
        self.listOfDistance.append(self.distanceCal(self.listOfatom2cal[0], self.listOfNi[0]))
        i=1
        while i < len(self.listOfNi):
            distance = self.distanceCal(self.listOfatom2cal[i*self.atomRepeat], self.listOfNi[i])
            self.listOfDistance.append(distance)
            i += 1

    def outputData(self):
        file = open(self.file2Process[0:-4] + '_Result.txt', 'w')
        file.write('generated by xyz2Distance.py from %s\n' %self.file2Process)
        file.write('Time    Distance (Ni-' + self.atom2cal + ')\n')
        file.write('ps    A\n')
        for time, distance in zip(self.listOfTime, self.listOfDistance):
            file.write(str(time) + '    ' + str(distance) + '\n')
        file.close()
        print('\nall done!\n')
        print('result is stored in ' + self.file2Process[0:-4] + '_Result.txt \n')

    def plotData(self):
        plt.figure('Distance (Ni-' + self.atom2cal + ')')
        plt.plot(self.listOfTime, self.listOfDistance)
        plt.xlabel('Tims (ps)')
        plt.ylabel('Distance (A)')
        plt.title('Distance (Ni-' + self.atom2cal + ')')
        plt.savefig(self.file2Process[0:-4] + '_Distance Ni-' + self.atom2cal + '.png')
        plt.show()

    def main(self):
        self.readFile()
        self.getDistance()
        self.outputData()
        self.plotData()

if __name__=='__main__':

    test = xyz2Distance(*sys.argv)
    test.main()

