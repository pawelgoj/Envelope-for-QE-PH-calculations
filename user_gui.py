import tkinter as tk
import tkinter.font as font
from tkinter import BaseWidget, Misc, ttk
from tkinter import filedialog 

import re

from abc import ABC

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
import matplotlib.pyplot as plt

from menu_functions import MenuFunctions
from do_envelope import *

#globals 
file = None

class Navigation:
    @staticmethod 
    def use_mouse_wheel(event):
        second_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
class CallBacks: 
    @staticmethod
    def get_folder_path():
        
        global file
        
        file = filedialog.askopenfile(mode='r')
        check_file_type = file.name
        file = check_file_type
        global file_type 
        if re.search(".txt$", check_file_type):
            file_type = 'txt'
        else:
            file_type = 'dynmat'
            
    @staticmethod
    def make_enevelopes():
        #Envelope for Raman or IR or Both
        self_raman_check = raman_check.get()
        self_ir_check = ir_check.get()
        
        if self_raman_check == False and self_ir_check == False:
            tk.messagebox.showwarning(message='Chose envelope for IR or/and Raman?', title='Warning!')
        progress_bar['value'] = 0
        
        if self_raman_check == True and self_ir_check == True:
            ir_raman = 'Both'
        elif self_raman_check == True:
            ir_raman = 'Raman'
        elif self_ir_check == True:
            ir_raman = 'IR'
        else:
            raise Exception('You do not chose Raman or/and IR!')
            
        self_proportional_check = proportional_check.get()
        self_type_bound = str(type_bound.get())
        
        all_correct = True
        
        if self_type_bound == 'Gauss':
            try:
                self_entry_standard_deviation = float(application_gui.entry_standard_deviation.get())
                self_entry_scale_param = 0
            except:
                tk.messagebox.showwarning(message='Insert value to Entry!', title='Warning!')
                all_correct = False
                
        elif self_type_bound == 'Lorentz':
            try:
                self_entry_scale_param = float(application_gui.entry_scale_param.get())
            except:
                tk.messagebox.showwarning(message='Insert value to Entry!', title='Warning!')
                all_correct = False
                
            self_entry_standard_deviation = 0
        else:
            try:
                self_entry_standard_deviation = float(application_gui.entry_standard_deviation.get())
                self_entry_scale_param = float(application_gui.entry_scale_param.get())

            except:
                tk.messagebox.showwarning(message='Insert value to Entry!', title='Warning!')
                all_correct = False
            
        try:
            self_entry_number_of_points = int(application_gui.entry_number_of_points.get())

        except:
            tk.messagebox.showwarning(message='Insert value to Entry!', title='Warning!')
            all_correct = False
        
        
        if file == None:
            
            tk.messagebox.showwarning(message='Select a data file!', title='Warning!')
            
        elif all_correct == True:
            
            application_gui.label_info.config(text='Wait!')
            progress_bar['value'] = 10
            application_gui.update_idletasks()
            
            do_envelope_object.set_param(file_type, self_type_bound, self_entry_standard_deviation, self_entry_scale_param, 
                                    self_proportional_check, self_entry_number_of_points, file, ir_raman)
            do_envelope_object.make_envelopes(progress_bar=progress_bar)
            
            
            fig_ir, fig_raman = do_envelope_object.return_figs()
            
            application_gui.canvas_figure_ir.config(fig=fig_ir)
            application_gui.canvas_figure_raman.config(fig=fig_raman)
            
            if progress_bar['value'] == 100:
                application_gui.label_info.config(text='Done!')
                
            else:
                application_gui.label_info.config(text='')
                progress_bar['value'] == 0
            
            
        application_gui.update_idletasks()
        
    @staticmethod
    def save_files():
        file_name = filedialog.asksaveasfilename(filetypes=[("text file","*.csv")], defaultextension = "*.csv")

        if file_name:
            try:
                do_envelope_object.save_envelopes(file_name)
            except:
                tk.messagebox.showwarning(message='There is no data to save!', title='Warning!')
                application_gui.update_idletasks()
        
    @staticmethod
    def disable_enable_lorentz_input():
        application_gui.entry_scale_param.config(state='normal')
        application_gui.entry_standard_deviation.config(state='disabled')
    @staticmethod
    def disable_enable_gauss_input():
        application_gui.entry_standard_deviation.config(state='normal')
        application_gui.entry_scale_param.config(state='disabled')
    @staticmethod
    def disable_enable_voigt_input():
        application_gui.entry_scale_param.config(state='normal')
        application_gui.entry_standard_deviation.config(state='normal')
        
    #callbacks for buttons change figure 
    @staticmethod
    def press_change_button_input_fig(event):
        global image_file_button_input_press
        application_gui.button_input_file.config(image=image_file_button_input_press)
        application_gui.update_idletasks()
        
    @staticmethod
    def reless_change_button_input_fig(event):
        global image_file_button_input_rellase
        application_gui.button_input_file.config(image=image_file_button_input_rellase)
        application_gui.update_idletasks()
        
    @staticmethod
    def press_change_button_calculate_fig(event):
        global image_file_button_calculate_press
        application_gui.button_start_process.config(image=image_file_button_calculate_press)
        application_gui.update_idletasks()
        
    @staticmethod
    def reless_change_button_calculate_fig(event):
        global image_file_button_calculate_rellase
        application_gui.button_start_process.config(image=image_file_button_calculate_rellase)
        application_gui.update_idletasks()
        
    @staticmethod
    def press_change_button_export_data_fig(event):
        global image_file_button_export_data_press
        application_gui.button_export_data.config(image=image_file_button_export_data_press)
        application_gui.update_idletasks()
        
    @staticmethod
    def reless_change_button_export_data_fig(event):
        global image_file_button_export_data_rellase
        application_gui.button_export_data.config(image=image_file_button_export_data_rellase)
        application_gui.update_idletasks()
        
            
            
