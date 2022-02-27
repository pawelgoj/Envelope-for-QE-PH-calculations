# -*- coding: utf-8 -*-
"""
Created on Sun Mar 14 19:54:36 2021

@author: Pawel Goj
"""

from classes import *


name_obw_1 = "Raman"
name_obw_2 = "IR"
       
print('Insert the: dynmat/txt, type of band curve, width of the curves, number of pints'\
    ', file name, label name and Raman/IR/Both')


#inputs
try:

    format_of_file = str(input()) #format of file txt or dynmat
    type_of_band = str(input()) #Gauss, Lorentz, Voigt
    width_bands = str(input()) #Q-Gauss and Q-Lorentz
    proportional_to_height = str(input()) #Q-Gauss and Q-Lorentz
    nr_points = int(input()) #number of points in Envelope 
    name_of_file= str(input()) #Name of file with data 
    label = str(input()) #Label of output files 
    ir_raman =str(input()) #Envelope for Raman or IR or Both 
    
except:
    print("Wrong inputs")
    
if (type_of_band != "Gauss" and type_of_band != "Lorentz" and type_of_band != "Voigt"):
    raise Exception("Wrong name of gauss like curve!!!") 
    
#the place to which data are read in text file
if format_of_file == "dynmat":
    Start_data_read_in_line = "# mode"

    #data read
    dane_1 = Dane(name_of_file, Start_data_read_in_line)
    list_of_mods = dane_1.wczytaj()
elif format_of_file == "txt":
    Start_data_read_in_line = ""

    dane_1 = Dane(name_of_file, Start_data_read_in_line)
    list_of_mods = dane_1.wczytaj()
else:
    raise Exception("File format not supported") 

print("Data loaded")
list_of_mods1 = ListOfMods(list_of_mods)

minimum, maximum = list_of_mods1.max_min()

if ir_raman == name_obw_1:
    raman = list_of_mods1.raman() #list of raman mods 
    max_raman_intensity = list_of_mods1.raman_max_intensity()
    
elif ir_raman == name_obw_2:
    ir = list_of_mods1.ir() #list of ir mods 
    max_ir_intensity = list_of_mods1.ir_max_intensity()
    
else: 
    max_ir_intensity = list_of_mods1.ir_max_intensity()
    max_raman_intensity = list_of_mods1.raman_max_intensity()
    raman = list_of_mods1.raman()
    ir = list_of_mods1.ir()

#create envelope 
if type_of_band == "Voigt":
    splited = width_bands.split()
    Q1 = float(splited[0])
    Q2 = float(splited[1])
elif type_of_band == "Lorentz" or type_of_band == "Gauss": 
    Q1 = float(width_bands.split()[0])
    Q2 = 0
else:
    raise Exception("Wrong curve type: Gauss/Lorentz/Voigt")

if proportional_to_height == 'proportional':
    proportional_to_height = True
    
else: 
    proportional_to_height = False
    
if ir_raman != name_obw_2:
    raman_envelpe = Envelope(raman, nr_points, minimum, maximum, max_raman_intensity).do_envelope(type_of_band, Q1, Q2, proportional_to_height = proportional_to_height)
    print("raman envelope done")
    
if ir_raman != name_obw_1:
    ir_envelpe = Envelope(ir, nr_points, minimum, maximum, max_ir_intensity).do_envelope(type_of_band, Q1, Q2, proportional_to_height = proportional_to_height)
    print("IR envelope done")

#write resoults 
'''
if ir_raman != name_obw_2:
    Results(raman_envelpe, "Raman").print_fig(label, raman)
if ir_raman != name_obw_1:
    Results(ir_envelpe, "IR").print_fig(label, ir)
'''

if ir_raman != name_obw_2:
    Results(raman_envelpe, "Raman").save(label)
if ir_raman != name_obw_1:
    Results(ir_envelpe, "IR").save(label)
if ir_raman != name_obw_2:
    Results(raman_envelpe, "Raman").save_fig(label, raman)
if ir_raman != name_obw_1:
    Results(ir_envelpe, "IR").save_fig(label, ir)
print("result saved") 