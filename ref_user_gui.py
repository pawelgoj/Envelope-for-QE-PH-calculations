"""
@author: Pawel Goj
"""
import tkinter as tk
import tkinter.font as font
from tkinter import BaseWidget, Misc, ttk
from tkinter import filedialog 
from tkinter.messagebox import showinfo
from abc import ABC
from program.cord_rand import *
from program.config import Config

from program.menu_functions import MenuFunctions

PATH_TO_IMAGES = Config.PATH_TO_IMAGE


class Navigation:
    @staticmethod 
    def use_mouse_wheel(event):
        second_canvas.yview_scroll(int(-1*(event.delta/120)), "units")


class CallBacks: 
    @staticmethod
    #funkcja pobierając ścieżkę do folderu
    def get_folder_path():
        app.set_directory(filedialog.askdirectory())

    @staticmethod
    #Funkcja wykonuje program
    def make_folders():
        instructions_2.config(text= "I'm working on it!!!")
        progress_bar['value'] = 0
        application_gui.update_idletasks()
        

        try:
            name_of_folder = application_gui.input_1.get()
            prefix_sub_folders = application_gui.input_2.get()

            glass_formula = application_gui.input_glass_formula.get()
            density_of_glass = application_gui.input_density_of_glass.get()
            charge_of_atoms = application_gui.input_charge_of_atoms.get()

            if name_of_folder == '' or prefix_sub_folders == '' or\
                glass_formula == '' or density_of_glass == '' or charge_of_atoms == '':
                raise Exception('Not all the necessary inputs have been entered!')
            many_glasses = not one_glass.get()

            try:
                number_of_atoms = int(application_gui.input_number_of_atoms.get())
            except:
                raise Exception('Not all the necessary inputs have been entered!')

            if many_glasses:
                try:
                    start_x = float(application_gui.input_start_x.get())
                    step_x = float(application_gui.input_step_x.get()) 
                    number_of_step =  int(application_gui.input_number_of_steps.get())
                except:
                    raise Exception('Not all the necessary inputs have been entered!')
                app.make_folders_with_data_for_lammps(name_of_folder, prefix_sub_folders, glass_formula,
                many_glasses, number_of_atoms, density_of_glass, charge_of_atoms, start_x, step_x, number_of_step, progress_bar, application_gui)
            
            else: 
                app.make_folders_with_data_for_lammps(name_of_folder, prefix_sub_folders, glass_formula,
                many_glasses, number_of_atoms, density_of_glass, charge_of_atoms, quantity_of_materials=1, progress_bar=progress_bar, application_gui=application_gui)
            
            showinfo('Info', 'Directory with files has been created!!!!')
            instructions_2['text'] = 'Directory with files has been created!!!'

        except BaseException as err:

            showinfo('Show error', f'{err}')
            

class WidgetInApp(ABC, BaseWidget):
    def add_mouse_wheel_interaction(self):
        self.bind('<MouseWheel>', Navigation.use_mouse_wheel)


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
    """ Button in aplication CFWDFL"""

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


class MessageInApp(tk.Message, WidgetInApp):
    def __init__(self, root: Misc, *args, fg: str='white', **kwargs):
        super().__init__(root, *args, fg=fg, **kwargs)
        self.add_mouse_wheel_interaction()


