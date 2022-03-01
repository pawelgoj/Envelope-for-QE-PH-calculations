import tkinter as tk
import tkinter.font as font
from tkinter import BaseWidget, Frame, Misc, ttk
from tkinter import filedialog 
from tkinter.messagebox import showinfo
from menu_functions import MenuFunctions
from pandas import DataFrame

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
import matplotlib.pyplot as plt

from abc import ABC


class Navigation:
    @staticmethod 
    def use_mouse_wheel(event):
        second_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

class NavigationToolbar(NavigationToolbar2Tk):
    def set_message(self, s):
        pass       
        
class WidgetInApp(ABC, BaseWidget):
    def add_mouse_wheel_interaction(self):
        self.bind('<MouseWheel>', Navigation.use_mouse_wheel)
        
class CanvasForFig(FigureCanvasTkAgg):
    def __init__(self, *args, **kwargs):
        super().__init__( *args, **kwargs)
        
class LabelInApp(tk.Label, WidgetInApp):
    """Label in aplication CFWDFL"""

    def __init__(self, root: Misc, row: int, column: int,\
        columspan: int = 1, txt: str = "text in label"):
        font_1 = font.Font(size = 12)
        paddings = {'padx': 8, 'pady': 8}
        background_color = {'bg': '#1E1E1E'}
        super().__init__(root, background_color, text = txt, fg='white', font=font_1, anchor='nw')
        self.grid(paddings, sticky='w', row=row, column=column, columnspan=columspan)
        self.add_mouse_wheel_interaction()


class ButtonInApp(tk.Button, WidgetInApp):
    """ Button in aplication"""

    def __init__(self, root: Misc, row: int, column: int,\
        columspan: int = 1, sticky='w', txt: str = "text on button",\
        function_app = None):

        font_1 = font.Font(size = 12)
        paddings = {'padx': 5, 'pady': 5}
        background_color_and_border = {'bg': '#403332', 'bd': 4}

        super().__init__(root, background_color_and_border, text = txt,\
            fg='white', font = font_1, command = function_app)
        self.grid(paddings, sticky=sticky, row=row, column=column, columnspan=columspan)
        self.add_mouse_wheel_interaction()


