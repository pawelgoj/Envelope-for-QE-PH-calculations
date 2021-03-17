# -*- coding: utf-8 -*-
"""
Created on Sun Mar 14 19:54:36 2021

@author: pagoj
"""
import numpy as np 
import math as math
import scipy.stats as stats
from classes import *
import matplotlib.pyplot as plt

nazwa_obw_1 = "Raman"
nazwa_obw_2 = "IR"
       
print("Insert the: dynmat/txt, type of band curve, width of the curves, number of pints, file name, label name and Raman/IR/Both")


#dane wejsciowe
try:
    format_of_file = str(input()) #format of file txt or dynmat
    type_of_band = str(input()) #Gauss, Lorentz, Voigt
    width_bands = str(input()) #Q-Gauss and Q-Lorentz
    Nr_points = int(input()) #number of points in Envelope 
    name_of_file= str(input()) #Name of file with data 
    label = str(input()) #Label of output files 
    Ir_Raman =str(input()) #Envelope for Raman or IR or Both 
except:
    print("Wrong inputs")
    
if (type_of_band != "Gauss" and type_of_band != "Lorentz" and type_of_band != "Voigt"):
    raise Exception("Wrong name of gauss like curve!!!") 
    
#miejsce od ktorego maja byc wczytywane dane z pliku tekstowego
if format_of_file == "dynmat":
    Start_data_read_in_line = "# mode"

    #wczywywanie danych
    dane1 = Dane(name_of_file, Start_data_read_in_line)
    list_of_mods = dane1.wczytaj()
elif format_of_file == "txt":
    Start_data_read_in_line = ""
    #wczywywanie danych
    dane1 = Dane(name_of_file, Start_data_read_in_line)
    list_of_mods = dane1.wczytaj()
else:
    raise Exception("File format not supported") 

print("Data loaded")
list_of_mods1 = List_of_mods(list_of_mods)

minimum, maximum = list_of_mods1.max_min()
if Ir_Raman == nazwa_obw_1:
    raman = list_of_mods1.raman() #lista modow raman
elif Ir_Raman == nazwa_obw_2:
    ir = list_of_mods1.ir() #lista modow IR
else: 
    raman = list_of_mods1.raman()
    ir = list_of_mods1.ir()

#Tworzenie obwiedni 
if type_of_band == "Voigt":
    splited = width_bands.split()
    Q = float(splited[0])
    Q2 = float(splited[1])
else: 
    Q = float(width_bands.split()[0])
    Q2 = 0
    
if Ir_Raman != nazwa_obw_2:
    raman_envelpe = Envelope(raman, Nr_points, Q, minimum, maximum).do_envelope(type_of_band, Q2)
    print("raman envelope done")
if Ir_Raman != nazwa_obw_1:
    ir_envelpe = Envelope(ir, Nr_points, Q, minimum, maximum).do_envelope(type_of_band, Q2)
    print("IR envelope done")
#Wypisywanie rezultatow
if Ir_Raman != nazwa_obw_2:
    Results(raman_envelpe, "Raman").print_fig(label, raman)
if Ir_Raman != nazwa_obw_1:
    Results(ir_envelpe, "IR").print_fig(label, ir)
if Ir_Raman != nazwa_obw_2:
    Results(raman_envelpe, "Raman").save(label)
if Ir_Raman != nazwa_obw_1:
    Results(ir_envelpe, "IR").save(label)
if Ir_Raman != nazwa_obw_2:
    Results(raman_envelpe, "Raman").save_fig(label, raman)
if Ir_Raman != nazwa_obw_1:
    Results(ir_envelpe, "IR").save_fig(label, ir)
print("result saved")