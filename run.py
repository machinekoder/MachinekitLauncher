#!/usr/bin/python

import sys
from time import *
import MachinekitLauncher as launcher

launcher.registerExitHandler()

launcher.setDebugLevel(5)
launcher.setMachinekitIni('machinekit.ini')

try:
    launcher.ripEnvironment('/home/machinekit/machinekit/')
    launcher.checkInstallation()
    launcher.clearSession()
    launcher.startProcess("configserver 'uis/HalanduinoDemo.Control'")
    launcher.startRealtime()
    launcher.loadHalfile("Halanduino.hal")
except subprocess.CalledProcessError:
    sys.exit(1)

while True:
    sleep(1)
    launcher.checkProcesses()
