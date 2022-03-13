"""
@author: Pawel Goj
Use WinAppDriver 1.2.1 + Appium-Python-Client 1.3
Leater versions of Appium-Python-Client not work properly with WinAppDriver 1.2.1
"""


from appium import webdriver
from selenium.webdriver.common.keys import Keys
import allure
from allure_commons.types import AttachmentType
import pytest
import os 
import base64
from PIL import Image
from io import BytesIO
import imagehash
import time



class PreconditionsGui:
    @pytest.fixture()
    def setup(self):
        
        self.file_test_path = "D:/Praca/Symulacje/Narzedzia/Moje/Envelope_for_QE/Envelope-for-dynmat-quantum-esspreso/Test_data"
        self.app_path = r'D:/Praca/Symulacje/Narzedzia/Moje/Envelope_for_QE/Envelope-for-dynmat-quantum-esspreso/'\
            r'Envelope for QE PH calculations/Envelope for QE PH calculations.exe'
        self.file_test_dynmat = r'dynmatAlPO3_3.out'
        self.file_test_txt = r'Dane_2.txt'
        self.new_file = r'wyniki.txt'
        self.path_to_new_file = r'D:/Praca/Symulacje/Narzedzia/Moje/Envelope_for_QE/Envelope-for-dynmat-quantum-esspreso/'\
            r'Test_data/wyniki.txt'
        self.to_check_text_warning_window_chose_envelope = 'Chose envelope for IR or/and Raman?'
            
        if os.path.isfile(self.path_to_new_file) == True:
            os.remove(self.path_to_new_file)
        
        self.driver = webdriver.Remote(
            command_executor='http://127.0.0.1:4723',
            desired_capabilities={
            "platformName": "Widows",
            "deviceName": "WindowsPC",
            "app": self.app_path
            })

        self.driver.implicitly_wait(1)
        self.driver.set_page_load_timeout(50000)
        
        yield self.driver, self.file_test_path, self.app_path, self.file_test_dynmat, self.file_test_txt,\
            self.new_file, self.path_to_new_file, self.to_check_text_warning_window_chose_envelope
        
        self.driver.quit()
        
        if os.path.isfile(self.path_to_new_file) == True:
            os.remove(self.path_to_new_file)


