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
    optionName = line.split('=')[0].rstrip().lstrip()
    optionName = optionName.lower() ## convert everything to lowercase
    value = line.split('=')[-1].split('!')[0].rstrip().lstrip()
    return optionName, value

def convertBool(val):
    #fix occasional typo in the docs
    if (val == ".true.") or (val == ".true"):
        return ".true."
    elif (val == ".false.") or (val == ".false"):
        return ".false."
    else:
        return val

def convertFloat(val):    
    try:
        tmp = val.replace('d','e')
        new_val = float(tmp)
        return new_val
    except:
        return val

def cleanVal(val):
    val = convertFloat(val)    
    val = convertBool(val)    
    return val


def getDefaults(namelist, MESA_DIR=""):
    defaults = {}
    if MESA_DIR == "":
        # read the MESA_DIR from bashrc if not provided
        MESA_DIR = os.environ['MESA_DIR']
    if namelist.lower() == "star_job":
        defaultFname = MESA_DIR+'/star/defaults/star_job.defaults'
    elif namelist.lower() == "binary_job":
        defaultFname = MESA_DIR+'/binary/defaults/binary_job.defaults'
    elif namelist.lower() == "controls":
        defaultFname = MESA_DIR+'/star/defaults/controls.defaults'
    elif namelist.lower() == "binary_controls":
        defaultFname = MESA_DIR+'/binary/defaults/binary_controls.defaults'
    elif namelist.lower() == "pgstar":
        print("pgstar stuff needs to be implemented!", "red")
        return defaults
    else:
        print("Namelist: "+namelist+" not recognized, don't know what to do!", red)
        return defaults
    # now if we did not exit already, load a dict
    # print(defaultFname)
    with open(defaultFname, "r") as f:
        for i, line in enumerate(f):
            l = line.strip('\n\r').rstrip().lstrip() # remove \n and white spaces
            if (l == "") or (l[0] == '!'):
                # empty line or comment, move on
                continue
            else:
                optionName, value = getNameVal(l)
                value = cleanVal(value)
                defaults[optionName] = value
    # Note, the longest key is ~45 characters in length, hence the 45 further down in the string formatting
    return defaults

# -------------------------------------------------------------

def getJobNamelist(inlist):
    """ 
    returns a dictionary of the star_job or binary_job namelist entries and values
    and a flag for binaries
    """
    job = {}
    isBinary = False
    with open(inlist,'r') as i1:     
        inJobNamelist=False
        for i, line in enumerate(i1):
            # print(line.strip('\n\r'))
            l = line.strip('\n\r').rstrip().lstrip() # remove \n and white spaces
            if ("&star_job" == l.lower()):
                inJobNamelist=True
                isBinary = False
                continue # to avoid adding the first line
            elif ("&binary_job" == l.lower()):
                inJobNamelist=True
                isBinary = True
                continue # to avoid adding the first line
            if (inJobNamelist):
                if (l == "") or (l[0] == "!"):
                    #skip empty lines
                    pass
                else:
                    if l[0]=='/': # exit
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
    with open(inlist,'r') as i1:
        inControlsNamelist=False
        for i, line in enumerate(i1):
            # print(line.strip('\n\r'))
            l = line.strip('\n\r').rstrip().lstrip() # remove \n and white spaces
            if ("&controls" == l.lower()):
                inControlsNamelist = True
                isBinary = False
                continue # to avoid adding the first line
            elif ("&binary_controls" == l.lower()):
                inControlsNamelist = True
                isBinary = True
                continue # to avoid adding the first line
            if (inControlsNamelist):
                if (l == "") or (l[0] == "!"):
                    #skip empty lines
                    pass
                else:
                    if l[0]=='/': # exit
                        inJobNamelist = False
                        break
                    else:
                        optionName, value = getNameVal(l)
                        value = cleanVal(value)
                        controls[optionName] = value                
    return controls, isBinary



def diffPgStar(inlist1, inlist2, MESA_DIR="", vb=False):
    print("in diffPgStar...please implement me")
    # TODO: implement me
    return True

