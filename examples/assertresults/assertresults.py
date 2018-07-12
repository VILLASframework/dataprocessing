import re
import os
import sys

sys.path.append(r"D:\HIWI\Git\data-processing\dataprocessing")
from validationtools import *
from readtools import *
os.chdir(r"D:\HIWI\Git")

print("Test Start")
# We need to extract all the result files from git now

for files in os.listdir(
        os.path.abspath("reference-results/Neplan/BasicGrids")):
        #  Assert the result, model result path read from cmd line
        validate_modelica_res(os.path.splitext(files)[0],
                                      os.path.abspath("reference-results/Modelica/BasicGrids/" +
                                                      os.path.splitext(files)[0] + ".mat"),
                                      os.path.abspath("reference-results/Neplan/BasicGrids/" +
                                                      os.path.splitext(files)[0] + ".rlf"))

print("Test End")
