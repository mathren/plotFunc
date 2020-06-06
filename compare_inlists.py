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


## This has been tested with MESA version 12778

import os
import sys

## pip install termcolor
from termcolor import colored

# ----- some auxiliary functions ----------------------------------
def getNameVal(line):
    optionName = line.split("=")[0].rstrip().lstrip()
    optionName = optionName.lower()  ## convert everything to lowercase
    value = line.split("=")[-1].split("!")[0].rstrip().lstrip()
    return optionName, value


def convertBool(val):
    # fix occasional typo in the docs
    if (val == ".true.") or (val == ".true"):
        return ".true."
    elif (val == ".false.") or (val == ".false"):
        return ".false."
    else:
        return val


def convertFloat(val):
    try:
        tmp = val.replace("d", "e")
        new_val = float(tmp)
        return new_val
    except:
        return val


def cleanVal(val):
    val = convertFloat(val)
    val = convertBool(val)
    return val

def getMESA_DIR():
    # read the MESA_DIR from bashrc if not provided
    try:
        MESA_DIR = os.environ["MESA_DIR"]
        return MESA_DIR
    except KeyError:
        print(colored("Maybe $MESA_DIR environment variabile is not set?","yellow"))
        print(colored("I don't know what to do, bye!","yellow"))
        sys.exit()

# ----------------------- read the defaults ----------------------------------
def getDefaults(namelist, MESA_DIR=""):
    defaults = {}
    if MESA_DIR == "":
        MESA_DIR = getMESA_DIR()
    if namelist.lower() == "star_job":
        defaultFname = MESA_DIR + "/star/defaults/star_job.defaults"
    elif namelist.lower() == "binary_job":
        defaultFname = MESA_DIR + "/binary/defaults/binary_job.defaults"
    elif namelist.lower() == "controls":
        defaultFname = MESA_DIR + "/star/defaults/controls.defaults"
    elif namelist.lower() == "binary_controls":
        defaultFname = MESA_DIR + "/binary/defaults/binary_controls.defaults"
    elif namelist.lower() == "pgstar":
        defaultFname = MESA_DIR + "/star/defaults/pgstar.defaults"
    else:
        print("Namelist: " + namelist + " not recognized, don't know what to do!", red)
        return defaults
    # now if we did not exit already, load a dict
    # print(defaultFname)
    with open(defaultFname, "r") as f:
        for i, line in enumerate(f):
            l = line.strip("\n\r").rstrip().lstrip()  # remove \n and white spaces
            if (l == "") or (l[0] == "!"):
                # empty line or comment, move on
                continue
            else:
                optionName, value = getNameVal(l)
                value = cleanVal(value)
                # # fix arrays
                # if "(" in optionName:
                #     optionName = optionName.split("(", 1)[0]
                defaults[optionName] = value
    # Note, the longest key is ~45 characters in length, hence the 45 further down in the string formatting
    return defaults


# --------------------- read namelist of the inlists -------------------------

def getJobNamelist(inlist):
    """ 
    returns a dictionary of the star_job or binary_job namelist entries and values
    and a flag for binaries
    """
    job = {}
    isBinary = False
    with open(inlist, "r") as i1:
        inJobNamelist = False
        for i, line in enumerate(i1):
            # print(line.strip('\n\r'))
            l = line.strip("\n\r").rstrip().lstrip()  # remove \n and white spaces
            if "&star_job" == l.lower():
                inJobNamelist = True
                isBinary = False
                continue  # to avoid adding the first line
            elif "&binary_job" == l.lower():
                inJobNamelist = True
                isBinary = True
                continue  # to avoid adding the first line
            if inJobNamelist:
                if (l == "") or (l[0] == "!"):
                    # skip empty lines
                    pass
                else:
                    if l[0] == "/":  # exit
                        inJobNamelist = False
                        break
                    else:
                        optionName, value = getNameVal(l)
                        value = cleanVal(value)
                        job[optionName] = value
    return job, isBinary


