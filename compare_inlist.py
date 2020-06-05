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


## select the Namelist to inspect

def getJobNamelist(inlist):
    job = []
    with open(inlist,'r') as i1:
        inJobNamelist=False
        for i, line in enumerate(i1):
            # print(line.strip('\n\r'))
            l = line.strip('\n\r').rstrip().lstrip() # remove \n and white spaces
            if ("&star_job" == l) or ("&binary_job" == l):
                inJobNamelist=True
                continue # to avoid adding the first line
            if (inJobNamelist):
                if l != "": #skip empty lines
                    if l[0]=='!': # skip comments
                        pass
                    else:
                        if l[0]=='/': # exit
                            inJobNamelist = False
                            break
                        else:
                            job.append(l)
                            # print(l)
                
    return job


def getControlsNamelist(inlist):
    controls = []
    with open(inlist,'r') as i1:
        inControlsNamelist=False
        for i, line in enumerate(i1):
            # print(line.strip('\n\r'))
            l = line.strip('\n\r').rstrip().lstrip() # remove \n and white spaces
            if ("&star_controls" == l) or ("&binary_controls" == l):
                inControlsNamelist=True
                continue # to avoid adding the first line
            if (inControlsNamelist):
                if l != "": #skip empty lines
                    if l[0]=='!': # skip comments
                        pass
                    else:
                        if l[0]=='/': # exit
                            inControlsNamelist = False
                            break
                        else:
                            controls.append(l)
                            # print(l)
                
    return controls
# -----------------------------------------------------------------------

def getNameVal(line):
    optionName = line.split('=')[0].rstrip().lstrip()
    value = line.split('=')[-1].rstrip().lstrip()
    return optionName, value

def convertBool(val):
    if val == ".true.":
        return True
    elif val == ".false.":
        return False
    else:
        return val

def convertFloat(val):
    try:
        new_val = float(val)
        return new_val
    except:
        return val

def cleanVal(val):
    val = convertFloat(val)    
    val = convertBool(val)    
    return val

def compareThisElement(line, other_namelist, MESA_DIR):    
    Found = False
    same = False
    optionName, value = getNameVal(line)
    value = cleanVal(value)
    # print(line)
    # print(optionName)
    # print(value)
    # print("-----")
    for line2 in other_namelist:
        name2, val2 = getNameVal(line2)
        if optionName == name2:
            Found = True
            val2 = cleanVal(val2)
            if value == val2:
                # print(value, val2)
                same = True
    if Found == False:
        # this assume you are comparing apples to apples!
        # i.e. it will give a wrong result if you compare
        # a binary_job with a star_job
        # or a binary_controls with a controls
        same = True
    return same


def comparePgStar(inlist1, inlist2, MESA_DIR):
    # TODO: implement me
    return True

def compareJob(inlist1, inlist2, MESA_DIR):
    # read the two starjobs namelists and compares them
    same = True # initially assume they are the same
    job1 = getJobNamelist(inlist1)
    job2 = getJobNamelist(inlist2)
    # loop on job1
    for line in job1:
        same = compareThisElement(line, job2, MESA_DIR)
    # loop on job2:
    for line in job2:
        same = compareThisElement(line, job1, MESA_DIR)
    return same


def compareControls(inlist1, inlist2, MESA_DIR):
    # read the two starjobs namelists and compares them
    same = True # initially assume they are the same
    controls1 = getControlsNamelist(inlist1)
    controls2 = getControlsNamelist(inlist2)
    # loop on job1
    for line in controls1:
        same = compareThisElement(line, controls2, MESA_DIR)
    # loop on controls2:
    for line in controls2:
        same = compareThisElement(line, controls1, MESA_DIR)
    return same

def compareInlists(inlist1, inlist2, MESA_DIR=""):
    """ 
    compare the inlists ignoring comments and order
    if two parameters are set to the same value, does nothing
    if they are different, print both values.
    """
    if MESA_DIR == "":
        # read the MESA_DIR from bashrc if not provided
        MESA_DIR = os.environ['MESA_DIR']
        # print(MESA_DIR)
    same_job = compareJob(inlist1, inlist2, MESA_DIR)
    same_controls = compareControls(inlist1, inlist2, MESA_DIR)
    # the comparison of Pgstar is still to be implemented
    # same_pgstar = comparePgStar(inlist1,inlist2, MESA_DIR)
    if same_job and same_controls:
        print(colored(inlist1+" and "+inlist2+" set the same physics, assuming you use the same MESA version","green"))
    else:
        print(colored(inlist1+" and "+inlist2+" are different, see the log above", "red"))
        if same_job:
            print(colored(inlist1+" and "+inlist2+" set the same job","green"))
        if same_controls:
            print(colored(inlist1+" and "+inlist2+" set the same controls","green"))