class AppLocators:

    app_window = 'Envelope for QE PH calculations'
    
    exit_button = '//Window[@Name="Envelope for QE PH calculations"]/TitleBar/Button[@Name="Zamknij"]'
    
    
    button_chose_input_file = '//Window[@Name="Envelope for QE PH calculations"]/'\
                              'Pane[@ClassName="TkChild"]/Pane[@ClassName="TkChild"]/'\
                              'Pane[@ClassName="TkChild"]/Pane[@ClassName="TkChild"]'\
                              '/Pane[@ClassName="TkChild"]/Pane[4]/Button[@ClassName="Button"]'
                            
    input_file_name = '//Window[@Name="Otwieranie"]/ComboBox[@Name="Nazwa pliku:"]/Edit[@Name="Nazwa pliku:"]'
    
    input_path_button = '//Window[@Name="Otwieranie"]/Pane[@ClassName="ReBarWindow32"]/'\
                        'Pane[@ClassName="Address Band Root"]/'\
                        'ProgressBar[@ClassName="msctls_progress32"]/Pane[@ClassName="Breadcrumb Parent"]/'\
                        'ToolBar[@ClassName="ToolbarWindow32"]/Button[@Name="Wszystkie lokalizacje"]'
                
    input_path_input = '//Window[@Name="Otwieranie"]/Pane[@ClassName="ReBarWindow32"]/'\
                       'Pane[@ClassName="Address Band Root"]/ProgressBar[@ClassName="msctls_progress32"]/'\
                       'ComboBox[@Name="Adres"]/Edit[@Name="Adres"]'
    
    input_path_button = '//Window[@Name="Otwieranie"]/Pane[@ClassName="ReBarWindow32"]/'\
                        'Pane[@ClassName="Address Band Root"]/ProgressBar[@ClassName="msctls_progress32"]/'\
                        'ToolBar[@ClassName="ToolbarWindow32"]/Button[1]'
    
    button_sent_input_file = '//Window[@Name="Otwieranie"]/Button[@Name="Otwórz"]'
    
    check_button_IR = '//Window[@Name="Envelope for QE PH calculations"]/'\
                      'Pane[@ClassName="TkChild"]/Pane[@ClassName="TkChild"]/'\
                      'Pane[@ClassName="TkChild"]/Pane[@ClassName="TkChild"]'\
                      '/Pane[@ClassName="TkChild"]/Pane[3]/Pane[3]/Button[2]'
                            
    check_button_Raman = '//Window[@Name="Envelope for QE PH calculations"]/'\
                         'Pane[@ClassName="TkChild"]/Pane[@ClassName="TkChild"]/'\
                         'Pane[@ClassName="TkChild"]/Pane[@ClassName="TkChild"]'\
                         '/Pane[@ClassName="TkChild"]/Pane[3]/Pane[3]/Button[1]'
                            
    radio_button_Voigt = '//Window[@Name="Envelope for QE PH calculations"]/'\
                         'Pane[@ClassName="TkChild"]/Pane[@ClassName="TkChild"]/'\
                         'Pane[@ClassName="TkChild"]/Pane[@ClassName="TkChild"]'\
                         '/Pane[@ClassName="TkChild"]/Pane[3]/Pane[2]/Pane[1]/Button[1]'
    
    check_button_PTI = '//Window[@Name="Envelope for QE PH calculations"]/'\
                       'Pane[@ClassName="TkChild"]/Pane[@ClassName="TkChild"]/'\
                       'Pane[@ClassName="TkChild"]/Pane[@ClassName="TkChild"]'\
                       '/Pane[@ClassName="TkChild"]/Pane[3]/Pane[1]/Button[1]'
    
    entry_standard_deviation = '//Window[@Name="Envelope for QE PH calculations"]/'\
                               'Pane[@ClassName="TkChild"]/Pane[@ClassName="TkChild"]'\
                               '/Pane[@ClassName="TkChild"]/Pane[@ClassName="TkChild"]'\
                               '/Pane[@ClassName="TkChild"]/Pane[2]/Pane[3]/Pane[3]'
    
    entry_scale_param = '//Window[@Name="Envelope for QE PH calculations"]/'\
                        'Pane[@ClassName="TkChild"]/Pane[@ClassName="TkChild"]/Pane[@ClassName="TkChild"]/'\
                        'Pane[@ClassName="TkChild"]/Pane[@ClassName="TkChild"]/Pane[2]/Pane[3]/Pane[2]'
    
    entry_number_of_pints_in_envelope = '//Window[@Name="Envelope for QE PH calculations"]/'\
                                        'Pane[@ClassName="TkChild"]/Pane[@ClassName="TkChild"]/'\
                                        'Pane[@ClassName="TkChild"]/Pane[@ClassName="TkChild"]'\
                                        '/Pane[@ClassName="TkChild"]/Pane[2]/Pane[3]/Pane[1]'
    
    button_calculate_envelope = '//Window[@Name="Envelope for QE PH calculations"]/'\
                                'Pane[@ClassName="TkChild"]/Pane[@ClassName="TkChild"]/'\
                                'Pane[@ClassName="TkChild"]/Pane[@ClassName="TkChild"]'\
                                '/Pane[@ClassName="TkChild"]/Pane[2]/Pane[2]/Button[2]'
    
    button_export_data = '//Window[@Name="Envelope for QE PH calculations"]/'\
                         'Pane[@ClassName="TkChild"]/Pane[@ClassName="TkChild"]/Pane[@ClassName="TkChild"]/'\
                         'Pane[@ClassName="TkChild"]/Pane[@ClassName="TkChild"]/Pane[2]/Pane[2]/Button[1]'
    
    label_with_info = '//Window[@Name="Envelope for QE PH calculations"]/'\
                      'Pane[@ClassName="TkChild"]/Pane[@ClassName="TkChild"]/Pane[@ClassName="TkChild"]/'\
                      'Pane[@ClassName="TkChild"]/Pane[@ClassName="TkChild"]/Pane[2]/Pane[1]/'\
                      'Image[@ClassName="Static"]'
                            
    fig_with_Raman = '//Window[@Name="Envelope for QE PH calculations"]/'\
                     'Pane[@ClassName="TkChild"]/Pane[@ClassName="TkChild"]/Pane[@ClassName="TkChild"]/'\
                     'Pane[@ClassName="TkChild"]/Pane[@ClassName="TkChild"]/Pane[1]/Pane[2]/Pane[2]'
                            
    window_save_file = '//Window[@Name="Envelope for QE PH calculations"]/'\
                        'Window[@ClassName="#32770"]/Pane[@ClassName="DUIViewWndClassName"]/'\
                        'ComboBox[@ClassName="AppControlHost"]/Edit[@Name="Nazwa pliku:"]'


    button_save_file = '//Window[@Name="Envelope for QE PH calculations"]/'\
                       'Window[@ClassName="#32770"]/Button[@Name="Zapisz"]'
                       
    text_in_warning_window_chose_envelope= 'Chose envelope for IR or/and Raman?'
    
    button_ok_warning_window_chose_envelope = '//Window[@Name="Warning!"]/Button[@Name="OK"]'