#switch off message. 
class NavigationToolbar(NavigationToolbar2Tk):
    def set_message(self, s):
        pass  
    
class FigureCanvas:
    def __init__(self, fig, master, row: int, column: int):
        
        self.master = master
        self.row = row 
        self.column = column
        
        self.figure = FigureCanvasTkAgg(fig, master=master)
        self.figure.draw()
        
        self.toolbar = NavigationToolbar(self.figure, master, pack_toolbar=False)
        self.toolbar.update()
        self.toolbar.grid(column=0, row=(row+1), pady=20)
        
        self.canvas_fig = self.figure.get_tk_widget()
        self.canvas_fig.bind('<MouseWheel>', Navigation.use_mouse_wheel)
        self.canvas_fig.grid(column=column, row=row, padx=20)
        
    def config(self, fig=None):
        
        self.canvas_fig.destroy()
        self.figure = FigureCanvasTkAgg(fig, master= self.master)
        self.figure.draw()
        
        self.toolbar = NavigationToolbar(self.figure, self.master, pack_toolbar=False)
        self.toolbar.update()
        self.toolbar.grid(column=0, row=(self.row+1), pady=20)
        
        self.canvas_fig = self.figure.get_tk_widget()
        self.canvas_fig.bind('<MouseWheel>', Navigation.use_mouse_wheel)
        self.canvas_fig.grid(column=self.column, row=self.row, padx=20)        
           
         
        
class WidgetInApp(ABC):
    def add_mouse_wheel_interaction(self):
        self.bind('<MouseWheel>', Navigation.use_mouse_wheel)                    
        
class PrograsBarrInApp(WidgetInApp, ttk.Progressbar):
    def __init__(self, *args, **kwargs):
        super().__init__( *args, **kwargs)
        self.add_mouse_wheel_interaction()
                
class LabelInApp(tk.Label, WidgetInApp):
    """Label in aplication CFWDFL"""

    def __init__(self, root: Misc, row: int, column: int,\
        columspan: int = 1, txt: str = "text in label", rowspan: int = 1):
        font_1 = font.Font(size = 11, family='Arial')
        paddings = {'padx': 5, 'pady': 5, 'ipadx': 2}
        background_color = {'bg': '#263238'}
        super().__init__(root, background_color, text = txt, fg='#eceff1', font=font_1, anchor='nw')
        self.grid(paddings, sticky='w', row=row, column=column, columnspan=columspan, rowspan=rowspan)
        self.add_mouse_wheel_interaction()


