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

# sys.path.append('path/to/folder/plotFunc/')
from compare_inlists import *


# ------------------------- some auxiliary functions ----------------------------------


def isPathAbsolute(path):
    # print(path[0])
    if path[0] == '/':
        return True
    else:
        return False

def appendInlistPath(path_list, path, workDir="./"):
    # print(path_list, path, workDir)
    if isPathAbsolute(path) == True:
        path_list.append(path)
    else: #it's relative
        path_list.append(workDir+'/'+path)
    return path_list


def getFirstInlist(workDir):
    inlist = workDir+"/inlist"
    if os.path.isfile(inlist):
        return inlist
    else:
        print(colored(workDir+" does not contain an inlist, this is too complex for me","yellow"))
        sys.exit()
    

# ------------------ check if there are nested namelists -------------------------------

    
def checkIfMoreStarJob(job, workDir="./"):
    """
    Check if there are more star_job namelists to be read and returns a 
    list of the paths to their inlists
    """
    inlists_to_be_read=[]
    if job.get("read_extra_star_job_inlist1") == ".true.":
        new_inlist = job.get("extra_star_job_inlist1_name").strip('\'').strip('\"')
        inlists_to_be_read = appendInlistPath(inlists_to_be_read, new_inlist, workDir)
    if job.get("read_extra_star_job_inlist2") == ".true.":    
        new_inlist = job.get("extra_star_job_inlist2_name").strip('\'').strip('\"')
        inlists_to_be_read = appendInlistPath(inlists_to_be_read, new_inlist, workDir)
    if job.get("read_extra_star_job_inlist3") == ".true.":
        new_inlist = job.get("extra_star_job_inlist3_name").strip('\'').strip('\"')
        inlists_to_be_read = appendInlistPath(inlists_to_be_read, new_inlist, workDir)
    if job.get("read_extra_star_job_inlist4") == ".true.":
        new_inlist = job.get("extra_star_job_inlist4_name").strip('\'').strip('\"')
        inlists_to_be_read = appendInlistPath(inlists_to_be_read, new_inlist, workDir)    
    if job.get("read_extra_star_job_inlist5") == ".true.":
        new_inlist = job.get("extra_star_job_inlist5_name").strip('\'').strip('\"')
        inlists_to_be_read = appendInlistPath(inlists_to_be_read, new_inlist, workDir)
    return inlists_to_be_read


def checkIfMoreControls(controls, workDir="./"):
    """
    Check if there are more controls namelists to be read and returns a 
    list of the paths to their inlists
    """
    inlists_to_be_read=[]
    if controls.get("read_extra_controls_inlist1") == ".true.":
        new_inlist = controls.get("extra_controls_inlist1_name").strip('\'').strip('\"')
        inlists_to_be_read = appendInlistPath(inlists_to_be_read, new_inlist, workDir)
    if controls.get("read_extra_controls_inlist2") == ".true.":    
        new_inlist = controls.get("extra_controls_inlist2_name").strip('\'').strip('\"')
        inlists_to_be_read = appendInlistPath(inlists_to_be_read, new_inlist, workDir)
    if controls.get("read_extra_controls_inlist3") == ".true.":
        new_inlist = controls.get("extra_controls_inlist3_name").strip('\'').strip('\"')
        inlists_to_be_read = appendInlistPath(inlists_to_be_read, new_inlist, workDir)
    if controls.get("read_extra_controls_inlist4") == ".true.":
        new_inlist = controls.get("extra_controls_inlist4_name").strip('\'').strip('\"')
        inlists_to_be_read = appendInlistPath(inlists_to_be_read, new_inlist, workDir)    
    if controls.get("read_extra_controls_inlist5") == ".true.":
        new_inlist = controls.get("extra_controls_inlist5_name").strip('\'').strip('\"')
        inlists_to_be_read = appendInlistPath(inlists_to_be_read, new_inlist, workDir)
    return inlists_to_be_read


