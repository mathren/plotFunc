# author: Mathieu Renzo

# Author: Mathieu Renzo <mathren90@gmail.com>
# Keywords: files

# Copyright (C) 2019-2020 Mathieu Renzo

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see http://www.gnu.org/licenses/.


import glob
import sys
import os
import re  # for getM
import subprocess  # for tail
from MESAreader import getSrcCol

def gitPush(repo, description=""):
    push = input("should we push to the git repo first? [Y/n]")
    if (push == "Y") or (push == "y"):
        pwd = os.getcwd()  # where am I?
        os.chdir(repo)
        os.system(
            "git add . && git commit -am 'about to start a run:" + description + "' && git push"
        )
        os.chdir(pwd)  # go back to previous folder


def checkFolder(folder):
    """ checks if folder exists, if not, it creates it, and returns its content """
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
            print("Ok, fix it yourself!")
            return 1


def getM(f):
    """
    get the mass from the folder name
    assumes that the mass is the first number in the folder name
    and that it has a decimal point -- in the regexp
    """
    if f[-1] == "/":
        folder = f.split("/")[-2]
    elif f[-1] != "/":
        folder = f.split("/")[-1]
    # print(folder)
    m = re.findall("[+-]?\d+\.\d+", folder)
    # print(m)
    return float(m[0])


def getMasses(f):
    if f[-1] == "/":
        folder = f.split("/")[-2]
    elif f[-1] != "/":
        folder = f.split("/")[-1]
    # print(folder)
    m = re.findall("[+-]?\d+\.\d+", folder)
    m1 = m[0]
    m2 = m[1]
    # print(m)
    return float(m1), float(m2)


def tail(f, n=1):
    # read the last n lines of f (modified from somewhere on the internet)
    n = str(n)
    p = subprocess.Popen(["tail", "-n", n, f], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    # print stdout
    lines = stdout.splitlines()
    return lines


def getTerminationCode(f, terminal_output="out.txt"):
    """Assuming you run MESA piping the output to a file whose name is in
    terminal_output (possibly using tee as in ./rn | tee output), this
    will scan this file for the termination code string and return
    it. It looks for the file in your run folder f
    """
    if os.path.isfile(f + "/"+terminal_output):
        outputfile = f + "/"+terminal_output
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
        elif "post RLOF found" in str(line):
            termcode = "post_RLOF"
            break
    return termination_code


def getFinalProfileLOGS(LOGfolder):
    """
    returns the path to the last profile written in the folder, assumes it is a LOGS* folder
    from a MESA run
    """
    indexFile = LOGfolder + "/profiles.index"
    last_line = tail(indexFile, 1)[0]
    # print(last_line)
    last_line = last_line.decode("utf-8")
    # print(type(last_line))
    profNum = "%d" % int(last_line.split()[-1])
    profile = "profile" + str(profNum) + ".data"
    # print(profile)
    return profile


def mvFolder(runFolder, targetFolder, targetTerminationCode="max_model_number"):
    """
    checks a MESA work directory and if the termination code is what is wanted
    moves the relevant content to a target folder
    """
    from compare_all_work_dir_inlists import isFolderBinary

    terminationCode = getTerminationCode(runFolder)
    if terminationCode == targetTerminationCode:
        ## make the folder if needed
        if not os.path.isdir(targetFolder):
            os.system("mkdir -p " + targetFolder)
        if not os.path.isdir(targetFolder + "/LOGS/"):
            os.system("mkdir -p " + targetFolder + "/LOGS/")
        ## these below are not needed for single stars, but whatever
        if not os.path.isdir(targetFolder + "/LOGS1/"):
            os.system("mkdir -p " + targetFolder + "/LOGS1/")
        if not os.path.isdir(targetFolder + "/LOGS2/"):
            os.system("mkdir -p " + targetFolder + "/LOGS2/")
        ## copy history output
        os.system(
            "cp -r " + runFolder + "/LOGS/history.data " + " " + targetFolder + "/LOGS/history.data"
        )
        os.system(
            "cp -r "
            + runFolder
            + "/LOGS1/history.data "
            + " "
            + targetFolder
            + "/LOGS1/history.data"
        )
        os.system(
            "cp -r "
            + runFolder
            + "/LOGS2/history.data "
            + " "
            + targetFolder
            + "/LOGS2/history.data"
        )
        os.system("cp -r " + runFolder + "/binary_history.data " + targetFolder)
        ## copy last profile
        os.system(
            "cp -r "
            + runFolder
            + "/LOGS/"
            + getFinalProfileLOGS(runFolder + "/LOGS/")
            + " "
            + targetFolder
            + "LOGS/"
        )
        os.system(
            "cp -r "
            + runFolder
            + "/LOGS1/"
            + getFinalProfileLOGS(runFolder + "/LOGS1/")
            + " "
            + targetFolder
            + "/LOGS1/"
        )
        os.system(
            "cp -r "
            + runFolder
            + "/LOGS2/"
            + getFinalProfileLOGS(runFolder + "/LOGS2/")
            + " "
            + targetFolder
            + "/LOGS2/"
        )
        ## copy models
        os.system("cp -r " + runFolder + "/*.mod " + targetFolder)
        ## copy input
        os.system("cp -r " + runFolder + "/inlist* " + targetFolder)
        os.system("cp -r " + runFolder + "/src/run_*_extras* " + targetFolder)
        print(runFolder, "copied to", targetFolder)
        ## now clean backup files and stuff
        os.system("rm -rf " + targetFolder + "/*~")
        os.system("rm -rf " + targetFolder + "/*.back")
    else:
        print(runFolder, terminationCode, "not copied")


def check_and_convert(f, convert=True, terminal_output="out.txt"):
    """
    given a MESA workdir f, check if the run terminated and if so create history.npy
    Assumes the terminal output was logged in a file in folder/terminal_output
    """
    if not os.path.isfile(f+'/'+terminal_output):
        print("No output file found, you'll have to check manually, sorry!")
        return
    termination_code = getTerminationCode(f, terminal_output)
    if ((termination_code != "") and \
        (termination_code != "Couldn't find termination code")):
        print("this run finished!")
        if convert:
            src, col = getSrcCol(f+'/LOGS/history.data', convert, convert)
            print("done converting!")