def diffStarJob(job1, job2, string1, string2, MESA_DIR="", vb=False):
    # check the keys appearing in both
    for k in job1.keys() & job2.keys():
        if job1[k] != job2[k]:
            print(colored("{:<45}\t{:}={:<45}".format(string1,k,str(job1[k])),"red"))
            print(colored("{:<45}\t{:}={:<45}".format(string2,k,str(job2[k])),"red"))
            print("")
        elif vb:
            print(colored("{:<45}\t{:}={:<45}".format(string1,k,str(job1[k])),"green"))
            print(colored("{:<45}\t{:}={:<45}".format(string2,k,str(job2[k])),"green"))
            print("")
    # check keys that are not in both and check if they are different than defaults
    defaults = getDefaults("star_job", MESA_DIR)        
    # keys in job1 but not job2
    k1 =  set(job1.keys()).difference(set(job2.keys()))
    for k in k1:
        if job1[k] != defaults[k]:
            print(colored("{:<45}\t{:}={:<45}".format(string1,k,str(job1[k])),"red"))
            print(colored("{:<45}\t{:}{:<45}".format(string2,"","missing"),"red"))
            print(colored("{:<45}\t{:}={:<45}".format("default",k,str(defaults[k])),"red"))
            print("")
        elif vb:
            print(colored("{:<45}\t{:}={:<45}".format(string1,k,str(job1[k])),"green"))
            print(colored("{:<45}\t{:}={:<45}".format("default",k,str(defaults[k])),"green"))
            print("")
    # keys in job2 but not job1
    k2 =  set(job2.keys()).difference(set(job1.keys()))
    for k in k2:
        if job2[k] != defaults[k]:
            print(colored("{:<45}\t{:}={:<45}".format(string2,k,str(job2[k])),"red"))
            print(colored("{:<45}\t{:}{:<45}".format(string1,"","missing"),"red"))
            print(colored("{:<45}\t{:}={:<45}".format("default",k,str(defaults[k])),"red"))
            print("")
        elif vb:
            print(colored("{:<45}\t{:}={:<45}".format(string2,k,str(job2[k])),"green"))
            print(colored("{:<45}\t{:}={:<45}".format("default",k,str(defaults[k])),"green"))
            print("")


def diffBinaryJob(job1, job2, string1, string2, MESA_DIR="", vb=False):
    # check the keys appearing in both
    for k in job1.keys() & job2.keys():
        if job1[k] != job2[k]:
            print(colored("{:<45}\t{:}={:<45}".format(string1,k,str(job1[k])),"red"))
            print(colored("{:<45}\t{:}={:<45}".format(string2,k,str(job2[k])),"red"))
            print("")
        elif vb:
            print(colored("{:<45}\t{:}={:<45}".format(string1,k,str(job1[k])),"green"))
            print(colored("{:<45}\t{:}={:<45}".format(string2,k,str(job2[k])),"green"))
            print("")
    # check keys that are not in both and check if they are different than defaults
    defaults = getDefaults("binary_job", MESA_DIR)        
    # keys in job1 but not job2
    k1 =  set(job1.keys()).difference(set(job2.keys()))
    for k in k1:
        if job1[k] != defaults[k]:
            print(colored("{:<45}\t{:}={:<45}".format(string1,k,str(job1[k])),"red"))
            print(colored("{:<45}\t{:}{:<45}".format(string2,"","missing"),"red"))
            print(colored("{:<45}\t{:}={:<45}".format("default",k,str(defaults[k])),"red"))
            print("")
        elif vb:
            print(colored("{:<45}\t{:}={:<45}".format(string1,k,str(job1[k])),"green"))
            print(colored("{:<45}\t{:}={:<45}".format("default",k,str(defaults[k])),"green"))
            print("")
    # keys in job2 but not job1
    k2 =  set(job2.keys()).difference(set(job1.keys()))
    for k in k2:
        if job2[k] != defaults[k]:
            print(colored("{:<45}\t{:}={:<45}".format(string2,k,str(job2[k])),"red"))
            print(colored("{:<45}\t{:}{:<45}".format(string1,"","missing"),"red"))
            print(colored("{:<45}\t{:}={:<45}".format("default",k,str(defaults[k])),"red"))
            print("")
        elif vb:
            print(colored("{:<45}\t{:}={:<45}".format(string2,k,str(job2[k])),"green"))
            print(colored("{:<45}\t{:}={:<45}".format("default",k,str(defaults[k])),"green"))
            print("")