def checkIfMorePgstar(pgstar, workDir="./"):
    """
    Check if there are more pgstar namelists to be read and returns a 
    list of the paths to their inlists
    """
    inlists_to_be_read=[]
    if pgstar.get("read_extra_pgstar_inlist1") == ".true.":
        new_inlist = pgstar.get("extra_pgstar_inlist1_name").strip('\'').strip('\"')
        inlists_to_be_read = appendInlistPath(inlists_to_be_read, new_inlist, workDir)
    if pgstar.get("read_extra_pgstar_inlist2") == ".true.":    
        new_inlist = pgstar.get("extra_pgstar_inlist2_name").strip('\'').strip('\"')
        inlists_to_be_read = appendInlistPath(inlists_to_be_read, new_inlist, workDir)
    if pgstar.get("read_extra_pgstar_inlist3") == ".true.":
        new_inlist = pgstar.get("extra_pgstar_inlist3_name").strip('\'').strip('\"')
        inlists_to_be_read = appendInlistPath(inlists_to_be_read, new_inlist, workDir)
    if pgstar.get("read_extra_pgstar_inlist4") == ".true.":
        new_inlist = pgstar.get("extra_pgstar_inlist4_name").strip('\'').strip('\"')
        inlists_to_be_read = appendInlistPath(inlists_to_be_read, new_inlist, workDir)    
    if pgstar.get("read_extra_pgstar_inlist5") == ".true.":
        new_inlist = pgstar.get("extra_pgstar_inlist5_name").strip('\'').strip('\"')
        inlists_to_be_read = appendInlistPath(inlists_to_be_read, new_inlist, workDir)
    return inlists_to_be_read


# ----------------- build the dictionary that MESA will use ------------------------------


def buildMasterStarJob(workDir):
    """
    Builds the namelist by reading the inlists starting from inlist 
    """
    first_inlist = getFirstInlist(workDir)
    job = getJobNamelist(first_inlist)[0]
    inlists_to_be_read = checkIfMoreStarJob(job, workDir=workDir)
    # print(inlists_to_be_read)
    while inlists_to_be_read:
        current_inlist = inlists_to_be_read[0]
        print("...reading "+current_inlist+" star_job namelist")
        job_to_add = getJobNamelist(current_inlist)[0]
        inlists_to_add = checkIfMoreStarJob(job_to_add, workDir=workDir)
        job = {**job, **job_to_add}
        ## note: if the same read_extra_star_job is used in multiple
        ## inlists, only the last one works because settings
        ## overwrites. That's also how MESA works
        # print(job)
        ## remove inlist we are doing now from list
        inlists_to_be_read = inlists_to_be_read.remove(current_inlist)
        ## add possible new inlists
        if  inlists_to_add != None:
            try:
                inlists_to_be_read = inlists_to_be_read + inlists_to_add
            except TypeError:
                # could be that inlists_to_be_read is empty
                # but we still want to add stuff
                inlists_to_be_read = inlists_to_add
    return job


def buildMasterControls(workDir):
    """
    Builds the namelist by reading the inlists starting from inlist 
    """
    first_inlist = getFirstInlist(workDir)
    controls = getControlsNamelist(first_inlist)[0]
    inlists_to_be_read = checkIfMoreControls(controls, workDir=workDir)
    # print(inlists_to_be_read)
    while inlists_to_be_read:
        current_inlist = inlists_to_be_read[0]
        print("...reading "+current_inlist+" controls namelist")
        controls_to_add = getControlsNamelist(current_inlist)[0]
        inlists_to_add = checkIfMoreControls(controls_to_add, workDir=workDir)
        controls = {**controls, **controls_to_add}
        ## note: if the same read_extra_star_controls is used in multiple
        ## inlists, only the last one works because settings
        ## overwrites. That's also how MESA works
        # print(controls)
        ## remove inlist we are doing now from list
        inlists_to_be_read = inlists_to_be_read.remove(current_inlist)
        ## add possible new inlists
        if  inlists_to_add != None:
            try:
                inlists_to_be_read = inlists_to_be_read + inlists_to_add
            except TypeError:
                # could be that inlists_to_be_read is empty
                inlists_to_be_read = inlists_to_add
    return controls


