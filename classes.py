# -*- coding: utf-8 -*-
"""
Created on Sun Mar 14 23:16:18 2021

@author: pagoj
"""
import math as math
import scipy.stats as stats
import numpy as np
import matplotlib.pyplot as plt

#Kasa obiektów dane, metoda wczytaj wczytuje dane z pliku i zwraca tablicę z wczytanymi danymi
class Dane:
   def __init__(self, name_of_file, Start_data_read_in_line):
       self.name_of_file = name_of_file
       self.Start_data_read_in_line = Start_data_read_in_line
   def wczytaj(self):
       try:  
           file = open(self.name_of_file, "r")
       except: 
           print("There is no such file!!!")
           
       line = ""

       while self.Start_data_read_in_line not in line: 
           line = file.readline()
           
       list_of_mods =[]
       line = file.readline()
       while "\n" != line:
           splited = line.split()
           mod = []
           for x in splited: 
               mod.append(x)
           list_of_mods.append(mod)
           line = file.readline()  
       file.close()
       return list_of_mods  

#obiekt lista modow, metody: zwraca wartosc najwieksz i najmniejsza, zwraca intensywnosci dla ramana i IR
class List_of_mods:
    def __init__(self, list_of_mods):
        self.list_of_mods = list_of_mods
    def max_min(self):
        min_of = math.ceil(float(self.list_of_mods[0][1]) - 1)
        lenght = len(self.list_of_mods) - 1
        max_of = math.ceil(float(self.list_of_mods[lenght][1]) + 100)
        return min_of, max_of
    def raman(self):
        x1, x2, x3, x4, x5, x6 = zip(*self.list_of_mods)
        raman = list(zip(x2, x5))
        del x1
        del x2
        del x3 
        del x4
        del x5
        del x6
        return raman
    def ir(self):
        x1, x2, x3, x4, x5, x6 = zip(*self.list_of_mods)
        ir = list(zip(x2, x4))
        del x1
        del x2
        del x3 
        del x4
        del x5
        del x6
        return ir

#liczy gaussy dla modow
class Gauss:
    def __init__(self, Intensity, wavenumber, number_of_points,  Q, minimum, maximum):
        self.Intensity = Intensity
        self.wavenumber = wavenumber
        self.number_of_points = number_of_points
        self.Q = Q
        self.maximum = maximum
        self.minimum = minimum
    def gausscurve(self):
        delta = (self.maximum - self.minimum)/self.number_of_points
        x = self.minimum
        curve = np.zeros((2,self.number_of_points))
        max_gauss = stats.norm.pdf(self.wavenumber, loc=self.wavenumber, scale=self.Q)
        scale = 1 / max_gauss
        for i in range(0, self.number_of_points):
            curve[1, i] = round(self.Intensity * scale * stats.norm.pdf(x, loc=self.wavenumber, scale=self.Q), 4)
            curve[0, i] = x
            x += delta
        return curve

#Tworzy obwiednie 
class Envelope:
    def __init__(self, curve, Nr_points, Q, minimum, maximum):
        self.curve = curve
        self.Nr_points = Nr_points
        self.Q = Q
        self.minimum = minimum
        self.maximum = maximum
    def do_envelope(self):
        wyniki = np.zeros((2,self.Nr_points))
        for i in range(0, len(self.curve)):
            if float(self.curve[i][1]) > 0.0005:
                wyniki1 = np.array(Gauss(float(self.curve[i][1]), float(self.curve[i][0]), self.Nr_points, self.Q, self.minimum, self.maximum).gausscurve())
                wyniki[0,0:] = wyniki1[0,0:]
                wyniki[1,0:] = wyniki1[1,0:] + wyniki[1,0:]
        return wyniki 

#Wyniki, metowy wypisywanie do pliku tekstowego, worzenie wykresu z wykorzystaniem matplotlib
class Results: 
    def __init__(self, wyniki, name):
        self.wyniki = wyniki 
        self.name = name
    def save(self, label):
        file_name = "{}_{}.txt"
        results = open(file_name.format(label, self.name), "w")
        results.write("cm-1 Intensity \n")
        results.write("\n")
        colums = self.wyniki.shape 
        for i in range(0, colums[1]): 
            results.write(str(self.wyniki[0, i]) + " " + str(self.wyniki[1, i]) + "\n")
        results.close()
        return
    def print_fig(self, label):
        x = self.wyniki[0, 0:]
        y = self.wyniki[1, 0:]
        Fig_title = "{}_{}.txt"
        plt.xlabel("cm^-1")
        plt.ylabel("Intensity")
        plt.title(Fig_title.format(label, self.name))
        plt.plot(x, y)
        plt.show()
        return