class CanvaInApp(tk.Canvas, WidgetInApp):
    def __init__(self, root: Misc, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self.add_mouse_wheel_interaction()


class AppliactionCFWDFL(tk.Tk):
    """Object is a aplication window
    """


    def __init__(self, background_color: str = '#1E1E1E', regular_font_size: int = 12, heading_font_size: int = 14, \
        message_box_font_size: int = 12, paddings: dict = {'padx': 6, 'pady': 6}):
        
        self.background_color_value = background_color
        self.background_color = {'bg': background_color}
        super().__init__()
        #Title of application
        self.title('CDFFL')
        self.appname = 'CFWDFL'
        #ico
        self.iconphoto(False, tk.PhotoImage(file=(PATH_TO_IMAGES + 'image/icon.png')))

        self.resizable(width=True, height=True)
        self.windowingsystem = 'win32'
        self.geometry("600x600")
        #fonts 
        self.regular_font_size = font.Font(size = regular_font_size)
        self.heading_font_size = font.Font(size = heading_font_size)
        self.message_box_font_size = font.Font(size = message_box_font_size)
        self.paddings = paddings
        self.createWidgets()


    def createWidgets(self) -> None:
        #Fonts in widgets 
        font_1 = self.heading_font_size 
        font_2 = self.regular_font_size
        fontmessage_box = self.message_box_font_size

        paddings = self.paddings 

        background_color = self.background_color

        self.style = ttk.Style()
        self.style.configure('TSeparator', background=self.background_color_value)
        self.style.configure('TPanewindow', background=self.background_color_value)
        #menu bar 
        menubar = tk.Menu(self)
        self['menu'] = menubar
        menu_help = tk.Menu(self)
        menu_other_projects = tk.Menu(self)
        menubar.add_cascade(menu=menu_other_projects, label='Other projects')
        menubar.add_cascade(menu=menu_help, label='Help')
        menu_other_projects.add_command(label='Envelope-for-dynmat-quantum-esspreso',
            command=MenuFunctions.show_project_EFDQE)
            
        menu_help.add_command(label='Documentation', command=MenuFunctions.show_documentation)

        #Main farame in GUI fills the application window completely
        self.main_frame = tk.Frame(self)
        main_frame = self.main_frame
        main_frame.pack(side='left', anchor='nw', fill='both', expand=1)

        self.main_canvas = CanvaInApp(main_frame, background_color , highlightthickness=0) 
        
        # second_canvas is global variable used in callback function: Navigation.use_mouse_wheel - which 
        # changed position of this canvas
        global second_canvas
        main_canvas = self.main_canvas
        
        
        #This canvas have dimension equal to content in it and don't fills main canvas
        self.second_canvas = CanvaInApp(main_canvas, background_color, highlightthickness=0, width=763, height=705)
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

        self.frame = FrameInApp(second_canvas, background_color)
        self.frame.grid(columnspan=6, rowspan=11, sticky = 'nw')

        #create window to display frame grid
        second_canvas.create_window((0,0), window=self.frame, anchor="nw", height=705)

        frame = self.frame

        self.instructions = LabelInApp(frame, 0, 0, 6,\
            txt="""The program creates folders with input data for lammps, based on the glass oxide formula. 
            """)

        #First row of buttons 
        self.separator_1 = ttk.Separator(frame, style='TSeparator', orient='horizontal')
        self.separator_1.grid(row = 1, column = 0, columnspan=6, sticky='w')
        self.label1 = LabelInApp(self.separator_1, 1, 0, 3, txt = "Choose the directory "\
             "where files will they be created:")
        self.button_1 = ButtonInApp(self.separator_1, 1, 3, 3, txt = "Directory", function_app =CallBacks.get_folder_path)

        #Second row of buttons 
        self.label_2 = LabelInApp(frame, 2, 0, 3, txt = "Name of folder:")
        self.input_1 = EntryInApp(frame, width=20, font = font_2)
        self.input_1.grid(paddings, sticky = 'w', row = 2, column = 3, columnspan=3)

        #third row of buttons 
        self.label_3 = LabelInApp(frame, 3, 0, 3, txt = "Enter the prefix for subfolders:")
        self.input_2 =  EntryInApp(frame, width=20, font = font_2)
        self.input_2.grid(paddings, sticky = 'w', row = 3, column = 3, columnspan=3)
        global one_glass 
        one_glass = tk.BooleanVar()
        self.check_If_one_glass = CheckbuttonInApp(frame, text='Only one glass', variable = one_glass, onvalue = True, offvalue = False)
        self.check_If_one_glass.grid(paddings, row = 5, column = 0, sticky = 'w', columnspan=3)
        self.separator_2 = ttk.Separator(frame, style='TSeparator', orient='horizontal')

        self.separator_2.grid(row = 4, column = 0, columnspan=6)

        #Instruction for user 
        self.instructions_2 = MessageInApp(frame, width=800, fg='black',  font=fontmessage_box,
            text="The quation of glasses should be written as follows: \n" \
            "  x Na2O (1 - x ) ( 0.3 Fe2O3 0.7 P2O5 ) \n" \
            "\nRemember about spaces!\n" \
            "There are molar ratios in the formula.\n" \
            "If one glass, insert simple equation: \n  eg. 0.3 Fe2O3 0.7 P2O5" )

        self.instructions_2.grid(paddings, row = 5, column = 2, sticky = 'w', columnspan=4)

        #4 row buttons
        self.label_4 = LabelInApp(self.separator_2, 0, 0, 3, txt = "Enter the glass equation:")
        self.input_glass_formula =  EntryInApp(self.separator_2, width=50, font = font_1)
        self.input_glass_formula.grid(paddings, sticky = 'w', row = 0, column = 3, columnspan=3)

        #5 row of buttons
        self.label_frame = LabelFrameInApp(frame, background_color, width=600, height=25, text='If many glasses', font=font_2, fg='white')
        self.label_frame.grid(row=6, column=0, columnspan=6, rowspan=1, sticky = 'w')

        self.label_5 = LabelInApp(self.label_frame, 0, 0, txt = "initial value of x:")
        self.input_start_x =  EntryInApp(self.label_frame, width=10, font = font_2)
        self.input_start_x.grid(paddings, row = 0, column = 1, sticky = 'w')

        self.label_6 = LabelInApp(self.label_frame, 0, 2, txt = "step value:")
        self.input_step_x =  EntryInApp(self.label_frame, width=10, font = font_2)
        self.input_step_x.grid(paddings, row = 0, column = 3, sticky = 'w')

        self.label_7 = LabelInApp(self.label_frame, 0, 4, txt = "quantity of materials:")
        self.input_number_of_steps =  EntryInApp(self.label_frame, width=10, font = font_2)
        self.input_number_of_steps.grid(paddings, row = 0, column = 5, sticky = 'w')

        #S6 row of buttons
        self.frame_3 = FrameInApp(frame, background_color,  width=600, height=25)
        self.frame_3.grid(row=7, column=0, columnspan=6, rowspan=1, sticky = 'w')
        frame_3 = self.frame_3
        self.label_number_of_atoms = LabelInApp(frame_3, 0, 0, txt = "quantity of atoms in single material:")
        self.input_number_of_atoms =  EntryInApp(frame_3, width=10, font = font_2)
        self.input_number_of_atoms.grid(paddings, row = 0, column = 2, sticky = 'w')

        self.frame_4 = FrameInApp(frame, background_color,  width=600, height=25)
        self.frame_4.grid(row=8, column=0, columnspan=6, rowspan=1, sticky = 'w')

        to_the_cube = b'\xC2\xB3'
        to_the_cube = to_the_cube.decode()
        self.label_density_of_glass = LabelInApp(self.frame_4, 0, 0, txt = f'list of density of glasses [g/cm{to_the_cube}]:')

        self.input_density_of_glass =  EntryInApp(self.frame_4, width=50, font = font_2)
        self.input_density_of_glass.grid(paddings, row = 0, column = 2, sticky = 'w')
        self.input_density_of_glass.insert(0, "eg. 3.14, 3.15")

        self.labelChargeOfAtoms = LabelInApp(self.frame_4, 1, 0, txt = f'charges of atoms for simulations:')
        self.input_charge_of_atoms =  EntryInApp(self.frame_4, width=50, font = font_2)
        self.input_charge_of_atoms.grid(paddings, row= 1, column=2, sticky='w')
        self.input_charge_of_atoms.insert(0, "eg. Fe: 3, P: 5")


        #Comunications:
        self.comunicates_to_user_frame = FrameInApp(frame, background_color,  width=600)
        self.comunicates_to_user_frame.grid(row=9, column=0, columnspan=6, rowspan=1)
        global instructions_2
        instructions_2 = MessageInApp(self.comunicates_to_user_frame, background_color, width=800, font=font_2, text="")
        instructions_2.grid(paddings, row = 0, column = 0, columnspan=6, rowspan=1)
        global progress_bar
        progress_bar = ttk.Progressbar(self.comunicates_to_user_frame, orient='horizontal', length=200, mode='determinate')
        progress_bar.grid(paddings, row = 1, column = 0, columnspan=6, rowspan=1)


        #Last row of buttons 
        self.Start_button = ButtonInApp(frame, 10, 0, 3, 'E', txt = "Start", function_app = CallBacks.make_folders)
        self.quit_button = ButtonInApp(frame, 10, 3, 3, txt = "Exit", function_app = self.quit)
        self.frame_6 = FrameInApp(frame, background_color,  width=600, height=40)
        self.frame_6.grid(row=11, column=0, columnspan=6, rowspan=1)


if __name__ == '__main__': 
    global application_gui
    application_gui = AppliactionCFWDFL()
    app = App()

else: 
    print(__name__)
    raise Exception('The __name__ == __main__ !!!!!')

application_gui.mainloop()