def diffStarControls(controls1, controls2, string1, string2, MESA_DIR="", vb=False):
    # check the keys appearing in both
    for k in controls1.keys() & controls2.keys():
        if controls1[k] != controls2[k]:
            print(colored("{:<45}\t{:}={:<45}".format(string1,k,str(controls1[k])),"red"))
            print(colored("{:<45}\t{:}={:<45}".format(string2,k,str(controls2[k])),"red"))
            print("")
        elif vb:
            print(colored("{:<45}\t{:}={:<45}".format(string1,k,str(controls1[k])),"green"))
            print(colored("{:<45}\t{:}={:<45}".format(string2,k,str(controls2[k])),"green"))
            print("")
    # check keys that are not in both and check if they are different than defaults
    defaults = getDefaults("controls", MESA_DIR)        
    # keys in controls1 but not controls2
    k1 =  set(controls1.keys()).difference(set(controls2.keys()))
    for k in k1:
        ## need ad-hoc fix for overshooting
        if "overshoot" in k:
            k_ov = k.split('(',1)[0]
            if controls1[k] != defaults[k_ov]:
                print(colored("{:<45}\t{:}={:<45}".format(string1,k,str(controls1[k])),"red"))
                print(colored("{:<45}\t{:}{:<45}".format(string2,"","missing"),"red"))
                print(colored("{:<45}\t{:}={:<45}".format("default",k_ov,str(defaults[k_ov])),"red"))
                print("")
            elif vb:
                print(colored("{:<45}\t{:}={:<45}".format(string1,k,str(controls1[k])),"green"))
                print(colored("{:<45}\t{:}={:<45}".format("default",k_ov,str(defaults[k_ov])),"green"))
                print("")
            continue # move on to next item
        if controls1[k] != defaults[k]:
            print(colored("{:<45}\t{:}={:<45}".format(string1,k,str(controls1[k])),"red"))
            print(colored("{:<45}\t{:}{:<45}".format(string2,"","missing"),"red"))
            print(colored("{:<45}\t{:}={:<45}".format("default",k,str(defaults[k])),"red"))
            print("")
        elif vb:
            print(colored("{:<45}\t{:}={:<45}".format(string1,k,str(controls1[k])),"green"))
            print(colored("{:<45}\t{:}={:<45}".format("default",k,str(defaults[k])),"green"))
            print("")
    # keys in controls2 but not controls1
    k2 =  set(controls2.keys()).difference(set(controls1.keys()))
    for k in k2:
        ## need ad-hoc fix for overshooting
        if "overshoot" in k:
            k_ov = k.split('(',1)[0]
            if controls2[k] != defaults[k_ov]:
                print(colored("{:<45}\t{:}={:<45}".format(string2,k,str(controls2[k])),"red"))
                print(colored("{:<45}\t{:}{:<45}".format(string1,"","missing"),"red"))
                print(colored("{:<45}\t{:}={:<45}".format("default",k_ov,str(defaults[k_ov])),"red"))
                print("")
            elif vb:
                print(colored("{:<45}\t{:}={:<45}".format(string2,k,str(controls2[k])),"green"))
                print(colored("{:<45}\t{:}={:<45}".format("default",k_ov,str(defaults[k_ov])),"green"))
                print("")
            continue # move on to next item
        if controls2[k] != defaults[k]:
            print(colored("{:<45}\t{:}={:<45}".format(string2,k,str(controls2[k])),"red"))
            print(colored("{:<45}\t{:}{:<45}".format(string1,"","missing"),"red"))
            print(colored("{:<45}\t{:}={:<45}".format("default",k,str(defaults[k])),"red"))
            print("")
        elif vb:
            print(colored("{:<45}\t{:}={:<45}".format(string2,k,str(controls2[k])),"green"))
            print(colored("{:<45}\t{:}={:<45}".format("default",k,str(defaults[k])),"green"))
            print("")

