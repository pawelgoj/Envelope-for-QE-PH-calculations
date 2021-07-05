# -*- coding: utf-8 -*-
"""
Created on Sun Mar 14 23:16:18 2021

@author: pagoj
"""
import math as math
from typing import Tuple
import scipy.special as special
import scipy.stats as stats
import numpy as np
import matplotlib.pyplot as plt

#Plots the strand positions calculated from QE on the graph
def int_bonds(x, y, intensity):
    y = np.zeros(len(y))
    j = 0
    
    for i in range(0, len(x) -2):
        if j > (len(intensity) -1):
            break
        else:
            if (x[i] <= intensity[j][0]) and (intensity[j][0] <= x[i+1]): 
                while intensity[j][0] <= x[i+1]:
                    y[i] = y[i] + np.array(intensity[j][1])
                    j +=1
                    if j > (len(intensity) -1):
                        break
            else:
                y[i] = 0
    
    return y

class Dane:
    """Class dane, objects are data read from a dynmat or txt file.
    """
    def __init__(self, nameOfFile: str, StartDataReadInLine: str):
       self.nameOfFile = nameOfFile
       self.StartDataReadInLine = StartDataReadInLine
    def wczytaj(self) -> list:
       """Loads a file and returns a list of mods 

       Returns:
           list: List of mods 
       """
       try:  
           file = open(self.nameOfFile, "r")
       except: 
           print("There is no such file!!!")
           
       line = ""
       if self.StartDataReadInLine != "":
           while self.StartDataReadInLine not in line: 
               line = file.readline()
           
       listOfMods =[]
       line = file.readline()
       if self.StartDataReadInLine == "":
           line = file.readline()
       while not ("" == line or "\n" == line) :
           splited = line.split()
           mod = []
           for x in splited: 
               mod.append(float(x))
           listOfMods.append(mod)
           line = file.readline()  
       file.close()
       return listOfMods  

class ListOfMods:
    """The object is the mods tables from loaded files
    """
    def __init__(self, listOfMods: list):
        self.listOfMods = listOfMods
    def max_min(self) -> tuple:
        """Return max and min wavenumber from list of mods 

        Returns:
            tuple: min, max
        """
        if len(self.listOfMods[0]) == 3:
            i = 0
        else:
            i = 1
        minOf = math.ceil(self.listOfMods[0][i] - 5)
        lenght = len(self.listOfMods) - 1
        maxOf = math.ceil(self.listOfMods[lenght][i] + 100)
        return minOf, maxOf
    def raman(self) -> list:
        """Return list of raman mods.

        Returns:
            list: list of Raman mods 
        """
        if len(self.listOfMods[0]) == 3:
            x1, x2, x3 = zip(*self.listOfMods)
            raman = list(zip(x1, x3))
            del x1 
            del x2
            del x3 
        else:
            x1, x2, x3, x4, x5, x6 = zip(*self.listOfMods)
            raman = list(zip(x2, x5))
            del x1
            del x2
            del x3 
            del x4
            del x5
            del x6
        return raman

    def ir(self) -> list:
        """Return list of ir mods.

        Returns:
            list: list of ir mods 
        """
        if len(self.listOfMods[0]) == 3:
            x1, x2, x3 = zip(*self.listOfMods)
            ir = list(zip(x1, x2))
            del x1 
            del x2
            del x3 
        else:
            x1, x2, x3, x4, x5, x6 = zip(*self.listOfMods)
            ir = list(zip(x2, x4))
            del x1
            del x2
            del x3 
            del x4
            del x5
            del x6
        return ir

class Pasmo:
    """Objects are a single band.
    """
    def __init__(self, Intensity: float, wavenumber: float, numberOfPoints: int,  Q: float, minimum: float, maximum: float):
        self.Intensity = Intensity
        self.wavenumber = wavenumber
        self.numberOfPoints = numberOfPoints
        self.Q = Q
        self.maximum = maximum
        self.minimum = minimum
    def gausscurve(self) -> np.array:
        """Return a gaussian curve  for band

        Returns:
            np.array: gaussian curve  for band
        """
        delta = (self.maximum - self.minimum)/self.numberOfPoints
        x = self.minimum
        curve = np.zeros((2,self.numberOfPoints))
        maxGauss = stats.norm.pdf(self.wavenumber, loc=self.wavenumber, scale=self.Q)
        scale = 1 / maxGauss
        for i in range(1, self.numberOfPoints):
            curve[1, i] = round(self.Intensity * scale * stats.norm.pdf(x, loc=self.wavenumber, scale=self.Q), 4)
            curve[0, i] = x
            x += delta
        return curve
    def cauchycurve(self) -> np.array:
        """Return a cauchy curve  for band

        Returns:
            np.array: cauchy curve  for band
        """
        delta = (self.maximum - self.minimum)/self.numberOfPoints
        x = self.minimum
        curve = np.zeros((2,self.numberOfPoints))
        cauchyMax = stats.cauchy.pdf(self.wavenumber, loc=self.wavenumber, scale=self.Q)
        scale = 1 / cauchyMax
        for i in range(1, self.numberOfPoints):
            curve[1, i] = round(self.Intensity * scale * stats.cauchy.pdf(x, loc=self.wavenumber, scale=self.Q), 4)
            curve[0, i] = x
            x += delta
        return curve
    def voigtcurve(self, Q2) -> np.array:
        """Return a voigt curve  for band
        This mathod is the fastes. 
        Returns:
            np.array: voigt curve  for band
        """
        delta = (self.maximum - self.minimum)/self.numberOfPoints
        x = self.minimum
        curve = np.zeros((2,self.numberOfPoints))
        voigtMax = special.voigt_profile(0, self.Q, Q2)
        scale = 1 / voigtMax
        for i in range(1, self.numberOfPoints):
            curve[1, i] = round(self.Intensity * scale * special.voigt_profile(x - self.wavenumber, self.Q, Q2), 4)
            curve[0, i] = x
            x += delta
        return curve       
 
