#import allure
import pytest
import os
import pandas as pd
import numpy as np
import factory
from pytest_factoryboy import register
from classes import Results
from do_envelope import DuEnvelope 


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
    
    def test_save_envelopes(self):
        
        raman_envelpe = np.array([[1,2],
                                [1,2]])
        ir_envelpe = np.array([[1,2],
                                [1,2]])
        du_envelope = DuEnvelope(None, None, None, None, None, None, None,None, 
                                 raman_envelpe = raman_envelpe, ir_envelpe = ir_envelpe)
        du_envelope.save_envelopes(self.path_results)
        assert os.path.isfile(self.path_results)

    def test_do_envelopes(self):
        
        du_envelope = DuEnvelope('dynmat', 'Voigt', 3, 2, False, 500, self.file_with_data,'Both')
        du_envelope.make_envelopes()
        du_envelope.save_envelopes(self.path_results)
        
        assert os.path.isfile(self.path_results)

    @pytest.mark.skip
    def test_input(self, script_runner, mocker):
        
        # the script_runner and mocker patch make ability to test console behave of user. 
        
        mocker.patch('builtins.input', side_effect= ['dynmat', 'Voigt', '5 1', 'proportional', '500', 'dynmatAlPO3_3.out', 'AlPO4', 'Both'])
        ret = script_runner.run('do_envelope.py')
        assert ret.success
        assert ret.stdout == "Insert the: dynmat/txt, type of band curve, width of the curves, "\
            "number of pints, file name, label name and Raman/IR/Both\nData loaded\nraman "\
            "envelope done\nIR envelope done\nresult saved\n"
            

            
            
@pytest.mark.classes_test
@pytest.mark.usefixtures("setup")
class TestResults(Preconditions):
    def test_save_data(self):
        d = {'cm-1': [1, 2, 3], 'IR': [0,2,4], '2cm-1': [4,5,6], 'Raman': [1,2,3]}
        df = pd.DataFrame(data=d)
        results = Results(df, self.path_results)
        results.save_data()
        assert os.path.isfile(self.path_results)
       
        

        