class EntryInApp(tk.Entry, WidgetInApp):
    def __init__(self, root: Misc, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self.add_mouse_wheel_interaction()


class FrameInApp(tk.Frame, WidgetInApp):
    def __init__(self, root: Misc, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self.add_mouse_wheel_interaction()


class LabelFrameInApp(tk.LabelFrame, WidgetInApp):
    def __init__(self, root: Misc, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self.add_mouse_wheel_interaction()


class CheckbuttonInApp(tk.Checkbutton, WidgetInApp):
    def __init__(self, root: Misc, *args, **kwargs):
        font_1 = font.Font(size = 14)
        attributes = {'padx': 6, 'pady': 6, 'bg': '#1E1E1E', 'selectcolor': '#1E1E1E',\
            'activebackground': '#1E1E1E', 'fg': 'white'}
        super().__init__(root, attributes, font = font_1,  *args, **kwargs)
        self.add_mouse_wheel_interaction()
        
class RadioButtonInApp(tk.Radiobutton, WidgetInApp):
    def __init__(self, root: Misc, *args, **kwargs):
        font_1 = font.Font(size = 12)
        attributes = {'padx': 6, 'pady': 6, 'bg': '#1E1E1E', 'selectcolor': '#1E1E1E',\
            'activebackground': '#1E1E1E', 'fg': 'white'}
        super().__init__(root, attributes, font = font_1,  *args, **kwargs)
        self.add_mouse_wheel_interaction()


class MessageInApp(tk.Message, WidgetInApp):
    def __init__(self, root: Misc, *args, fg: str='white', **kwargs):
        super().__init__(root, *args, fg=fg, **kwargs)
        self.add_mouse_wheel_interaction()


class CanvaInApp(tk.Canvas, WidgetInApp):
    def __init__(self, root: Misc, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self.add_mouse_wheel_interaction()
        
        
class MakeEnvelope(tk.Tk):
    
    def __init__(self, background_color: str = '#1E1E1E', regular_font_size: int = 12, heading_font_size: int = 14, \
        message_box_font_size: int = 12, paddings: dict = {'padx': 6, 'pady': 6}):
        
        self.background_color_value = background_color
        self.background_color = {'bg': background_color}
        super().__init__()
        
        #Title of application
        self.title('Envelope for QE PH calculations')
        self.appname = 'Envelope for QE PH calculations'
        
        #ico
        #self.iconphoto(False, tk.PhotoImage(file=(PATH_TO_IMAGES + 'image/icon.png')))

        self.resizable(width=True, height=True)
        self.windowingsystem = 'win32'
        self.geometry("600x600")
        
        #fonts 
        self.regular_font_size = font.Font(size = regular_font_size)
        self.heading_font_size = font.Font(size = heading_font_size)
        self.message_box_font_size = font.Font(size = message_box_font_size)
        self.paddings = paddings
        
        self.createWidgets()
    
    def createWidgets(self):
        
        #menu bar 
        
        menubar = tk.Menu(self)
        self['menu'] = menubar
        menu_help = tk.Menu(self)
        menu_other_projects = tk.Menu(self)
        menubar.add_cascade(menu=menu_other_projects, label='Other projects')
        menubar.add_cascade(menu=menu_help, label='Help')
        
        #TODO menu functions 
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
        self.second_canvas = CanvaInApp(main_canvas, self.background_color, highlightthickness=0, width=1300, height=1000)
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
        self.frame.grid(columnspan=2, rowspan=9, sticky = 'nw')

        #create window to display frame grid
        second_canvas.create_window((0,0), window=self.frame, anchor="nw", height=1000)

        self.button_input_file = ButtonInApp(self.frame, 0, 0, 1, txt='Chose input file')
        self.button_input_file = ButtonInApp(self.frame, 0, 1, 1, txt='Save files')
        
        self.label_spectra_type = LabelInApp(self.frame, 1, 0, txt='Envelope for:')
        self.frame_chose_type_of_spectra = FrameInApp(self.frame, self.background_color)
        
        self.frame_chose_type_of_spectra.grid(column=1, row=1, sticky = 'nw')
        
        self.ir_label = LabelInApp(self.frame_chose_type_of_spectra, 0, 0, txt='IR')    
        self.check_button_ir = CheckbuttonInApp(self.frame_chose_type_of_spectra)
        self.check_button_ir.grid(column=1, row=0, sticky = 'w')
        self.raman_label = LabelInApp(self.frame_chose_type_of_spectra, 0, 2, txt='Raman')
        self.check_button_raman = CheckbuttonInApp(self.frame_chose_type_of_spectra)
        self.check_button_raman.grid(column=3, row=0, sticky = 'w') 
        
        self.label_band_type = LabelInApp(self.frame, 1,1, txt='Band type:')
        self.frame_band_type = FrameInApp(self.frame, self.background_color)
        self.frame_band_type.grid(column=3, row=1, sticky = 'w')
        self.radio_button_gauss = RadioButtonInApp(self.frame_band_type, text='Gauss')
        self.radio_button_gauss.grid(column=0, row=0, sticky = 'w')
        self.radio_button_lorentz = RadioButtonInApp(self.frame_band_type, text='Lorentz')
        self.radio_button_lorentz.grid(column=1, row=0, sticky = 'w')
        self.radio_button_voigt = RadioButtonInApp(self.frame_band_type, text='Voigt')
        self.radio_button_voigt.grid(column=2, row=0, sticky = 'w')
        
        self.label_standard_deviation = LabelInApp(self.frame, 3, 0, txt='Standard deviation:')
        self.entry_standard_deviation = EntryInApp(self.frame)
        self.entry_standard_deviation.grid(column=1, row=3, sticky = 'w')
        self.label_scale_param = LabelInApp(self.frame, 4, 0, txt='Scale param:')
        self.entry_scale_param = EntryInApp(self.frame)
        self.entry_scale_param.grid(column=1, row=4, sticky = 'w')
        
        self.label_number_of_points = LabelInApp(self.frame, 5, 0, txt='Number of points in envelope:')
        self.entry_number_of_points = EntryInApp(self.frame)
        self.entry_number_of_points.grid(column=1, row=5, sticky = 'w')

        progress_bar = ttk.Progressbar(self.frame, orient='horizontal', length=400, mode='determinate')
        progress_bar.grid(row = 6, column = 0, columnspan=2, rowspan=1, pady=20)
        
        self.frame_raman_fig = FrameInApp(self.frame, self.background_color)
        self.frame_raman_fig.grid(column=0, row=7)
        self.label_raman_fig = LabelInApp(self.frame_raman_fig, 0, 0, txt='Raman')
        
        self.frame_ir_fig = FrameInApp(self.frame, self.background_color)
        self.frame_ir_fig.grid(column=1, row=7)
        self.label_ir_fig = LabelInApp(self.frame_ir_fig, 0, 0, txt='IR') 
        
        fig, ax = plt.subplots(figsize=(5, 3))
        
        
        #example data 
        data1 = {'Country': ['US','CA','GER','UK','FR'],
        'GDP_Per_Capita': [45000,42000,52000,49000,47000]}
        df1 = DataFrame(data1,columns=['Country','GDP_Per_Capita'])

        

        df1 = df1[['Country','GDP_Per_Capita']].groupby('Country').sum()
        df1.plot(kind='bar', legend=True, ax=ax)
        ax.set_title('Country Vs. GDP Per Capita')
             
        self.canvas_figure_ir = FigureCanvasTkAgg(fig, master=self.frame_ir_fig) 
        self.canvas_figure_ir.draw()
        self.toolbar_ir = NavigationToolbar(self.canvas_figure_ir, self.frame_ir_fig, pack_toolbar=False)
        self.toolbar_ir.update()
        self.toolbar_ir.grid(column=0, row=2, pady=20)
        self.canvas_figure_ir.get_tk_widget().grid(column=0, row=1, padx=20)
        
        self.canvas_figure_raman = FigureCanvasTkAgg(fig, master=self.frame_raman_fig) 
        self.canvas_figure_raman.draw()
        self.toolbar_raman = NavigationToolbar(self.canvas_figure_raman, self.frame_raman_fig, pack_toolbar=False)
        self.toolbar_raman.update()
        self.toolbar_raman.grid(column=0, row=2, pady=20)
        self.canvas_figure_raman.get_tk_widget().grid(column=0, row=1, padx=20)


if __name__ == '__main__': 
    global application_gui
    application_gui = MakeEnvelope()

else: 
    print(__name__)
    raise Exception('The __name__ == __main__ !!!!!')

application_gui.mainloop()       