def getControlsNamelist(inlist):
    """ 
    returns a dictionary of the controls or binary_controls namelist entries and values 
    and a flag for binaries
    """
    controls = {}
    isBinary = False
    with open(inlist, "r") as i1:
        inControlsNamelist = False
        for i, line in enumerate(i1):
            # print(line.strip('\n\r'))
            l = line.strip("\n\r").rstrip().lstrip()  # remove \n and white spaces
            if "&controls" == l.lower():
                inControlsNamelist = True
                isBinary = False
                continue  # to avoid adding the first line
            elif "&binary_controls" == l.lower():
                inControlsNamelist = True
                isBinary = True
                continue  # to avoid adding the first line
            if inControlsNamelist:
                if (l == "") or (l[0] == "!"):
                    # skip empty lines
                    pass
                else:
                    if l[0] == "/":  # exit
                        inControlsNamelist = False
                        break
                    else:
                        optionName, value = getNameVal(l)
                        value = cleanVal(value)
                        controls[optionName] = value
    return controls, isBinary

def getPgstarNamelist(inlist):
    """ 
    returns a dictionary of the pgstar namelist entries and values 
    """
    pgstar = {}
    with open(inlist, "r") as i1:
        inPgstarNamelist = False
        for i, line in enumerate(i1):
            # print(line.strip('\n\r'))
            l = line.strip("\n\r").rstrip().lstrip()  # remove \n and white spaces
            if "&pgstar" == l.lower():
                inPgstarNamelist = True
                continue  # to avoid adding the first line
            if inPgstarNamelist:
                if (l == "") or (l[0] == "!"):
                    # skip empty lines
                    pass
                else:
                    if l[0] == "/":  # exit
                        inPgstarNamelist = False
                        break
                    else:
                        optionName, value = getNameVal(l)
                        value = cleanVal(value)
                        pgstar[optionName] = value
    return pgstar


# ---------- compare namelists entries between each other and defaults -------------------------


def compareAndReport(k, dic1, dic2, string1, string2, vb=False):
    """
    Given two dictionaries, compares them entry by entry.
    Assumes the inlist name is less than 30 characters.
    The longest MESA parameter is about 45 characters.
    """
    if dic1[k] != dic2[k]:
        print(colored(f"{string1:<30}\t{k}={str(dic1[k]):<45}", "red"))
        print(colored(f"{string2:<30}\t{k}={str(dic2[k]):<45}", "red"))
        print("")
    elif vb:
        print(colored(f"{string1:<30}\t{k}={str(dic1[k]):<45}", "green"))
        print(colored(f"{string2:<30}\t{k}={str(dic2[k]):<45}", "green"))
        print("")


def compareDefaultsAndReport(k, dic, dic_defaults, string, string_other, vb=False):
    """
    Given two dictionaries, compares them entry by entry and prints if not default.
    Assumes the inlist name is less than 30 characters.
    The longest MESA parameter is about 45 characters.
    """
    default = "default"  # for fstring
    try:
        tmp = dic_defaults[k]
    except KeyError:
        print(colored(k + " not in defaults", "yellow"))
        # print(colored(dic_defaults.keys(),"yellow"))
        return
    if dic[k] != dic_defaults[k]:
        print(colored(f"{string:<30}\t{k}={str(dic[k]):<45}", "red"))
        print(colored(f"{string_other:<30}\tmissing", "red"))
        print(colored(f"{default:<30}\t{k}={str(dic_defaults[k]):<45}", "red"))
        print("")
    elif vb:
        print(colored(f"{string:<30}\t{k}={str(dic[k]):<45}", "green"))
        print(colored(f"{default:<30}\t{k}={str(dic_defaults[k]):<45}", "green"))
        print("")


# --------------do the diff on separate namelists ---------------------------


