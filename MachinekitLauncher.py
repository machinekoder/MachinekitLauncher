import os
import sys
from time import *
import subprocess
import signal

_processes = []


def cleanup():
    stopProcesses()
    stopRealtime()


def checkInstallation():
    commands = ['realtime', 'configserver', 'halcmd', 'haltalk', 'webtalk']
    for command in commands:
        process = subprocess.Popen('which ' + command, stdout=subprocess.PIPE, shell=True)
        process.wait()
        if process.returncode != 0:
            print((command + ' not found, check Machinekit installation'))
            sys.exit(1)


def clearSession():
    pids = []
    commands = ['configserver', 'halcmd', 'haltalk', 'webtalk', 'rtapi']
    process = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
    out, err = process.communicate()
    for line in out.splitlines():
        for command in commands:
            if command in line:
                pid = int(line.split(None, 1)[0])
                pids.append(pid)

    if pids != []:
        print("cleaning up leftover session")
        subprocess.check_call('realtime stop', shell=True)
        for pid in pids:
            try:
                os.kill(pid, signal.SIGTERM)
            except OSError:
                pass


def startProcess(command):
    sys.stdout.write("starting " + command.split(None, 1)[0] + "... ")
    sys.stdout.flush()
    process = subprocess.Popen(command, shell=True)
    sleep(1)
    process.poll()
    if (process.returncode is not None):
        sys.exit(1)
    process.command = command
    _processes.append(process)
    sys.stdout.write('done\n')


def stopProcesses():
    for process in _processes:
        sys.stdout.write('stopping ' + process.command.split(None, 1)[0] + '... ')
        sys.stdout.flush()
        process.kill()
        process.wait()
        sys.stdout.write('done\n')


def loadHalfile(filename):
    sys.stdout.write("loading " + filename + '... ')
    sys.stdout.flush()
    subprocess.check_call('halcmd -f ' + filename, shell=True)
    sys.stdout.write('done\n')


def startRealtime():
    sys.stdout.write("starting realtime...")
    sys.stdout.flush()
    subprocess.check_call('realtime start', shell=True)
    sys.stdout.write('done\n')


def stopRealtime():
    sys.stdout.write("stopping realtime... ")
    sys.stdout.flush()
    subprocess.check_call('realtime stop', shell=True)
    sys.stdout.write('done\n')


def ripEnvironment(machinekit_path):
    subprocess.check_call('. ' + machinekit_path + 'scripts/rip-environment', shell=True)


def checkProcesses():
    for process in _processes:
        process.poll()
        if (process.returncode is not None):
            _processes.remove(process)
            cleanup()
            if (process.returncode != 0):
                sys.exit(1)
            else:
                sys.exit(0)


def registerExitHandler():
    signal.signal(signal.SIGINT, _exitHandler)
    signal.signal(signal.SIGTERM, _exitHandler)


def _exitHandler(signum, frame):
    cleanup()
    sys.exit(0)


def setDebugLevel(level):
    os.environ['DEBUG'] = str(level)


def setMachinekitIni(ini):
    os.environ['MACHINEKIT_INI'] = ini