def diffBinaryControls(controls1, controls2, string1, string2, MESA_DIR="", vb=False):
    # check the keys appearing in both
    for k in controls1.keys() & controls2.keys():
        if controls1[k] != controls2[k]:
            print(colored("{:<45}\t{:}={:<45}".format(string1,k,str(controls1[k])),"red"))
            print(colored("{:<45}\t{:}={:<45}".format(string2,k,str(controls2[k])),"red"))
            print("")
        elif vb:
            print(colored("{:<45}\t{:}={:<45}".format(string1,k,str(controls1[k])),"green"))
            print(colored("{:<45}\t{:}={:<45}".format(string2,k,str(controls2[k])),"green"))
            print("")
    # check keys that are not in both and check if they are different than defaults
    defaults = getDefaults("binary_controls", MESA_DIR)        
    # keys in controls1 but not controls2
    k1 =  set(controls1.keys()).difference(set(controls2.keys()))
    for k in k1:
        if controls1[k] != defaults[k]:
            print(colored("{:<45}\t{:}={:<45}".format(string1,k,str(controls1[k])),"red"))
            print(colored("{:<45}\t{:}{:<45}".format(string2,"","missing"),"red"))
            print(colored("{:<45}\t{:}={:<45}".format("default",k,str(defaults[k])),"red"))
            print("")
        elif vb:
            print(colored("{:<45}\t{:}={:<45}".format(string1,k,str(controls1[k])),"green"))
            print(colored("{:<45}\t{:}={:<45}".format("default",k,str(defaults[k])),"green"))
            print("")
    # keys in controls2 but not controls1
    k2 =  set(controls2.keys()).difference(set(controls1.keys()))
    for k in k2:
        if controls2[k] != defaults[k]:
            print(colored("{:<45}\t{:}={:<45}".format(string2,k,str(controls2[k])),"red"))
            print(colored("{:<45}\t{:}{:<45}".format(string1,"","missing"),"red"))
            print(colored("{:<45}\t{:}={:<45}".format("default",k,str(defaults[k])),"red"))
            print("")
        elif vb:
            print(colored("{:<45}\t{:}={:<45}".format(string2,k,str(controls2[k])),"green"))
            print(colored("{:<45}\t{:}={:<45}".format("default",k,str(defaults[k])),"green"))
            print("")

def diffInlists(inlist1, inlist2, MESA_DIR="", vb=False):
    """
    print a pretty diff of the inlists, or nothing if they are the same.
    will ignore comments and empty lines. Works for single stars and binaries
    TODO: implement this for pgstar
    """
    if MESA_DIR == "":
        # read the MESA_DIR from bashrc if not provided
        MESA_DIR = os.environ['MESA_DIR']
        # print(MESA_DIR)
    ## check star_job
    job1, isBinary1 = getJobNamelist(inlist1)
    job2, isBinary2 = getJobNamelist(inlist2)
    if isBinary1 != isBinary2:
        print(colored("ERROR: comparing one inlist for binaries to one for single stars!","red"))
        return
    else:
        if isBinary1 == False:
            # then single stars
            diffStarJob(job1, job2, inlist1.split('/')[-1], inlist2.split('/')[-1], MESA_DIR,vb)
        else:
            # then binaries
            diffBinaryJob(job1, job2, inlist1.split('/')[-1], inlist2.split('/')[-1], MESA_DIR,vb)
    print("------end job namelist------")
    ## check constrols
    controls1, isBinary1 = getControlsNamelist(inlist1)
    controls2, isBinary2 = getControlsNamelist(inlist2)
    if isBinary1 != isBinary2:
        print(colored("ERROR: comparing one inlist for binaries to one for single stars!","red"))
        return
    else:
        if isBinary1 == False:
            # then single stars
            diffStarControls(controls1, controls2,inlist1.split('/')[-1],inlist2.split('/')[-1], MESA_DIR,vb)
        else:
            # then binaries
            diffBinaryControls(controls1, controls2,inlist1.split('/')[-1],inlist2.split('/')[-1], MESA_DIR,vb)
    print("------end controls namelist------")





if __name__ == "__main__":
    args = sys.argv
    # args[0] is the name of the script
    inlist1 = args[1]
    inlist2 = args[2]
    MESA_DIR = os.environ['MESA_DIR']
    # print(colored(MESA_DIR,"yellow"))
    # from command line will interpret anything beyond the 2 inlists as a request for verbosity
    # TODO: implement proper argparse
    if len(sys.argv) > 3:
        vb=True
    else:
        vb=False
    # print("--------------------------------")
    # print(args)
    # print(inlist1, inlist2, MESA_DIR, vb)
    # print("--------------------------------")
    diffInlists(inlist1, inlist2, MESA_DIR, vb)
    print("done!")