def diffPgstar(pgstar1, pgstar2, string1, string2, MESA_DIR="", vb=False):
    # check the keys appearing in both
    for k in pgstar1.keys() & pgstar2.keys():
        compareAndReport(k, pgstar1, pgstar2, string1, string2, vb)
    # check keys that are not in both and check if they are different than defaults
    defaults = getDefaults("pgstar", MESA_DIR)
    # keys in pgstar1 but not pgstar2
    k1 = set(pgstar1.keys()).difference(set(pgstar2.keys()))
    for k in k1:
        compareDefaultsAndReport(k, pgstar1, defaults, string1, string2, vb)
    # keys in pgstar2 but not pgstar1
    k2 = set(pgstar2.keys()).difference(set(pgstar1.keys()))
    for k in k2:
        compareDefaultsAndReport(k, pgstar2, defaults, string2, string1, vb)

        
def diffStarJob(job1, job2, string1, string2, MESA_DIR="", vb=False):
    # check the keys appearing in both
    for k in job1.keys() & job2.keys():
        compareAndReport(k, job1, job2, string1, string2, vb)
    # check keys that are not in both and check if they are different than defaults
    defaults = getDefaults("star_job", MESA_DIR)
    # keys in job1 but not job2
    k1 = set(job1.keys()).difference(set(job2.keys()))
    for k in k1:
        compareDefaultsAndReport(k, job1, defaults, string1, string2, vb)
    # keys in job2 but not job1
    k2 = set(job2.keys()).difference(set(job1.keys()))
    for k in k2:
        compareDefaultsAndReport(k, job2, defaults, string2, string1, vb)


def diffStarControls(controls1, controls2, string1, string2, MESA_DIR="", vb=False):
    # check the keys appearing in both
    for k in controls1.keys() & controls2.keys():
        compareAndReport(k, controls1, controls2, string1, string2, vb)
    # check keys that are not in both and check if they are different than defaults
    defaults = getDefaults("controls", MESA_DIR)
    # keys in controls1 but not controls2
    k1 = set(controls1.keys()).difference(set(controls2.keys()))
    for k in k1:
        compareDefaultsAndReport(k, controls1, defaults, string1, string2, vb)
    # keys in controls2 but not controls1
    k2 = set(controls2.keys()).difference(set(controls1.keys()))
    for k in k2:
        compareDefaultsAndReport(k, controls2, defaults, string2, string1, vb)


def diffBinaryJob(job1, job2, string1, string2, MESA_DIR="", vb=False):
    # check the keys appearing in both
    for k in job1.keys() & job2.keys():
        compareAndReport(k, job1, job2, string1, string2, vb)
    # check keys that are not in both and check if they are different than defaults
    defaults = getDefaults("binary_job", MESA_DIR)
    # keys in job1 but not job2
    k1 = set(job1.keys()).difference(set(job2.keys()))
    for k in k1:
        compareDefaultsAndReport(k, job1, defaults, string1, string2, vb)
    # keys in job2 but not job1
    k2 = set(job2.keys()).difference(set(job1.keys()))
    for k in k2:
        compareDefaultsAndReport(k, job2, defaults, string2, string1, vb)


def diffBinaryControls(controls1, controls2, string1, string2, MESA_DIR="", vb=False):
    # check the keys appearing in both
    for k in controls1.keys() & controls2.keys():
        compareAndReport(k, controls1, controls2, string1, string2, vb)
    # check keys that are not in both and check if they are different than defaults
    defaults = getDefaults("binary_controls", MESA_DIR)
    # keys in controls1 but not controls2
    k1 = set(controls1.keys()).difference(set(controls2.keys()))
    for k in k1:
        compareDefaultsAndReport(k, controls1, defaults, string1, string2, vb)
    # keys in controls2 but not controls1
    k2 = set(controls2.keys()).difference(set(controls1.keys()))
    for k in k2:
        compareDefaultsAndReport(k, controls2, defaults, string2, string1, vb)


