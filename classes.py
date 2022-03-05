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
    def __init__(self, name_of_file: str, start_data_read_in_line: str):
       self.name_of_file = name_of_file
       self.start_data_read_in_line = start_data_read_in_line
       
    def load_file(self):
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
       
       if start_data_read_in_line != "":
           
           while start_data_read_in_line not in line: 

               line = file.readline()
           
       listOfMods =[]
       line = file.readline()
       
       if start_data_read_in_line == "":

           line = file.readline()
           
       while not ("" == line or "\n" == line) :
           splited = line.split()
           mod = []
           
           for x in splited: 
               mod.append(float(x))
               
           list_of_mods.append(mod)
           line = file.readline()  
           
       file.close()
       
       return list_of_mods  


class ListOfMods:
    """The object is the mods tables from loaded files
    """
    def __init__(self, list_of_mods: list):
        self.list_of_mods = list_of_mods
        
    def max_min(self) -> tuple:
        """Return max and min wavenumber from list of mods 

        Returns:
            tuple: min, max
        """
        
        if len(self.list_of_mods[0]) == 3:
            i = 0
            
        else:
            i = 1
            
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
    
    def raman(self) -> list:
        """Return list of raman mods.

        Returns:
            list: list of Raman mods 
        """
        if len(self.list_of_mods[0]) == 3:
            x1, x2, x3 = zip(*self.list_of_mods)
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
        if len(self.list_of_mods[0]) == 3:
            x1, x2, x3 = zip(*self.list_of_mods)
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
        """Return a voigt curve  for band
        This mathod is the fastes. 
        Returns:
            np.array: voigt curve  for band
        """
        
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
            curve[0, i] = x
            x += delta
            
        return curve       
 
class Envelope:
    """objects are lists of bands for Raman or Ir"""
    def __init__(self, curve: list, nr_points: int, minimum: float, maximum: float, max_intensity: float):
        self.curve = curve
        self.nr_points = nr_points
        self.minimum = minimum
        self.maximum = maximum
        self.max_intensity = max_intensity
        
    def do_envelope(self, typeBand: str, Q1: float, Q2: float = 0, proportional_to_height: bool = False) -> np.array:
        """Returns an envelope

        Args:
            typeBand (str): Gauss/Cauchy/Voigt 
            Q2 (float): Q2 for Voigt curve 

        Returns:
            np.array: envelope 
        """
        
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

                    wyniki[0,0:] = wyniki1[0,0:]
                    wyniki[1,0:] = wyniki1[1,0:] + wyniki[1,0:]
                    
        elif typeBand == "Gauss":
            for i in range(0, len(self.curve)):
                if self.curve[i][1] > 0.001:
                    wyniki1 = np.array(Pasmo(self.curve[i][1], self.curve[i][0], self.nr_points, self.minimum, self.maximum, proportional_to_height, self.max_intensity).voigtcurve(Q1, 0))

                    wyniki[0,0:] = wyniki1[0,0:]
                    wyniki[1,0:] = wyniki1[1,0:] + wyniki[1,0:]
                    
        else:
            raise Exception("Wrong curve type: Gauss/Lorentz/Voigt")
                    
        return wyniki

class Results: 
    """Objects are the results to save or draw"""
    def __init__(self, wyniki: DataFrame, path):
        self.path = path
        self.wyniki = wyniki 

        
    def save_data(self):

        (self.wyniki).to_csv(self.path, sep=',')
        
    
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

    
    def save_fig(self, label: str, intensity: list):
        """save fig 

        Args:
            label (str): Name of envelope eg. Raman or IR
            intensity (list): List of mods 
        """
        x = np.array(self.wyniki[0, 1:]) 
        y = np.array(self.wyniki[1, 1:])
        
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