class Envelope:
    """objects are lists of bands for Raman or Ir"""
    def __init__(self, curve: list, NrPoints: int, Q: float, minimum: float, maximum: float):
        self.curve = curve
        self.NrPoints = NrPoints
        self.Q = Q
        self.minimum = minimum
        self.maximum = maximum
    def do_envelope(self, typeBand: str, Q2: float) -> np.array:
        """Returns an envelope

        Args:
            typeBand (str): Gauss/Cauchy/Voigt 
            Q2 (float): Q2 for Voigt curve 

        Returns:
            np.array: envelope 
        """
        wyniki = np.zeros((2,self.NrPoints))
        if typeBand == "Lorentz":
            for i in range(0, len(self.curve)):
                if self.curve[i][1] > 0.001:
                    wyniki1 = np.array(Pasmo(self.curve[i][1], self.curve[i][0], self.NrPoints, self.Q, self.minimum, self.maximum).cauchycurve())
                    wyniki[0,0:] = wyniki1[0,0:]
                    wyniki[1,0:] = wyniki1[1,0:] + wyniki[1,0:]
        elif typeBand == "Voigt":
            for i in range(0, len(self.curve)):
                if self.curve[i][1] > 0.001:
                    wyniki1 = np.array(Pasmo(self.curve[i][1], self.curve[i][0], self.NrPoints, self.Q, self.minimum, self.maximum).voigtcurve(Q2))
                    wyniki[0,0:] = wyniki1[0,0:]
                    wyniki[1,0:] = wyniki1[1,0:] + wyniki[1,0:]
        else:
            for i in range(0, len(self.curve)):
                if self.curve[i][1] > 0.001:
                    wyniki1 = np.array(Pasmo(self.curve[i][1], self.curve[i][0], self.NrPoints, self.Q, self.minimum, self.maximum).gausscurve())
                    wyniki[0,0:] = wyniki1[0,0:]
                    wyniki[1,0:] = wyniki1[1,0:] + wyniki[1,0:]
                    
        return wyniki

class Results: 
    """Objects are the results to save or draw"""
    def __init__(self, wyniki: np.array, name: str):
        self.wyniki = wyniki 
        self.name = name
    def save(self, label: str):
        """save results 

        Args:
            label (str): Name of envelope eg. Raman or IR
        """
        file_name = "{}_{}.txt"
        results = open(file_name.format(label, self.name), "w")
        results.write("cm-1 Intensity \n")
        results.write("\n")
        colums = self.wyniki.shape 
        for i in range(1, colums[1]): 
            results.write(str(self.wyniki[0, i]) + " " + str(self.wyniki[1, i]) + "\n")
        results.close()
        return
    def print_fig(self, label: str, intensity: list):
        """Print fig 

        Args:
            label (str): Name of envelope eg. Raman or IR
            intensity (list): List of mods 
        """
        x = np.array(self.wyniki[0, 0:])
        y = np.array(self.wyniki[1, 0:])
        Fig_title = "{}_{}"
        plt.xlabel("cm^-1")
        plt.ylabel("Intensity")
        plt.title(Fig_title.format(label, self.name))
        plt.plot(x, y)
        y = int_bonds(x, y, intensity)
        plt.stem(x, y, markerfmt='none', linefmt='red', basefmt='none')
        plt.show()
        return
    def save_fig(self, label: str, intensity: list):
        """save fig 

        Args:
            label (str): Name of envelope eg. Raman or IR
            intensity (list): List of mods 
        """
        x = np.array(self.wyniki[0, 0:]) 
        y = np.array(self.wyniki[1, 0:])
        Fig_title = "{}_{}"
        plt.xlabel("cm^-1")
        plt.ylabel("Intensity")
        plt.title(Fig_title.format(label, self.name))
        plt.plot(x, y)
        y = np.zeros(len(y))
        j = 0
        y = int_bonds(x, y, intensity)
        plt.stem(x, y, markerfmt='none', linefmt='red', basefmt='none') 
        name = "{}_{}.png"
        name1 = name.format(label, self.name)
        plt.savefig(name1, dpi=600)
        plt.close()
        return