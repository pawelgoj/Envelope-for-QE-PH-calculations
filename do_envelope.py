# -*- coding: utf-8 -*-
"""
Created on Sun Mar 14 19:54:36 2021

@author: Pawel Goj
"""

from classes import *

class DuEnvelope:
    def __init__(self, format_of_file: str, type_of_band: str, width_band_g: float, width_band_l: float, proportional_to_height: bool,
                 nr_points: int, file: str, ir_raman: str, raman_envelpe = None, ir_envelpe = None):
        self.name_obw_1 = "Raman"
        self.name_obw_2 = "IR"

        #inputs
        try:

            self.format_of_file = format_of_file #format of file txt or dynmat
            self.type_of_band = type_of_band #Gauss, Lorentz, Voigt
            self.width_band_g =  width_band_g #Q-Gauss and Q-Lorentz
            self.width_band_l =  width_band_l
            self.proportional_to_height = proportional_to_height #Q-Gauss and Q-Lorentz
            self.nr_points = nr_points #number of points in Envelope 
            self.file = file #Name of file with data 
            #self.label = label #Label of output files 
            self.ir_raman = ir_raman #Envelope for Raman or IR or Both 
            self.raman_envelpe = raman_envelpe
            self.ir_envelpe = ir_envelpe
            
        except:
            print("Wrong inputs")
            
    def make_envelopes(self):
        if (self.type_of_band != "Gauss" and self.type_of_band != "Lorentz" and self.type_of_band != "Voigt"):
            raise Exception("Wrong name of gauss like curve!!!") 
            
        #the place to which data are read in text file
        if self.format_of_file == "dynmat":
            start_data_read_in_line = "# mode"

            #data read 
            data = Dane(self.file, start_data_read_in_line)
            list_of_mods = data.load_file()
        elif self.format_of_file == "txt":
            start_data_read_in_line = ""
            data = Dane(self.file, start_data_read_in_line)
            list_of_mods = data.load_file()
        else:
            raise Exception("File format not supported") 

        #print("Data loaded")
        list_of_mods1 = ListOfMods(list_of_mods)

        minimum, maximum = list_of_mods1.max_min()

        if self.ir_raman == self.name_obw_1:
            self.raman = list_of_mods1.raman() #list of raman mods 
            max_raman_intensity = list_of_mods1.raman_max_intensity()
            
        elif self.ir_raman == self.name_obw_2:
            self.ir = list_of_mods1.ir() #list of ir mods 
            max_ir_intensity = list_of_mods1.ir_max_intensity()
            
        else: 
            max_ir_intensity = list_of_mods1.ir_max_intensity()
            max_raman_intensity = list_of_mods1.raman_max_intensity()
            self.raman = list_of_mods1.raman()
            self.ir = list_of_mods1.ir()

        #create envelope 
        if self.type_of_band == "Voigt":
            Q1 = self.width_band_g
            Q2 = self.width_band_l
        elif self.type_of_band == "Lorentz" or self.type_of_band == "Gauss": 
            Q1 = self.width_band_l
            Q2 = 0
        else:
            raise Exception("Wrong curve type: Gauss/Lorentz/Voigt")

        if self.proportional_to_height == 'proportional':
            self.proportional_to_height = True
            
        else: 
            self.proportional_to_height = False
            
        if self.ir_raman != self.name_obw_2:
            self.raman_envelpe = Envelope(self.raman, self.nr_points, minimum, maximum, max_raman_intensity).do_envelope(self.type_of_band, Q1, Q2, proportional_to_height = self.proportional_to_height)
            self.raman_envelpe = self.raman_envelpe.transpose()
            print("raman envelope done")
            
        if self.ir_raman != self.name_obw_1:
            self.ir_envelpe = Envelope(self.ir, self.nr_points, minimum, maximum, max_ir_intensity).do_envelope(self.type_of_band, Q1, Q2, proportional_to_height = self.proportional_to_height)
            self.ir_envelpe = self.ir_envelpe.transpose()
            print("IR envelope done")

        #write resoults 
        '''
        if ir_raman != self.name_obw_2:
            Results(raman_envelpe, "Raman").print_fig(label, raman)
        if ir_raman != name_obw_1:
            Results(ir_envelpe, "IR").print_fig(label, ir)
        '''
    
    #TODO Implement this method    
    def save_envelopes(self, path):
        #code procesing np.array to dataframe 
        if  not (self.raman_envelpe is None) and not(self.ir_envelpe is None):
            array_to_dt = np.hstack((self.ir_envelpe, self.raman_envelpe))
            df = pd.DataFrame(array_to_dt, columns=['cm-1', 'IR', 'cm-1', 'Raman'])
            
        elif self.raman_envelpe:
            df = pd.DataFrame(self.raman_envelpe, columns=['cm-1', 'Raman'])
            
        elif self.ir_envelpe:
            df = pd.DataFrame(self.ir_envelpe, columns=['cm-1', 'IR'])            
                        
        results = Results(df, path)
        results.save_data()
    
    #TODO Implement this method         
    def save_figs(self):
        pass

        print("result saved") 