def buildMasterPgstar(workDir):
    """
    Builds the namelist by reading the inlists starting from inlist 
    """
    first_inlist = getFirstInlist(workDir)
    pgstar = getPgstarNamelist(first_inlist)
    inlists_to_be_read = checkIfMorePgstar(pgstar, workDir=workDir)
    # print(inlists_to_be_read)
    while inlists_to_be_read:
        current_inlist = inlists_to_be_read[0]
        print("...reading "+current_inlist+" pgstar namelist")
        pgstar_to_add = getPgstarNamelist(current_inlist)
        inlists_to_add = checkIfMorePgstar(pgstar_to_add, workDir=workDir)
        pgstar = {**pgstar, **pgstar_to_add}
        ## note: if the same read_extra_star_pgstar is used in multiple
        ## inlists, only the last one works because settings
        ## overwrites. That's also how MESA works
        # print(pgstar)
        ## remove inlist we are doing now from list
        inlists_to_be_read = inlists_to_be_read.remove(current_inlist)
        ## add possible new inlists
        if  inlists_to_add != None:
            try:
                inlists_to_be_read = inlists_to_be_read + inlists_to_add
            except TypeError:
                # could be that inlists_to_be_read is empty
                inlists_to_be_read = inlists_to_add
    return pgstar


# ----------------------------- do the comparison ----------------------------------


def compareSingleWorkDirs(work1, work2, doPgstar=False, MESA_DIR="", vb=False):
    """ compare the MESA setup in two work directories allowing for multiple nested inlists"""
    # for now works only for single stars
    # TODO implement binaries
    if work1.split('/')[-1]:
        name1 = "1: "+work1.split('/')[-1]
    else:
        name1 = "1: "+work1.split('/')[-2]
    if work2.split('/')[-1]:
        name2 = "2: "+work2.split('/')[-1]
    else:
        name2 = "2: "+work2.split('/')[-2]

    # star_job
    job1 = buildMasterStarJob(work1)
    job2 = buildMasterStarJob(work2)
    print("")
    print("&star_job")
    print("")
    diffStarJob(job1, job2, name1, name2, MESA_DIR, vb)
    print("/ !end star_job namelist")
    print("")
    # controls
    controls1 = buildMasterControls(work1)
    controls2 = buildMasterControls(work2)
    print("")
    print("&controls")
    print("")
    diffControls(controls1, controls2, name1, name2, MESA_DIR, vb)
    print("")
    print("/ !end controls namelist")
    print("")
    if doPgstar:
        pgstar1 = buildMasterPgstar(work1)
        pgstar2 = buildMasterPgstar(work2)
        print("")
        print("&pgstar")
        print("")
        diffPgstar(pgstar1, pgstar2, name1, name2, MESA_DIR, vb)
        print("")
        print("/ !end pgstar")

# command line wrapper
@click.command(context_settings={"ignore_unknown_options": True})
@click.argument("work_dir1", nargs=1, type=click.Path(exists=True))
@click.argument("work_dir2", nargs=1, type=click.Path(exists=True))
@click.option("--pgstar", default=False, help="Show also diff of pgstar namelists.")
@click.option(
    "--mesa_dir",
    default="",
    help="use customized location of $MESA_DIR. Will use environment variable if empty and return an error if empty.",
)
@click.option("--vb", default=False, help="Show also matching lines using green.")
def cli_wrapper_directories(work_dir1, work_dir2, pgstar, mesa_dir, vb):
    compareSingleWorkDirs(work_dir1, work_dir2, doPgstar=pgstar, MESA_DIR=mesa_dir, vb=vb)
    print("")
    print("*********")
    print("* done! *")
    print("*********")


if __name__ == "__main__":
    cli_wrapper_directories()
    
