First Exercise
=======================


What Is This?
-------------

This code (first_exercise.py) were developed in python (version 3.7.3) to comply with the proposed challenge described at the first-exercise.txt. The code implements a function that authorizes a transaction for a specific account, following some predefined rules.


Requirements to run this code
-----------------------

1. This code were developed to be run directly through terminal: cmd (Windows) or bash (Linux). 

2. The input information is passed by a json extension file.

3. Install Python 3.7.3. You can download and install Python 3.7.3 by accessing https://www.python.org/downloads/

4. Extract the files of first-exercise.zip

5. You must have read/write privileges in the directory from you'll be executing the code.

6. You must have execute permissions to run first_exercise.py.

7. Keep your "input.json" files in the same directory of the first_exercise.py file.

8. Check how your environment variable to run python is configured. During installation you may be asked to configure the environment variable and this can vary, it may be "python", "python3", etc. To check, in your terminal type "python --version". This command will tell you which version of python you have installed. If the command is not recognized, check your installation.


Running the code
--------------------------

To run the code:

1. Open the terminal (cmd or bash).

2. Navigate to the directory where you saved the extracted files.

3. To run the code with the default test file (input.json), type the following command:
# python first_exercise.py input.json

4. Check the result of the transaction in the terminal.

5. The result is also saved in the "output.json" file. This file is generated in the same directory from you're running the code.


Test Examples
--------------------------

We are providing some test files that can be used to simulate the rules to approve (or not) a transaction. Below we have the commands that you should run to execute the example tests.

# python first_exercise.py input_amount_limit.json
# python first_exercise.py input_blacklist.json
# python first_exercise.py input_blocked.json
# python first_exercise.py input_same_merchant.json
# python first_exercise.py input_time_interval.json


