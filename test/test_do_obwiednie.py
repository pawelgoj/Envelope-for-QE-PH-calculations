#import allure
import pytest
import shutil
import os


class Preconditions:
    
    @pytest.fixture()
    def setup(self):
        self.file_name = "D:/Praca/Symulacje/Narzędzia/Moje/Envelope_for_QE/Envelope-for-dynmat-quantum-esspreso/AlPO4"
        
        yield self.file_name
        
        try:
            file_1 = self.file_name + '_IR.png'
            file_2 = self.file_name + '_Raman.png'
            file_3 = self.file_name + '_Raman.txt'
            file_4 = self.file_name + '_Raman.txt'
            os.remove(file_1)
            os.remove(file_2)
            os.remove(file_3)
            os.remove(file_4)
            
        except:
            pass
        
class TestDoEnvelopwe:
    def test_input(self, script_runner, mocker):
        mocker.patch('builtins.input', side_effect= ['dynmat', 'Voigt', '5 1', '500', 'dynmatAlPO3_3.out', 'AlPO4', 'Both'])
        ret = script_runner.run('do_envelope.py')
        assert ret.success
        assert ret.stdout == "Insert the: dynmat/txt, type of band curve, width of the curves, "\
            "number of pints, file name, label name and Raman/IR/Both\nData loaded\nraman "\
            "envelope done\nIR envelope done\nresult saved\n"