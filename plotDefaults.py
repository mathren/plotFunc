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

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import rc
from matplotlib import rcParams
from matplotlib.ticker import MultipleLocator, FormatStrFormatter, FuncFormatter, MaxNLocator
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatch
from mpl_toolkits.axes_grid1.inset_locator import inset_axes, zoomed_inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset

# define some colors
Yellow = "#DDDD77"
Green = "#88CCAA"
Blue = "#77AADD"

def is_number(x):
    try:
        float(x)
        return True
    except ValueError:
        return False

def set_plot_defaults_from_matplotlibrc(root="../src/figures/"):
    """given the path of the folder containing the matplotlibrc parses
    the matplotlibrc and set the non-commented parameters.  By default
    it assumes the folder where matplotlibrc is to be ../src/data for
    a showyourwork workflow where notebooks are outside of src.
    """
    # for some reason if you run this function in the same cell containing
    #          ``` from plotDefaults import * ```
    # it will not work as intended. Run it in a separate cell and it works.
    # TODO: understand and fix this behavior.
    from matplotlib import rcParams
    with open(root+"/matplotlibrc", "r") as f:
        for i, line in enumerate(f):
            L = line.rstrip().lstrip()
            if not L: continue # skip empty lines
            if L[0] != "#": # skip commented lines
                # read the line
                uncommented_line = L.split("#")[0].rstrip().lstrip()
                group_param = uncommented_line.split(":")[0].rstrip().lstrip()
                val = uncommented_line.split(":")[-1].rstrip().lstrip()
                # fix figsize
                if "figsize" in group_param:
                    length = tuple(val.split(','))
                rcParams[group_param] = val
    print("done reading matplotlibrc")

def set_plotDefaults():
    """ old way of setting up defaults, maintained for legacy """
    try:
        set_plot_defaults_from_matplotlibrc(".")
        return
    except:
        print("No local matplotlibrc")
        # sets rc param that I like
        # these are also in ./matplotlibrc
        # for some reason if you run this function in the same cell containing
        #          ``` from plotDefaults import * ```
        # it will not work as intended. Run it in a separate cell and it works
        # TODO: understand and fix this behavior.
        rc("text", usetex=True)
        rc("font", serif="palatino")
        rc("font", weight="bold")
        rc("mathtext", default="sf")
        rc("lines", markeredgewidth=2)
        rc("lines", linewidth=3)
        rc("axes", labelsize=30)
        rc("axes", linewidth=2)
        # set fontsize
        rc("xtick", labelsize=30)
        rc("ytick", labelsize=30)
        rc("legend", fontsize=30)
        # ticks stuff
        rc("xtick", top=True, direction="in")
        rc("ytick", right=True, direction="in")
        rc("xtick.major", width=2, size=12, pad=12)
        rc("ytick.major", width=2, size=12, pad=12)
        rc("xtick.minor", width=2, size=6, visible=True)
        rc("ytick.minor", width=2, size=6, visible=True)
        rc(
            "figure",
            figsize=(8.0, 8.0),
            facecolor="white",
            edgecolor="white",
            autolayout=True,
            frameon=False,
        )
        rc("axes", facecolor="white", linewidth=2)
        rc("savefig", facecolor="white", bbox="tight")
        rc("image", cmap="viridis")
        rc("errorbar", capsize=2)
        rc("legend", frameon=False)
        rc("legend", fontsize=30)
        print("done in plotDefaults.py")
