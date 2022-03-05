# -*- coding: utf-8 -*-
"""
Created on Sun Mar 14 23:16:18 2021

@author: pagoj
"""
from logging import raiseExceptions
import math as math
from typing import Tuple
import scipy.special as special
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pandas import DataFrame

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
<<<<<<< HEAD
    def __init__(self, name_of_file: str, start_data_read_in_line: str):
       self.name_of_file = name_of_file
       self.start_data_read_in_line = start_data_read_in_line
       
    def load_file(self):
=======
    def __init__(self, nameOfFile: str, StartDataReadInLine: str):
       self.nameOfFile = nameOfFile
       self.StartDataReadInLine = StartDataReadInLine
    def wczytaj(self) -> list:
>>>>>>> b1ee945981ab195c0d32946c44d2b64d645b47c7
       """Loads a file and returns a list of mods 

       Returns:
           list: List of mods 
       """
       try:  
           file = open(self.nameOfFile, "r")
       except: 
           print("There is no such file!!!")
        
       list_of_mods = Dane.read_data(file, self.start_data_read_in_line)
       return list_of_mods
           
    @staticmethod     
    def read_data(file, start_data_read_in_line: str) -> list:
       line = ""
<<<<<<< HEAD
       
       if start_data_read_in_line != "":
           
           while start_data_read_in_line not in line: 
=======
       if self.StartDataReadInLine != "":
           while self.StartDataReadInLine not in line: 
>>>>>>> b1ee945981ab195c0d32946c44d2b64d645b47c7
               line = file.readline()
           
       listOfMods =[]
       line = file.readline()
<<<<<<< HEAD
       
       if start_data_read_in_line == "":
=======
       if self.StartDataReadInLine == "":
>>>>>>> b1ee945981ab195c0d32946c44d2b64d645b47c7
           line = file.readline()
           
       while not ("" == line or "\n" == line) :
           splited = line.split()
           mod = []
           
           for x in splited: 
               mod.append(float(x))
<<<<<<< HEAD
               
           list_of_mods.append(mod)
=======
           listOfMods.append(mod)
>>>>>>> b1ee945981ab195c0d32946c44d2b64d645b47c7
           line = file.readline()  
           
       file.close()
<<<<<<< HEAD
       
       return list_of_mods  
=======
       return listOfMods  
>>>>>>> b1ee945981ab195c0d32946c44d2b64d645b47c7

class ListOfMods:
    """The object is the mods tables from loaded files
    """
<<<<<<< HEAD
    def __init__(self, list_of_mods: list):
        self.list_of_mods = list_of_mods
        
=======
    def __init__(self, listOfMods: list):
        self.listOfMods = listOfMods
>>>>>>> b1ee945981ab195c0d32946c44d2b64d645b47c7
    def max_min(self) -> tuple:
        """Return max and min wavenumber from list of mods 

        Returns:
            tuple: min, max
        """
<<<<<<< HEAD
        
        if len(self.list_of_mods[0]) == 3:
=======
        if len(self.listOfMods[0]) == 3:
>>>>>>> b1ee945981ab195c0d32946c44d2b64d645b47c7
            i = 0
            
        else:
            i = 1
<<<<<<< HEAD
            
        minOf = math.ceil(self.list_of_mods[0][i] - 5)
        lenght = len(self.list_of_mods) - 1
        maxOf = math.ceil(self.list_of_mods[lenght][i] + 100)
        
        return minOf, maxOf
    
    def raman_max_intensity(self):
        
        max_item = 0 
        
        for item in self.list_of_mods:
            if max_item < item[4]:
                max_item = item[4]
                
        return max_item
    
    def ir_max_intensity(self):
        
        max_item = 0 
        
        for item in self.list_of_mods:
            if max_item < item[3]:
                max_item = item[3]
        
        return max_item
    
=======
        minOf = math.ceil(self.listOfMods[0][i] - 5)
        lenght = len(self.listOfMods) - 1
        maxOf = math.ceil(self.listOfMods[lenght][i] + 100)
        return minOf, maxOf
