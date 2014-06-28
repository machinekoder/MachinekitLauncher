#!/usr/bin/python

import sys
import os
import subprocess
from time import *
import MachinekitLauncher as launcher

launcher.registerExitHandler()

launcher.setDebugLevel(5)
launcher.setMachinekitIni('machinekit.ini')

os.chdir(os.path.dirname(os.path.realpath(__file__)))

try:
    launcher.ripEnvironment()
    launcher.checkInstallation()
    launcher.clearSession()
    launcher.startProcess("configserver 'uis/HalanduinoDemo.Control'")
    launcher.startRealtime()
    launcher.loadHalFile("Halanduino.hal")
except subprocess.CalledProcessError:
    sys.exit(1)

while True:
    sleep(1)
    launcher.checkProcesses()
