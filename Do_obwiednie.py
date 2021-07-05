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

nazwaObw1 = "Raman"
nazwaObw2 = "IR"
       
print("Insert the: dynmat/txt, type of band curve, width of the curves, number of pints, file name, label name and Raman/IR/Both")


#dane wejsciowe
try:
    formatOfFile = str(input()) #format of file txt or dynmat
    typeOfBand = str(input()) #Gauss, Lorentz, Voigt
    widthBands = str(input()) #Q-Gauss and Q-Lorentz
    NrPoints = int(input()) #number of points in Envelope 
    nameOfFile= str(input()) #Name of file with data 
    label = str(input()) #Label of output files 
    IrRaman =str(input()) #Envelope for Raman or IR or Both 
except:
    print("Wrong inputs")
    
if (typeOfBand != "Gauss" and typeOfBand != "Lorentz" and typeOfBand != "Voigt"):
    raise Exception("Wrong name of gauss like curve!!!") 
    
#miejsce od ktorego maja byc wczytywane dane z pliku tekstowego
if formatOfFile == "dynmat":
    Start_data_read_in_line = "# mode"

    #wczywywanie danych
    dane1 = Dane(nameOfFile, Start_data_read_in_line)
    listOfMods = dane1.wczytaj()
elif formatOfFile == "txt":
    Start_data_read_in_line = ""
    #wczywywanie danych
    dane1 = Dane(nameOfFile, Start_data_read_in_line)
    listOfMods = dane1.wczytaj()
else:
    raise Exception("File format not supported") 

print("Data loaded")
listOfMods1 = ListOfMods(listOfMods)

minimum, maximum = listOfMods1.max_min()
if IrRaman == nazwaObw1:
    raman = listOfMods1.raman() #lista modow raman
elif IrRaman == nazwaObw2:
    ir = listOfMods1.ir() #lista modow IR
else: 
    raman = listOfMods1.raman()
    ir = listOfMods1.ir()

#Tworzenie obwiedni 
if typeOfBand == "Voigt":
    splited = widthBands.split()
    Q = float(splited[0])
    Q2 = float(splited[1])
else: 
    Q = float(widthBands.split()[0])
    Q2 = 0
    
if IrRaman != nazwaObw2:
    ramanEnvelpe = Envelope(raman, NrPoints, Q, minimum, maximum).do_envelope(typeOfBand, Q2)
    print("raman envelope done")
if IrRaman != nazwaObw1:
    irEnvelpe = Envelope(ir, NrPoints, Q, minimum, maximum).do_envelope(typeOfBand, Q2)
    print("IR envelope done")
#Wypisywanie rezultatow
if IrRaman != nazwaObw2:
    Results(ramanEnvelpe, "Raman").print_fig(label, raman)
if IrRaman != nazwaObw1:
    Results(irEnvelpe, "IR").print_fig(label, ir)
if IrRaman != nazwaObw2:
    Results(ramanEnvelpe, "Raman").save(label)
if IrRaman != nazwaObw1:
    Results(irEnvelpe, "IR").save(label)
if IrRaman != nazwaObw2:
    Results(ramanEnvelpe, "Raman").save_fig(label, raman)
if IrRaman != nazwaObw1:
    Results(irEnvelpe, "IR").save_fig(label, ir)
print("result saved")