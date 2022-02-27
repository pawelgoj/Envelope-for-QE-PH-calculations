#import allure
import pytest
import os


class Preconditions:
    @pytest.fixture()
    def setup(self):
        self.file_name = "D:/Praca/Symulacje/Narzędzia/Moje/Envelope_for_QE/Envelope-for-dynmat-quantum-esspreso"
        
        yield self.file_name
        
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
class TestDoEnvelopwe(Preconditions):
    
    def test_input(self, script_runner, mocker):
        
        mocker.patch('builtins.input', side_effect= ['dynmat', 'Voigt', '5 1', 'proportional', '500', 'dynmatAlPO3_3.out', 'AlPO4', 'Both'])
        ret = script_runner.run('do_envelope.py')
        assert ret.success
        assert ret.stdout == "Insert the: dynmat/txt, type of band curve, width of the curves, "\
            "number of pints, file name, label name and Raman/IR/Both\nData loaded\nraman "\
            "envelope done\nIR envelope done\nresult saved\n"