>>>>>>> b1ee945981ab195c0d32946c44d2b64d645b47c7
    def raman(self) -> list:
        """Return list of raman mods.

        Returns:
            list: list of Raman mods 
        """
<<<<<<< HEAD
        if len(self.list_of_mods[0]) == 3:
            x1, x2, x3 = zip(*self.list_of_mods)
=======
        if len(self.listOfMods[0]) == 3:
            x1, x2, x3 = zip(*self.listOfMods)
>>>>>>> b1ee945981ab195c0d32946c44d2b64d645b47c7
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
<<<<<<< HEAD
        if len(self.list_of_mods[0]) == 3:
            x1, x2, x3 = zip(*self.list_of_mods)
=======
        if len(self.listOfMods[0]) == 3:
            x1, x2, x3 = zip(*self.listOfMods)
>>>>>>> b1ee945981ab195c0d32946c44d2b64d645b47c7
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
<<<<<<< HEAD
    def __init__(self, intensity: float, wavenumber: float, number_of_points: int,
                 minimum: float, maximum: float, proportional_to_height: bool, max_intensity: float):
        self.intensity = intensity
        self.wavenumber = wavenumber
        self.number_of_points = number_of_points
        self.maximum = maximum
        self.minimum = minimum
        self.proportional_to_height = proportional_to_height
        self.max_intensity = max_intensity

    def voigtcurve(self, Q1, Q2) -> np.array:
=======
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
>>>>>>> b1ee945981ab195c0d32946c44d2b64d645b47c7
        """Return a voigt curve  for band
        This mathod is the fastes. 
        Returns:
            np.array: voigt curve  for band
        """
<<<<<<< HEAD
        
        if self.proportional_to_height == True:
            
            Q1 = 0.75 * Q1 * (self.intensity / self.max_intensity) + 0.25 * Q1
            Q2 = 0.75 * Q2 * (self.intensity / self.max_intensity) + 0.25 * Q2
        
        delta = (self.maximum - self.minimum) / self.number_of_points
        x = self.minimum
        curve = np.zeros((2,self.number_of_points))
        voigt_max = special.voigt_profile(0, Q1, Q2)
        scale = 1 / voigt_max
               
        for i in range(1, self.number_of_points):
                
            curve[1, i] = round(self.intensity * scale * special.voigt_profile(x - self.wavenumber, Q1, Q2), 5)
=======
        delta = (self.maximum - self.minimum)/self.numberOfPoints
        x = self.minimum
        curve = np.zeros((2,self.numberOfPoints))
        voigtMax = special.voigt_profile(0, self.Q, Q2)
        scale = 1 / voigtMax
        for i in range(1, self.numberOfPoints):
            curve[1, i] = round(self.Intensity * scale * special.voigt_profile(x - self.wavenumber, self.Q, Q2), 4)
>>>>>>> b1ee945981ab195c0d32946c44d2b64d645b47c7
            curve[0, i] = x
            x += delta
            
        return curve       
 
class Envelope:
    """objects are lists of bands for Raman or Ir"""
<<<<<<< HEAD
    def __init__(self, curve: list, nr_points: int, minimum: float, maximum: float, max_intensity: float):
        self.curve = curve
        self.nr_points = nr_points
        self.minimum = minimum
        self.maximum = maximum
        self.max_intensity = max_intensity
        
    def do_envelope(self, typeBand: str, Q1: float, Q2: float = 0, proportional_to_height: bool = False) -> np.array:
=======
    def __init__(self, curve: list, NrPoints: int, Q: float, minimum: float, maximum: float):
        self.curve = curve
        self.NrPoints = NrPoints
        self.Q = Q
        self.minimum = minimum
        self.maximum = maximum
    def do_envelope(self, typeBand: str, Q2: float) -> np.array:
>>>>>>> b1ee945981ab195c0d32946c44d2b64d645b47c7
        """Returns an envelope

        Args:
            typeBand (str): Gauss/Cauchy/Voigt 
            Q2 (float): Q2 for Voigt curve 

        Returns:
            np.array: envelope 
        """
