# -*- coding: utf-8 -*-
"""
Created on Sun Mar 14 19:54:36 2021

@author: Pawel Goj
"""

from classes import *
import concurrent.futures 
import tkinter as tk
import logging

#The function for multiprocesing 
def process_envelpe(args: list):
    
    process = args[0]
    type_of_band = args[1]
    Q1 = args[2]
    Q2 = args[3]
    proportional_to_height = args[4]

    envelpe = process.do_envelope(type_of_band, Q1, Q2, proportional_to_height = proportional_to_height)
    envelpe_t = envelpe.transpose()
    
    return envelpe, envelpe_t


class DoEnvelope:
    def __init__(self, application_gui=None):
        self.application_gui = application_gui
    
    def set_param(self, format_of_file: str, type_of_band: str, width_band_g: float, width_band_l: float, proportional_to_height: bool,
                 nr_points: int, file, ir_raman: str, raman_envelpe = None, ir_envelpe = None):
        
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
            logging.error("Wrong inputs")
            
    def make_envelopes(self, progress_bar=None):
        try:
            if (self.type_of_band != "Gauss" and self.type_of_band != "Lorentz" and self.type_of_band != "Voigt"):
                
                logging.error("Wrong name of gauss like curve!!!")
                raise Exception("Wrong name of gauss like curve!!!") 
                
            #the place to which data are read in text file
            if self.format_of_file == "dynmat":
                
                start_data_read_in_line = "# mode"
                #data read 
                data = Dane(self.file, start_data_read_in_line)
                self.file_content, self.first_column_file = data.check_file_content()
                if data.check_file_is_proper() == False:
                    
                    tk.messagebox.showwarning(message='Wrong file!', title='Warning!')
                    logging.error("File format not supported")
                    raise Exception("File format not supported") 
                             
                elif self.file_content == 'Wrong':
                    
                    tk.messagebox.showwarning(message='Wrong file!', title='Warning!')
                    logging.error("File format not supported")
                    raise Exception("File format not supported")
                    
                list_of_mods = data.load_file()
                
            elif self.format_of_file == "txt":
                
                start_data_read_in_line = "cm"
                data = Dane(self.file, start_data_read_in_line)
                self.file_content, self.first_column_file = data.check_file_content()
                
                if data.check_file_is_proper() == False:
                    
                    tk.messagebox.showwarning(message='Wrong file!', title='Warning!')
                    logging.error("File format not supported")
                    raise Exception("File format not supported") 
                
                elif self.file_content == 'Wrong':
                    
                    tk.messagebox.showwarning(message='Wrong file!', title='Warning!')
                    logging.error("File format not supported")
                    raise Exception("File format not supported")
                
                list_of_mods = data.load_file()
                
            else:
                logging.error("File format not supported")
                raise Exception("File format not supported") 
            
            if progress_bar:
                progress_bar['value'] = 20
                self.application_gui.update_idletasks()

            #print("Data loaded")
            list_of_mods1 = ListOfMods(list_of_mods, self.format_of_file, self.first_column_file)

            minimum, maximum = list_of_mods1.max_min()
            print(minimum, maximum)
            if self.ir_raman == self.name_obw_1:
                
                if self.file_content == self.name_obw_1 or self.file_content == 'Both':
                    
                    self.raman = list_of_mods1.raman() #list of raman mods 
                    max_raman_intensity = list_of_mods1.raman_max_intensity()
                    
                else: 
                    tk.messagebox.showwarning(message='File not contain Raman data!',
                                              title='Warning!')
                    logging.error("File not contain Raman data!")
                    raise Exception("File format not supported")
                
            elif self.ir_raman == self.name_obw_2:
                
                if self.file_content == self.name_obw_2 or self.file_content == 'Both':
                    
                    self.ir = list_of_mods1.ir() #list of ir mods 
                    max_ir_intensity = list_of_mods1.ir_max_intensity()
                    
                else:
                    tk.messagebox.showwarning(message='File not contain IR data!', 
                                              title='Warning!')
                    logging.error("File not contain IR data!")
                    raise Exception("File format not supported")
                
            else: 
                if self.file_content == 'Both':
                    max_ir_intensity = list_of_mods1.ir_max_intensity()
                    max_raman_intensity = list_of_mods1.raman_max_intensity()
                    self.raman = list_of_mods1.raman()
                    self.ir = list_of_mods1.ir()
                    
                else:
                    tk.messagebox.showwarning(message='File not contain IR or/and Raman data!', 
                                              title='Warning!')
                    logging.error("File not contain IR data!")
                    raise Exception("File format not supported")
                    

            #create envelope 
            if self.type_of_band == "Voigt":
                Q1 = self.width_band_g
                Q2 = self.width_band_l
                
            elif self.type_of_band == "Lorentz": 
                Q1 = self.width_band_l
                Q2 = 0
                
            elif self.type_of_band == "Gauss":
                Q1 = self.width_band_g
                Q2 = 0
                
            else:
                logging.error("Wrong curve type: Gauss/Lorentz/Voigt")
                raise Exception("Wrong curve type: Gauss/Lorentz/Voigt")
            
            if progress_bar:
                progress_bar['value'] = 30
                self.application_gui.update_idletasks()
            
            if self.ir_raman != self.name_obw_2 and self.ir_raman != self.name_obw_1:        
                
                self.raman_envelpe = Envelope(self.raman, self.nr_points, minimum, maximum, max_raman_intensity)
                self.ir_envelpe = Envelope(self.ir, self.nr_points, minimum, maximum, max_ir_intensity)
                
                
                list_raman = [self.raman_envelpe, self.type_of_band, Q1, Q2, self.proportional_to_height]
                list_ir = [self.ir_envelpe, self.type_of_band, Q1, Q2, self.proportional_to_height]
                
                with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
                    f_1 = executor.submit(process_envelpe, list_raman)
                    f_2 = executor.submit(process_envelpe, list_ir)
                    self.raman_envelpe, self.raman_envelpe_dt = f_1.result()
                    self.ir_envelpe, self.ir_envelpe_dt = f_2.result()

        
            if self.ir_raman != self.name_obw_2 and self.ir_raman == self.name_obw_1:
                self.raman_envelpe = Envelope(self.raman, self.nr_points, minimum, maximum, max_raman_intensity)\
                    .do_envelope(self.type_of_band, Q1, Q2, proportional_to_height = self.proportional_to_height)
                    
                self.raman_envelpe_dt = self.raman_envelpe.transpose()
                logging.info("raman envelope done")
                
            if progress_bar:
                progress_bar['value'] = 60
                self.application_gui.update_idletasks()
                
            if self.ir_raman != self.name_obw_1 and self.ir_raman == self.name_obw_2:
                self.ir_envelpe = Envelope(self.ir, self.nr_points, minimum, maximum, max_ir_intensity)\
                    .do_envelope(self.type_of_band, Q1, Q2, proportional_to_height = self.proportional_to_height)
                    
                self.ir_envelpe_dt = self.ir_envelpe.transpose()
                logging.info("IR envelope done")
                
            if progress_bar:
                progress_bar['value'] = 100
                self.application_gui.update_idletasks()
        
            #code procesing np.array to dataframe 
            if self.ir_raman == self.name_obw_1:
                df = pd.DataFrame(self.raman_envelpe_dt, columns=['cm-1', 'Raman'])
                
            elif self.ir_raman == self.name_obw_2:
                df = pd.DataFrame(self.ir_envelpe_dt, columns=['cm-1', 'IR']) 
            else:
                array_to_dt = np.hstack((self.ir_envelpe_dt, self.raman_envelpe_dt))
                df = pd.DataFrame(array_to_dt, columns=['cm-1', 'IR', 'cm-1', 'Raman'])
                        
                            
            self.results = Results(df, wyniki_ir = self.ir_envelpe, wyniki_raman = self.raman_envelpe)
            
        except:
            logging.error("Error!")
            tk.messagebox.showerror(message='Error!', title='Warning!')
    
    def save_envelopes(self, path):

        self.results.save_data(path)
        
        
    def return_figs(self):
        if self.ir_raman == self.name_obw_1:
            fig_ir, fig_raman = self.results.print_fig(intensity_raman = self.raman)
            
        elif self.ir_raman == self.name_obw_2:
            fig_ir, fig_raman = self.results.print_fig(intensity_ir = self.ir)
            
        else:
            fig_ir, fig_raman = self.results.print_fig(intensity_ir = self.ir, intensity_raman = self.raman)
        
        return fig_ir, fig_raman
        
        