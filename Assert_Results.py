import re
import os
import sys

from dataprocessing.Validationtools import *
from dataprocessing.readtools import *
print("Test Start")
# We need to extract all the result files from git now

assert_modelia_neplan_results("Slack_ZLoad") #  Assert the result, model result path read from cmd line
print("Test End")
