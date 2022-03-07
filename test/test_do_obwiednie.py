#import allure
import pytest
import os
import pandas as pd
import numpy as np
from pytest_factoryboy import register
from classes import Results
from do_envelope import DoEnvelope 
import matplotlib.pyplot as plt


class Preconditions:
    @pytest.fixture()
    def setup(self):
        self.file_name = "D:/Praca/Symulacje/Narzedzia/Moje/Envelope_for_QE/"\
            "Envelope-for-dynmat-quantum-esspreso"
        self.path_results = "D:/Praca/Symulacje/Narzedzia/Moje/Envelope_for_QE/"\
            "Envelope-for-dynmat-quantum-esspreso/file.csv"
        self.file_with_data = "D:/Praca/Symulacje/Narzedzia/Moje/Envelope_for_QE/"\
            "Envelope-for-dynmat-quantum-esspreso/dynmatAlPO3_3.out" 
        
        yield self.file_name, self.path_results, self.file_with_data
        
        try:
            file_1 = os.path.join(self.file_name, 'AlPO4_IR.png')
            file_2 = os.path.join(self.file_name, 'AlPO4_Raman.png')
            file_3 = os.path.join(self.file_name, 'AlPO4_Raman.txt')
            file_4 = os.path.join(self.file_name, 'AlPO4_IR.txt')


            os.remove(file_1)
            os.remove(file_2)
            os.remove(file_3)
            os.remove(file_4)
            
        except:
            pass



@pytest.mark.usefixtures("setup")
class TestDoEnvelope(Preconditions):

    def test_do_envelopes(self):
        do_envelope = DoEnvelope()
        do_envelope.set_param('dynmat', 'Voigt', 3, 2, False, 500, self.file_with_data,'Both')
        do_envelope.make_envelopes()
        do_envelope.save_envelopes(self.path_results)
        
        assert os.path.isfile(self.path_results)

    #The app no longer has console interaction
    @pytest.mark.skip
    def test_input(self, script_runner, mocker):
        
        # the script_runner and mocker patch make ability to test console behave of user. 
        
        mocker.patch('builtins.input', side_effect= ['dynmat', 'Voigt', '5 1', 'proportional', '500', 'dynmatAlPO3_3.out', 'AlPO4', 'Both'])
        ret = script_runner.run('do_envelope.py')
        assert ret.success
        assert ret.stdout == "Insert the: dynmat/txt, type of band curve, width of the curves, "\
            "number of pints, file name, label name and Raman/IR/Both\nData loaded\nraman "\
            "envelope done\nIR envelope done\nresult saved\n"
            
    def test_return_figs(self):
        #Given 
        do_envelope = DoEnvelope()
        
        #When
        do_envelope.set_param('dynmat', 'Voigt', 3, 2, False, 500, self.file_with_data,'Both')
        do_envelope.make_envelopes()
        ir_fig, raman_fig = do_envelope.return_figs()
        
        #Then
        ir_fig.savefig("output1", dpi=100)
        raman_fig.savefig("output2", dpi=100)
        plt.close()
        
                  
@pytest.mark.classes_test
@pytest.mark.usefixtures("setup")
class TestResults(Preconditions):
    def test_save_data(self):
        
        #Given 
        array1 = np.array([[0,1,2],[0,1,2]])
        array2 = np.array([[0,1,2],[0,1,2]])
        d = {'cm-1': [1, 2, 3], 'IR': [0,2,4], '2cm-1': [4,5,6], 'Raman': [1,2,3]}
        df = pd.DataFrame(data=d)
        results = Results(df,array1,array2)
        
        #When
        results.save_data(self.path_results)
        
        #Then
        assert os.path.isfile(self.path_results)
       
        

        