# Introduction:
Based on the paper **pyTDGL: Time-dependent Ginzburg-Landau in Python, Computer Physics Communications 291, 108799 (2023)** and the corresponding code at https://github.com/loganbvh/py-tdgl, I wrote a quick-tdgl py file for easy simualtions and records.

# Install ``pyTDGL``:
Refer to the guide in https://github.com/loganbvh/py-tdgl.

# Try ``pyTDGL``:
Run jupyter notebook ``example.ipynb`` to simulate the gradual emergence of vortex in the rising external field.

![](output.png 'vortices')

Or run ``I-B.ipynb`` to draw a curve of boundary current versus magnetic field and observe the hysteresis phenomenon.

![](I-B.png 'hysteresis')

# How to use ``quick-tdgl.py``:
View the program parameters:  
``python quick-tdgl.py -h``

Input parameters:  
``python quick-tdgl.py --length_units 'um' ...``

Or manually assign values ​​to parameters in ``parser.py`` by modifying the default value.  
``parser.add_argument('--length_units', type=str, default='um')``  
``...``

Run the code:  
``python quick-tdgl.py``




