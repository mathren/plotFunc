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
import re # for getM

def gitPush(description=""):
    push = input('should we push to the git repo first? [Y/n]')
    if ((push == 'Y') or (push == 'y')):
        pwd = os.getcwd() # where am I?
        os.chdir('/mnt/home/mrenzo/Templates/ppisn/')
        os.system('git add . && git commit -am \'about to start a run:'+description+'\' && git push')
        os.chdir(pwd) # go back to previous folder

def checkFolder(folder):
    # checks if folder exists, if not, it creates it, and returns its content
    found=glob.glob(folder)
    if found:
        print("Found folder:", folder)
        content = glob.glob(folder+'/*')
        return content
    if not found:
        os.system("mkdir -p "+str(folder))
        return glob.glob(folder+'/*') ## will be empty
        
def MoveIntoFolder(folder, description=""):
    content = checkFolder(folder)
    if content:
        os.chdir(folder)
        os.system('pwd')
        return 0
    else:
        print("content:", content)
        mkfolder=input(str(folder)+" is not empty. Proceed? [Y/n]")
        if ((mkfolder == 'Y') or (mkfolder == 'y')):
            os.chdir(folder)
            os.system("echo "+description+" > run_description.txt")
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
    return float(m[0])
        