================
FOLDER STRUCTURE
================

.ipynb_checkpoints - contains all files neccessary for Jupyter Notebook to work || DO NOT ALTER.

model_training - .ipynb files are source code files that are opened in Jupyter Notebook.

	-> .ipynb_checkpoints - contains all files neccessary for Jupyter Notebook to work || DO NOT ALTER.
	-> data - contains hand tracking data used when developing the models
	-> model_testing - all the ouput files of my model testing script
	-> saved_models - all the different models that I have developed and saved for later use

scripts - where the main application scripts reside, DataExtractor.py is the driver module.

tests - some screenshots of graphs and confusion matrices of different models


=============
PREREQUISITES
=============

- Leap Motion Controller is connected to computer via USB, and drivers have been installed.
- Python 2.7 installed, take note of directory location.
- Rename the python.exe file in your Python 2.7 folder to python27.exe, if not already done.
- Python 3.9 installed.
- All python dependencies and packages installed.


==========
HOW TO RUN
==========

1. Make sure all the prerequisites are met.
2. Run the command prompt (run as administrator if you encouter any problems)
3. Navigate to the project's "scripts" folder using the 'cd' command. Example: cd C:\Users\winba\Desktop\TYP_SUPPLEMENTARY\scripts
4. Run the DataExtractor script using python27. Example: python27 DataExtractor.py
5. Follow on-screen instructions.