# ----------- do the diff of the whole inlists ----------------------------
def diffInlists(inlist1, inlist2, doPgstar=False, MESA_DIR="", vb=False):
    """
    print a pretty diff of the inlists, or nothing if they are the same.
    will ignore comments and empty lines. Works for single stars and binaries
    TODO: implement this for pgstar
    """
    if MESA_DIR == "":
        MESA_DIR = getMESA_DIR()
        # print(MESA_DIR)
    name1 = inlist1.split("/")[-1]
    name2 = inlist2.split("/")[-1]
    ## check star_job
    job1, isBinary1 = getJobNamelist(inlist1)
    job2, isBinary2 = getJobNamelist(inlist2)
    if isBinary1 != isBinary2:
        print(colored("ERROR: comparing binary to single star!", "red"))
        return
    else:
        if isBinary1 == False:
            # then single stars
            diffStarJob(job1, job2, name1, name2, MESA_DIR, vb)
        else:
            # then binaries
            diffBinaryJob(job1, job2, name1, name2, MESA_DIR, vb)
    print("------end job namelist------")
    ## check constrols
    controls1, isBinary1 = getControlsNamelist(inlist1)
    controls2, isBinary2 = getControlsNamelist(inlist2)
    if isBinary1 != isBinary2:
        print(colored("ERROR: comparing binary to single star!", "red"))
        return
    else:
        if isBinary1 == False:
            # then single stars
            diffStarControls(
                controls1,
                controls2,
                name1,
                name2,                
                MESA_DIR,
                vb,
            )
        else:
            # then binaries
            diffBinaryControls(
                controls1,
                controls2,
                name1,
                name2,
                MESA_DIR,
                vb,
            )
    print("------end controls namelist------")
    if doPgstar:
        # check pgstar
        # this will compare single pgstar namelists and binaries
        pgstar1 = getPgstarNamelist(inlist1)
        pgstar2 = getPgstarNamelist(inlist2)
        # sometimes they can be empty, substitute with defaults
        diffPgstar(pgstar1, pgstar2, name1, name2, MESA_DIR,vb)
        print(colored("at least one pgstar namelists empty", "yellow"))
        print("------end pgstar namelist------")

# # ----------------- for testing on the MESA test_suite -------------------------------
def test_diffInlists(outfile="", MESA_DIR=""):
    """
    Run all possible pairs of inlists from the test_suite as a test
    """
    Failed = 0
    go_on = input("Do you want to do this very long test? [Y/y]")
    if go_on == "Y" or go_on == "y":
        import glob
        import itertools
        import time

        t_start = time.time()
        if MESA_DIR == "":
            MESA_DIR = getMESA_DIR()
        inlists_single = glob.glob(MESA_DIR + "/star/test_suite/*/inlist*")
        inlists_binary = glob.glob(MESA_DIR + "/binary/test_suite/*/inlist*")
        inlists = inlists_binary + inlists_single
        # this below could be parallelized
        for pair in itertools.combinations_with_replacement(inlists, 2):
            inlist1 = pair[0]
            inlist2 = pair[1]
            try:
                diffInlists(inlist1, inlist2, doPgstar=True)
            except:
                print(colored("FAILED: " + inlist1 + " " + inlist2, "yellow"))
                if outfile != "":
                    with open(outfile, "a") as F:
                        F.writelines("FAILED: " + inlist1 + " " + inlist2 + "\n")
                Failed += 1
    else:
        t_start = 0
        print("If you don't try nothing fails...that's perfect!")
    t_end = time.time()
    print("...test took", t_end - t_start, "seconds")
    return Failed


if __name__ == "__main__":
    args = sys.argv
    # args[0] is the name of the script
    inlist1 = args[1]
    inlist2 = args[2]
    MESA_DIR = os.environ["MESA_DIR"]
    # print(colored(MESA_DIR,"yellow"))
    # from command line will interpret anything beyond the 2 inlists as a request for verbosity
    # TODO: implement proper argparse
    if len(sys.argv) > 3:
        vb = True
    else:
        vb = False
    # print("--------------------------------")
    # print(args)
    # print(inlist1, inlist2, MESA_DIR, vb)
    # print("--------------------------------")
    diffInlists(inlist1, inlist2, doPgstar=False, MESA_DIR=MESA_DIR, vb=vb)
    print("done!")
