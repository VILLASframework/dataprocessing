import re
import os
import sys

sys.path.append(r"D:\HIWI\Git\data-processing\dataprocessing")
sys.path.append(r"D:\HIWI\Git\python-for-modelica-dev_interface\Py4Mod\py4mod")

from ModelicaModel import ModelicaModel
from validationtools import *
from readtools import *
os.chdir(r"D:\HIWI\Git")


def simulate_modelica(model_name, model_path):
    interface = ModelicaModel(model_name, model_path)

    # Initialization
    interface.createInterface("OPENMODELICA")
    interface.loadFile(model_path + '\ModPowerSystems\package.mo')

    # Redirection
    cwd = os.getcwd()
    wd = os.path.join(cwd, 'test')
    if not os.path.exists(wd):
        os.makedirs(wd)
    interface.changeWorkingDirectory(wd.replace("\\", "/"))

    # Build & Run
    interface.buildModel()
    interface.simulate()


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
