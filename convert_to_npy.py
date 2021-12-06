# author: Mathieu Renzo

# Author: Mathieu Renzo <mathren90@gmail.com>
# Keywords: files

# Copyright (C) 2019-2021 Mathieu Renzo

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

__author__ = "Mathieu Renzo"

from MESAreader import getSrcCol
from utilsLib import getTerminationCode
import sys


def convert_if_terminated(folder, outfname="out.txt", termcode="extras_finish_step"):
    """given a MESA work directory `folder`, looks for the terminal
    output `folder+/outfname` and if the desired termination code
    `termcode` is found, convert the history file to npy"""
    termination_code = getTerminationCode(folder)
    if termination_code == term_code:
        try:
            hfile = folder+'/LOGS/history.data'
            src, col = getSrcCol(hfile, True, True)
        except: #maybe binary?
            hfile1 = folder+'/LOGS1/history.data'
            src, col = getSrcCol(hfile1, True, True)
            hfile2 = folder+'/LOGS2/history.data'
            src, col = getSrcCol(hfile2, True, True)
    else:
        print(folder.split('/')[-2], termination_code)


if __name__ == "__main__":
    """convert to npy binary file the command line argument """
    getSrcCol(sys.argv[1], True, True)