@pytest.mark.usefixtures("setup")
class TestsGUI(PreconditionsGui):

    @allure.title("User enter correct data into the form")
    @allure.description_html("""
    <p>User enter correct data into the form. Positive test case.</p>
    <p>Environment: Windows 10 Home 20H2</p>
    """)
    @allure.severity(allure.severity_level.NORMAL)
    #@pytest.mark.skip
    @pytest.mark.parametrize(
        'standard_deviation,scale_param,number_of_points_in_envelope',
        [('5.5', '5.5', '500')]
    )
    def test_user_gui_positive_test_case(self, standard_deviation, scale_param, number_of_points_in_envelope):

        #When
        button_chose_input_file = self.driver.find_element_by_xpath(AppLocators.button_chose_input_file)
        button_chose_input_file.click()
    
        input_directory_button = self.driver.find_element_by_xpath(AppLocators.input_path_button)
        input_directory_button.click()
        
        input_directory_input = self.driver.find_element_by_xpath(AppLocators.input_path_input)
        input_directory_input.click()

        #press keys in the same time
        input_directory_input.send_keys(Keys.CONTROL, 'a')
        
        input_directory_input.send_keys(Keys.BACKSPACE + self.file_test_path)
        
        button_input_directory = self.driver.find_element_by_xpath(AppLocators.input_path_button)
        button_input_directory.click()
        
        input_file = self.driver.find_element_by_xpath(AppLocators.input_file_name)
        input_file.click()
        input_file.send_keys(self.file_test_dynmat)
        
        button_sent_input_file = self.driver.find_element_by_xpath(AppLocators.button_sent_input_file)
        button_sent_input_file.click() 
        
        button_sent_input_ir = self.driver.find_element_by_xpath(AppLocators.check_button_IR)
        button_sent_input_ir.click()
        
        button_sent_input_raman = self.driver.find_element_by_xpath(AppLocators.check_button_Raman)
        button_sent_input_raman.click() 
        
        radio_button_Voigt = self.driver.find_element_by_xpath(AppLocators.radio_button_Voigt)
        radio_button_Voigt.click()
        
        check_button_PTI = self.driver.find_element_by_xpath(AppLocators.check_button_PTI)
        check_button_PTI.click()
        
        
        entry_standard_deviation = self.driver.find_element_by_xpath(AppLocators.entry_standard_deviation)
        entry_standard_deviation.click()
        entry_standard_deviation.send_keys(standard_deviation)
        
        entry_scale_param =self.driver.find_element_by_xpath(AppLocators.entry_scale_param)
        entry_scale_param.click()
        entry_scale_param.send_keys(scale_param)
        
        entry_number_of_points = self.driver.find_element_by_xpath(AppLocators.entry_number_of_pints_in_envelope)
        entry_number_of_points.click()
        entry_number_of_points.send_keys(number_of_points_in_envelope)
        
        button_calculate_envelope = self.driver.find_element_by_xpath(AppLocators.button_calculate_envelope)
        button_calculate_envelope.click()
        
        
        fig_with_Raman = self.driver.find_element_by_xpath(AppLocators.fig_with_Raman)
        
        #Slicing of figure
        location_Raman = fig_with_Raman.location
        size = fig_with_Raman.size
    
        image1 = base64.decodebytes(bytes(self.driver.get_screenshot_as_base64(), "utf-8"))
        image1 = Image.open(BytesIO(image1))
        image2 = Image.open('D:/Praca/Symulacje/Narzedzia/Moje/Envelope_for_QE/Envelope-for-dynmat-quantum-esspreso/Test_data/Envelope_for_QE_PH_calculations.png')
        
        left = location_Raman['x']
        top = location_Raman['y']
        right = location_Raman['x'] + size['width']
        bottom = location_Raman['y'] + size['height']
        
        image1 = image1.crop((left, top, right, bottom))

        #Compare images by image hashing
        hash0 = imagehash.average_hash(image1)
        hash1 = imagehash.average_hash(image2)
        
        print('Delta_hash: ', hash0 - hash1)
        
        if hash0 - hash1 < 0.5:
            assert_val = True
        else:
            assert_val = False
            
        #Then 
        assert assert_val
        
        #When 
        #convert PIL image to bytes 
        buffered = BytesIO()
        image1.save(buffered, format="PNG")
        buffered = buffered.getvalue()
        
        allure.attach(buffered, name="App_Window.png", attachment_type=AttachmentType.PNG)
        
        button_export_data = self.driver.find_element_by_xpath(AppLocators.button_export_data)
        button_export_data.click()
        
        window_save_file = self.driver.find_element_by_xpath(AppLocators.window_save_file)
        window_save_file.click()
        window_save_file.send_keys(self.new_file)
        
        button_save_file = self.driver.find_element_by_xpath(AppLocators.button_save_file)
        button_save_file.click()
        #Then 
        time.sleep(2)
        assert os.path.isfile(self.path_to_new_file)
        
    @allure.title("User enter incorrect data into the form")
    @allure.severity(allure.severity_level.NORMAL)        
    def test_user_no_insert_data_to_form(self):
        #When
        button_calculate_envelope = self.driver.find_element_by_xpath(AppLocators.button_calculate_envelope)
        print(button_calculate_envelope)
        button_calculate_envelope.click()
        
        text_in_warning_window_chose_envelope = self.driver.find_element_by_name(AppLocators.text_in_warning_window_chose_envelope)
        string = text_in_warning_window_chose_envelope.text
        print('Text in warning: ', string)
        #Then
        assert string == self.to_check_text_warning_window_chose_envelope
        
        button_ok_warning_window_chose_envelope = self.driver.find_element_by_xpath(AppLocators.button_ok_warning_window_chose_envelope)
        button_ok_warning_window_chose_envelope.click()
        time.sleep(2)
        
        val_expect = False
        
        try: 
            button_ok_warning_window_chose_envelope = self.driver.find_element_by_xpath(AppLocators.button_ok_warning_window_chose_envelope)
            val_expect = False
            
        except:
            val_expect = True
            
        assert val_expect
        
    @allure.title("User exit app")
    @allure.severity(allure.severity_level.NORMAL)        
    def test_user_exit_app(self):
        
        #Then
        exit_button = self.driver.find_element_by_xpath(AppLocators.exit_button)
        exit_button.click()
        
        time.sleep(2)
        assert_val = False
        
        try:
            app_window = self.driver.find_element_by_name(AppLocators.exit_button)
            assert_val = False
        except:
            assert_val = True
        
        assert assert_val