class ButtonInApp(tk.Button, WidgetInApp):
    """ Button in aplication"""

    def __init__(self, root: Misc, row: int, column: int,\
        columspan: int = 1, sticky='w', txt: str = "text on button",\
        function_app = None, image = None):
        self.image = image
        
        #Configure font of button 
        font_1 = font.Font(size = 11, family='Arial Black')
        paddings = {'padx': 5, 'pady': 5, 'ipadx': 2}
        background_color_and_border = {'bg': '#455a64', 'bd': 2}

        if image != None:
            super().__init__(root, background_color_and_border, \
                fg='#eceff1', font = font_1, text = txt, image = self.image, compound = 'left',\
                    command = function_app)
            self.config(activeforeground= '#263238', activebackground='#eceff1')
        else:
            super().__init__(root, background_color_and_border, text = txt,\
                fg='#eceff1', font = font_1, command = function_app)
        self.grid(paddings, sticky=sticky, row=row, column=column, columnspan=columspan)
        self.add_mouse_wheel_interaction()


class EntryInApp(tk.Entry, WidgetInApp):
    def __init__(self, root: Misc, *args, **kwargs):
        config_entry = {'disabledbackground': '#575757'}
        super().__init__(root, *args, config_entry, **kwargs)
        self.add_mouse_wheel_interaction()