<<<<<<< HEAD
        
        wyniki = np.zeros((2,self.nr_points))
        
        if typeBand == "Lorentz":
            for i in range(0, len(self.curve)):
                if self.curve[i][1] > 0.001:
                    wyniki1 = np.array(Pasmo(self.curve[i][1], self.curve[i][0], self.nr_points, self.minimum, self.maximum, proportional_to_height, self.max_intensity).voigtcurve(0, Q1))
                    wyniki[0,0:] = wyniki1[0,0:]
                    wyniki[1,0:] = wyniki1[1,0:] + wyniki[1,0:]
                    
        elif typeBand == "Voigt":
            for i in range(0, len(self.curve)):
                if self.curve[i][1] > 0.001:
                    wyniki1 = np.array(Pasmo(self.curve[i][1], self.curve[i][0], self.nr_points, self.minimum, self.maximum, proportional_to_height, self.max_intensity).voigtcurve(Q1, Q2))
=======
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
>>>>>>> b1ee945981ab195c0d32946c44d2b64d645b47c7
                    wyniki[0,0:] = wyniki1[0,0:]
                    wyniki[1,0:] = wyniki1[1,0:] + wyniki[1,0:]
                    
        elif typeBand == "Gauss":
            for i in range(0, len(self.curve)):
                if self.curve[i][1] > 0.001:
<<<<<<< HEAD
                    wyniki1 = np.array(Pasmo(self.curve[i][1], self.curve[i][0], self.nr_points, self.minimum, self.maximum, proportional_to_height, self.max_intensity).voigtcurve(Q1, 0))
=======
                    wyniki1 = np.array(Pasmo(self.curve[i][1], self.curve[i][0], self.NrPoints, self.Q, self.minimum, self.maximum).gausscurve())
>>>>>>> b1ee945981ab195c0d32946c44d2b64d645b47c7
                    wyniki[0,0:] = wyniki1[0,0:]
                    wyniki[1,0:] = wyniki1[1,0:] + wyniki[1,0:]
                    
        else:
            raise Exception("Wrong curve type: Gauss/Lorentz/Voigt")
                    
        return wyniki

class Results: 
    """Objects are the results to save or draw"""
<<<<<<< HEAD
    def __init__(self, wyniki: DataFrame, path):
        self.path = path
        self.wyniki = wyniki 

        
    def save_data(self):

        (self.wyniki).to_csv(self.path, sep=',')
        
    
=======
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
>>>>>>> b1ee945981ab195c0d32946c44d2b64d645b47c7
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
        
        name ='Dupa'
        plt.title(Fig_title.format(label, name))
        plt.plot(x, y)
        
        y = int_bonds(x, y, intensity)
        
        plt.stem(x, y, markerfmt='none', linefmt='red', basefmt='none')
        plt.show()
        
        return
<<<<<<< HEAD
    
=======
>>>>>>> b1ee945981ab195c0d32946c44d2b64d645b47c7
    def save_fig(self, label: str, intensity: list):
        """save fig 

        Args:
            label (str): Name of envelope eg. Raman or IR
            intensity (list): List of mods 
        """
<<<<<<< HEAD
        x = np.array(self.wyniki[0, 1:]) 
        y = np.array(self.wyniki[1, 1:])
        
=======
        x = np.array(self.wyniki[0, 0:]) 
        y = np.array(self.wyniki[1, 0:])
>>>>>>> b1ee945981ab195c0d32946c44d2b64d645b47c7
        Fig_title = "{}_{}"
        plt.xlabel("cm^-1")
        plt.ylabel("Intensity")
        plt.title(Fig_title.format(label, self.name))
        
        plt.plot(x, y)
        
        y = int_bonds(x, y, intensity)
        
        plt.stem(x, y, markerfmt='none', linefmt='red', basefmt='none') 
        
        name = "{}_{}.png"
        name1 = name.format(label, self.name)
        
        plt.savefig(name1, dpi=600)
        plt.close()
        
        return