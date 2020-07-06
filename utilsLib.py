## author: Mathieu Renzo

## Author: Mathieu Renzo <mathren90@gmail.com>
## Keywords: files

## Copyright (C) 2019-2020 Mathieu Renzo

## This program is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or (at
## your option) any later version.
##
## This program is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
## General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program.  If not, see http://www.gnu.org/licenses/.


import glob
import sys
import os
import re  # for getM
import subprocess  # for tail


def gitPush(description=""):
    push = input("should we push to the git repo first? [Y/n]")
    if (push == "Y") or (push == "y"):
        pwd = os.getcwd()  # where am I?
        os.chdir("/mnt/home/mrenzo/Templates/ppisn/")
        os.system(
            "git add . && git commit -am 'about to start a run:" + description + "' && git push"
        )
        os.chdir(pwd)  # go back to previous folder


def checkFolder(folder):
    # checks if folder exists, if not, it creates it, and returns its content
    found = glob.glob(folder)
    if found:
        print("Found folder:", folder)
        content = glob.glob(folder + "/*")
        return content
    if not found:
        os.system("mkdir -p " + str(folder))
        return glob.glob(folder + "/*")  ## will be empty


def MoveIntoFolder(folder, description=""):
    content = checkFolder(folder)
    if content:
        os.chdir(folder)
        os.system("pwd")
        return 0
    else:
        print("content:", content)
        mkfolder = input(str(folder) + " is not empty. Proceed? [Y/n]")
        if (mkfolder == "Y") or (mkfolder == "y"):
            os.chdir(folder)
            os.system("echo " + description + " > run_description.txt")
            print("******************")
            print(description)
            print("******************")
            return 0
        else:
            print("Ok, fix it yourself!Bye!")
            return 1


def getM(f):
    # use regexp to find mass, will only work if mass is the first number in the path
    m = re.findall("[+-]?\d+\.\d+", f)
    # print(m)
    return float(m[0])


def tail(f, n=1):
    # read the last n lines of f (modified from somewhere on the internet)
    n = str(n)
    p = subprocess.Popen(["tail", "-n", n, f], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    # print stdout
    lines = stdout.splitlines()
    return lines


def getTerminationCodeFromOutput(f):
    """
    Assuming you run MESA piping the output to a file called output
    or out (possibly using tee as in ./rn | tee output), this will scan
    this file for the termination code string and return it. It looks for 
    the file in your run folder
    """
    if os.path.isfile(f + "/output"):
        outputfile = f + "/output"
    elif os.path.isfile(f + "/out"):
        outputfile = f + "/out"
    else:
        print("can't find output file")
        print("did you forget to pipe ./rn or ./re to a file?")
        return ""
    end_out = tail(outputfile, 50)
    termination_code = "Couldn't find termination code"
    # print end_out
    for i in range(len(end_out) - 1, 0, -1):
        line = str(end_out[i].decode("utf-8"))
        # print(line)
        if "termination code:" in line:
            termination_code = line.split(":")[-1].strip()
            break
        elif ("star is going PISN!" in line) or ("above the escape velocity, PISN!" in line):
            termination_code = "PISN"
            break
    return termination_code



def mvFolder(runFolder, targetFolder, targetTerminationCode="max_model_number"):
    """ 
    checks a MESA work directory and if the termination code is what is wanted
    moves the relevant content to a target folder
    """
    terminationCode = getTerminationCodeFromOutput(runFolder)
    if terminationCode == targetTerminationCode:
        if not os.path.isdir(targetFolder):
            os.system('mkdir -p '+targetFolder)
        # # copy output
        os.system("cp -r "+runFolder+"/LOGS "+" "+targetFolder)
        # copy input
        os.system("cp -r "+runFolder+"/inlist* "+targetFolder)
        os.system("cp -r "+runFolder+"/src/run_*_extras* "+targetFolder)
        # copy models
        os.system("cp -r "+runFolder+"/*.mod "+targetFolder)
        print(runFolder, "copied to", targetFolder)
        # now clean backup files and stuff
        os.system("rm -rf "+targetFolder+"/*~")
        os.system("rm -rf "+targetFolder+"/*.back")
    else:
        print(runFolder, terminationCode, "not copied")