class FrameInApp(tk.Frame, WidgetInApp):
    def __init__(self, root: Misc, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self.add_mouse_wheel_interaction()

class CheckbuttonInApp(tk.Checkbutton, WidgetInApp):
    def __init__(self, root: Misc, *args, **kwargs):
        
        font_1 = font.Font(size = 11, family='Arial')
        attributes = {'padx': 5, 'pady': 5, 'bg': '#263238', 'selectcolor': '#263238',\
            'activebackground': '#263238', 'fg': '#eceff1'}
        super().__init__(root, attributes, font = font_1,  *args, **kwargs)
        self.add_mouse_wheel_interaction()
        
class RadioButtonInApp(tk.Radiobutton, WidgetInApp):
    def __init__(self, root: Misc, *args, **kwargs):
        
        font_1 = font.Font(size = 11, family='Arial')
        attributes = {'padx': 5, 'pady': 5, 'bg': '#263238', 'selectcolor': '#263238',\
            'activebackground': '#263238', 'fg': '#eceff1'}
        super().__init__(root, attributes, font = font_1,  *args, **kwargs)
        self.add_mouse_wheel_interaction()


class MessageInApp(tk.Message, WidgetInApp):
    def __init__(self, root: Misc, *args, fg: str='#eceff1', **kwargs):
        super().__init__(root, *args, fg=fg, **kwargs)
        self.add_mouse_wheel_interaction()


class CanvaInApp(tk.Canvas, WidgetInApp):
    def __init__(self, root: Misc, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self.add_mouse_wheel_interaction()
        
        
class MakeEnvelope(tk.Tk):
    
    def __init__(self, background_color: str = '#263238', regular_font_size: int = 11, heading_font_size: int = 12, \
        message_box_font_size: int = 12, paddings: dict = {'padx': 5, 'pady': 5}):
        
        self.background_color_value = background_color
        self.background_color = {'bg': background_color}
        super().__init__()
        
        #Title of application
        self.title('Envelope for QE PH calculations')
        self.appname = 'Envelope for QE PH calculations'
        
        #ico if true all other pop ups have this ico
        self.iconphoto(True, tk.PhotoImage(file='fig_logo.png'))


        self.resizable(width=True, height=True)
        self.windowingsystem = 'win32'
        self.geometry("1000x800")
        
        #fonts 
        self.regular_font_size = font.Font(size = regular_font_size)
        self.heading_font_size = font.Font(size = heading_font_size)
        self.message_box_font_size = font.Font(size = message_box_font_size)
        self.paddings = paddings
        
        self.createWidgets()
    
    def createWidgets(self):
        #globals 
        global image_file_button_input_press
        image_file_button_input_press = tk.PhotoImage(file = r"plik_dark.png")
        global image_file_button_input_rellase
        image_file_button_input_rellase = tk.PhotoImage(file = r"plik.png")
        
        global image_file_button_calculate_press
        image_file_button_calculate_press = tk.PhotoImage(file = r"proces_dark.png")
        global image_file_button_calculate_rellase
        image_file_button_calculate_rellase = tk.PhotoImage(file = r"proces.png")
        
        global image_file_button_export_data_press
        image_file_button_export_data_press = tk.PhotoImage(file = r"rysunek_dark.png")
        global image_file_button_export_data_rellase
        image_file_button_export_data_rellase = tk.PhotoImage(file = r"rysunek.png")
        
        #menu bar 
        
        menubar = tk.Menu(self)
        self['menu'] = menubar
        menu_help = tk.Menu(self)
        menu_other_projects = tk.Menu(self)
        menubar.add_cascade(menu=menu_other_projects, label='Other projects')
        menubar.add_cascade(menu=menu_help, label='Help')
        
        #menu functions 
        menu_other_projects.add_command(label='CDFFL',
            command=MenuFunctions.show_project_CDFFL)
            
        menu_help.add_command(label='Documentation', command=MenuFunctions.show_documentation)
        
        #Main farame in GUI fills the application window completely
        self.main_frame = tk.Frame(self)
        main_frame = self.main_frame
        main_frame.pack(side='left', anchor='nw', fill='both', expand=1)

        self.main_canvas = CanvaInApp(main_frame, self.background_color , highlightthickness=0) 
        
        # second_canvas is global variable used in callback function: Navigation.use_mouse_wheel - which 
        # changed position of this canvas
        global second_canvas
        main_canvas = self.main_canvas
        
        
        #This canvas have dimension equal to content in it and don't fills main canvas
        self.second_canvas = CanvaInApp(main_canvas, self.background_color, highlightthickness=0, width=1300, height=850)
        second_canvas = self.second_canvas
        

        #command scroll second_canvas view in y direction
        self.scroll_bar = tk.Scrollbar(main_frame, orient='vertical', command=second_canvas.yview)
        
        #command scroll second_canvas view in x direction
        self.scroll_bar_x = tk.Scrollbar(main_frame, orient='horizontal', command=second_canvas.xview)
        scroll_bar = self.scroll_bar

        #pack elements in main frame
        #In GUI in main frame are in left canvas shows GUI content and on the right scrollbar 
        scroll_bar.pack(side='right', fill='y', anchor='ne')
        self.scroll_bar_x.pack(side='bottom', anchor='w', fill='x', after=scroll_bar)
        main_canvas.pack(side='left', anchor='nw', fill='both', expand=1, after=self.scroll_bar_x)
        second_canvas.pack(side='top', anchor='nw', fill='none', expand=0)

        #function determines size and position of scroll bar elevator
        second_canvas.config(yscrollcommand=scroll_bar.set, xscrollcommand=self.scroll_bar_x.set)


        #event is event get size and position of canvas, scroll region, bbox is list of xmin, xmax, ymin, ymax
        #of canvas 
        second_canvas.bind('<Configure>', lambda e: second_canvas.config(scrollregion = second_canvas.bbox("all")))

        self.frame = FrameInApp(second_canvas, self.background_color)
        self.frame.grid(sticky = 'nw')

        #create window to display frame grid
        second_canvas.create_window((0,0), window=self.frame, anchor="nw", height=850)
        
        self.frame_with_buttons = FrameInApp(self.frame, self.background_color)
        self.frame_with_buttons.grid(column=0, row=0, sticky='nw', pady=5)
        image_file = tk.PhotoImage(file = r"plik.png")
        image_file = image_file.subsample(1, 1)
        self.button_input_file = ButtonInApp(self.frame_with_buttons, 0, 0, 1, txt='Chose input file', image=image_file, function_app = CallBacks.get_folder_path)
        self.button_input_file.bind('<ButtonPress-1>', CallBacks.press_change_button_input_fig)
        self.button_input_file.bind('<ButtonRelease-1>', CallBacks.reless_change_button_input_fig)
        
        self.frame_with_options= FrameInApp(self.frame, self.background_color)
        self.frame_with_options.grid(row=1, column=0, sticky='nw')
        
        self.frame_chose_type_of_spectra = FrameInApp(self.frame_with_options, self.background_color, 
                                                      highlightthickness=2, highlightbackground='#cfd8dc')
        self.frame_chose_type_of_spectra.grid(column=0, row=0, sticky = 'nw')
        self.label_spectra_type = LabelInApp(self.frame_chose_type_of_spectra, 0, 0, txt='Envelope for:')
        
        
        global raman_check 
        global ir_check 
        raman_check = tk.BooleanVar()
        ir_check = tk.BooleanVar() 
        self.check_button_ir = CheckbuttonInApp(self.frame_chose_type_of_spectra, text='IR',
                                                variable=ir_check, onvalue = True, offvalue = False)
        self.check_button_ir.grid(column=1, row=0, sticky = 'w')
        self.check_button_raman = CheckbuttonInApp(self.frame_chose_type_of_spectra, text='Raman',
                                                   variable=raman_check, onvalue = True, offvalue = False)
        self.check_button_raman.grid(column=2, row=0, sticky = 'w') 

        
        self.frame_with_bond_type = FrameInApp(self.frame_with_options, self.background_color,
                                                highlightthickness=2, highlightbackground='#cfd8dc')
        self.frame_with_bond_type.grid(column=3, row=0, sticky='w')
        self.label_band_type = LabelInApp(self.frame_with_bond_type, 0,0, txt='Band type:')
        self.frame_band_type = FrameInApp(self.frame_with_bond_type, self.background_color)
        self.frame_band_type.grid(column=1, row=0, sticky = 'w')
        
        global type_bound 
        type_bound = tk.StringVar() 
        self.radio_button_gauss = RadioButtonInApp(self.frame_band_type, text='Gauss', 
                                                   variable=type_bound, value='Gauss', state='normal',
                                                       command=CallBacks.disable_enable_gauss_input)
        self.radio_button_gauss.grid(column=0, row=0, sticky = 'w')

        self.radio_button_lorentz = RadioButtonInApp(self.frame_band_type, text='Lorentz', 
                                                     variable=type_bound, value='Lorentz', state='normal',
                                                        command=CallBacks.disable_enable_lorentz_input)
        self.radio_button_lorentz.grid(column=1, row=0, sticky = 'w')

        self.radio_button_voigt = RadioButtonInApp(self.frame_band_type, text='Voigt', 
                                                   variable=type_bound, value='Voigt', state='normal',
                                                   command=CallBacks.disable_enable_voigt_input)
        self.radio_button_voigt.grid(column=2, row=0, sticky = 'w')
        self.radio_button_gauss.select()
        
        global proportional_check 
        proportional_check = tk.BooleanVar()
        
        self.frame_proportional_to_intensity = FrameInApp(self.frame_with_options, self.background_color, 
                                                          highlightthickness=2, highlightbackground='#cfd8dc')
        self.frame_proportional_to_intensity.grid(column=4, row=0, sticky='w')

        self.check_button_proportional_to_intensity = CheckbuttonInApp(self.frame_proportional_to_intensity, 
                                                                        text='Proportional to intensity',
                                                                        variable = proportional_check,
                                                                        onvalue = True, offvalue = False)
        self.check_button_proportional_to_intensity.grid(column=0, row=0, sticky='w')
        
        
        
        
        self.frame_with_image = FrameInApp(self.frame, self.background_color)
        self.frame_with_image.grid(column=0, row=3, sticky='nw')
        
        self.photo_logo_big = tk.PhotoImage(file = r"fig_logo_white.png")
        self.label_number_of_points = LabelInApp(self.frame_with_image, 0, 1, txt='', rowspan=4)
        self.label_number_of_points.config(image=self.photo_logo_big)
        
        self.frame_with_parameters_for_band = FrameInApp(self.frame_with_image, self.background_color)
        self.frame_with_parameters_for_band.grid(column=0, row=0, sticky='nw')
        self.label_standard_deviation = LabelInApp(self.frame_with_parameters_for_band, 0, 0,
                                                   txt='Standard deviation:')
        self.entry_standard_deviation = EntryInApp(self.frame_with_parameters_for_band)
        self.entry_standard_deviation.grid(column=1, row=0, sticky = 'w')
        self.label_scale_param = LabelInApp(self.frame_with_parameters_for_band, 0, 2, txt='Scale param:')
        self.entry_scale_param = EntryInApp(self.frame_with_parameters_for_band)
        self.entry_scale_param.grid(column=3, row=0, sticky = 'w')
        self.entry_scale_param.config(state='disabled')
        
        self.label_number_of_points = LabelInApp(self.frame_with_parameters_for_band, 1, 0, 
                                                 txt='Number of points in envelope:')
        self.entry_number_of_points = EntryInApp(self.frame_with_parameters_for_band)
        self.entry_number_of_points.grid(column=1, row=1, sticky = 'w')

        self.frame_precess_button = FrameInApp(self.frame_with_image, self.background_color)
        self.frame_precess_button.grid(column=0, row=1, sticky='w')
        image_process = tk.PhotoImage(file = r"proces.png")
        image_process = image_process.subsample(1, 1)
        self.button_start_process = ButtonInApp(self.frame_precess_button, 0, 0, 1, 
                                                txt='Calculate envelope', image=image_process, 
                                                function_app = CallBacks.make_enevelopes)
        
        self.button_start_process.bind('<ButtonPress-1>', CallBacks.press_change_button_calculate_fig)
        self.button_start_process.bind('<ButtonRelease-1>', CallBacks.reless_change_button_calculate_fig)
        
        photo = tk.PhotoImage(file = r"rysunek.png")
        photoimage = photo.subsample(1, 1)
        self.button_export_data = ButtonInApp(self.frame_precess_button, 0, 1, 1, txt='Export data',  
                                            image=photoimage, function_app =CallBacks.save_files)

        self.button_export_data.bind('<ButtonPress-1>', CallBacks.press_change_button_export_data_fig)
        self.button_export_data.bind('<ButtonRelease-1>', CallBacks.reless_change_button_export_data_fig)
        
        self.progres_label = LabelInApp(self.frame_with_image, 2, 0, txt='Progress:')
        
        self.frame_with_progress_bar = FrameInApp(self.frame_with_image, self.background_color)
        self.frame_with_progress_bar.grid(row = 3, column = 0, sticky='w')
        
        global progress_bar
        #configure style progres barr
        style_progressbar = ttk.Style()
        style_progressbar.theme_use('default')
        style_progressbar.configure('blue.Horizontal.TProgressbar', foreground='#abe5a8', background='#4cd87d')
        
        progress_bar = PrograsBarrInApp(self.frame_with_progress_bar, orient='horizontal',
                                        length=400, mode='determinate', style='blue.Horizontal.TProgressbar')
        progress_bar.grid(row = 0, column = 0, pady=5, sticky='w', padx=20)

        
        self.label_info = LabelInApp(self.frame_with_progress_bar, 0, 1, 1, txt=' ')
        
        self.frame_with_figs = FrameInApp(self.frame, self.background_color)
        self.frame_with_figs.grid(row=7, column=0, sticky='nw')
        
        self.frame_raman_fig = FrameInApp(self.frame_with_figs, self.background_color)
        self.frame_raman_fig.grid(column=0, row=0, columnspan=1)
        self.label_raman_fig = LabelInApp(self.frame_raman_fig, 0, 0, txt='Raman')
        
        self.frame_ir_fig = FrameInApp(self.frame_with_figs, self.background_color)
        self.frame_ir_fig.grid(column=1, row=0, columnspan=1)
        self.label_ir_fig = LabelInApp(self.frame_ir_fig, 0, 0, txt='IR') 
        
        
        fig1, ax1 = plt.subplots(figsize=(4.5, 3.5))
        fig2, ax2 = plt.subplots(figsize=(4.5, 3.5))
        

        self.canvas_figure_ir = FigureCanvas(fig1, self.frame_ir_fig, 1, 0) 

        self.canvas_figure_raman = FigureCanvas(fig2, self.frame_raman_fig, 1, 0) 
            

if __name__ == '__main__': 
    global application_gui
    application_gui = MakeEnvelope()
    do_envelope_object = DoEnvelope(application_gui)
    application_gui.mainloop() 
else: 
    print(__name__)
    raise Exception('The __name__ == __main__ !!!!!')

      