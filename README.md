# Envelope for QE PH calculations

## Description

The application generates envelopes for intensities of the calculated theoretical spectra of IR and Raman. You can generate an envelope for a output from dynmat.x ( [Quantum espresso](https://www.quantum-espresso.org/)) or appropriate '.txt' file.

![Window of app Envelope for QE PH calculations](Window.png "Window of app Envelope for QE PH calculations")


## Usage

If you want to use exe file for windows download "Envelope for QE PH calculations.zip" (find it in Releases) and unpack it. Run program "Envelope for QE PH calculations.exe" in unpacked folder. Complete the form and press `<Calculate envelope>` button to calculate envelope.

### Input files

You can use dynamt.x output or '.txt'. If you want use dynamt.x output don't add '.txt' extension. If file have '.txt' extension its format should be as shown in the picture. The file should contain 'Raman', 'cm-1' and 'IR' column labels.

![example1](example_txt.png "example1")

If only one spectra is used two columns are needed 'cm-1' and 'IR' or 'Raman'.

### Types of bands 

- Gauss - Gaussian curve of single band
- Lorentz - Cauchy curve (Lorentz) of single band
- Voigt - Voigt curve of single band

Proportional to intensity option causes standard deviation and scale param are proportional to intensity. Only the greatest intensity has the entered values of standard deviation and scale param. These values decrease with intensity.

To obtain accurate envelopes number of points in envelope must be greater than 500.

### Export data

Calculated envelopes can be exported to '.csv' file.

## Technologies/Tools

1. Python 3.9
2. tkinter
3. Python Standard Library modules
4. Matplotlib
5. Numpy
6. SciPy
7. Pandas

## Tests

### Tools:

1. Appium-Python-Client 1.3 + WinAppDriver 1.2.1
2. pytest 
3. allure 
